import sqlite3
from pprint import pprint
from flask import g
import pathlib
import mutagen
import json
import time
import colorama #https://www.geeksforgeeks.org/python/print-colors-python-terminal/
from colorama import Style #https://stackoverflow.com/questions/33199172/python3-cannot-reset-colors-with-colorama-module
from pyobjtojson import obj_to_json #black magic witchcraft #https://deepwiki.com/carlosplanchon/pyobjtojson
from obj_todict import todict
import taglib
import os
from ffmpeg import FFmpeg
from unidecode import unidecode
from pymediainfo import MediaInfo

def unicode(textvalue):
    if textvalue is not None:
        return unidecode(textvalue)
    else:
        return None

def sum_unique_values(sizejson):
    summedsize = 0
    for ind_size in json.loads(sizejson).keys():
        summedsize += json.loads(sizejson)[ind_size]

    return summedsize

def get_db():
    if 'db' not in g: #https://sqlpey.com/python/solved-how-to-handle-sqlite-threading-issues-in-flask/
        g.db = sqlite3.connect('spider.db')
        g.db.row_factory = sqlite3.Row
        #https://pytutorial.com/python-sqlite3-create_function-custom-functions-guide/
        g.db.create_function('unicode', 1, unicode)
        g.db.create_function('sum_unique_values', 1, sum_unique_values)
    return g.db

def dbcreate():
    #https://docs.python.org/2/library/sqlite3.html#using-the-connection-as-a-context-manager
    with get_db() as mycursor:

        #maybe change inode to tagfileinode and meta to livemeta, but not now so things don't break.

        mycursor.execute('''CREATE TABLE IF NOT EXISTS file(
        inode INT PRIMARY KEY NOT NULL,
        ogfileinode INT,
        scantime INT NOT NULL,
        tagfilescantime INT,
        streampath TEXT NOT NULL UNIQUE, 
        size INT NOT NULL, 
        modtime INT NOT NULL, 
        meta TEXT,
        ogmeta_audio TEXT,
        ogmeta_video TEXT,
        duration REAL, 
        hastagfile INT NOT NULL, 
        artinode INT)''')

        #the foreign key constraint has to be listed last
        #purposely making the xvalue able to have null values
        mycursor.execute('''CREATE TABLE IF NOT EXISTS metadata(
        key TEXT NOT NULL,
        xvalue TEXT,
        fk_inode INT NOT NULL REFERENCES file(inode) ON DELETE CASCADE ON UPDATE CASCADE,
        UNIQUE(key, xvalue, fk_inode))''') 

        #https://youtu.be/eXMA_2dEMO0

        mycursor.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS metadata_fts USING fts5(fk_inode, key, xvalue)''')

        mycursor.execute('''CREATE TRIGGER IF NOT EXISTS after_insert 
        AFTER INSERT ON metadata BEGIN
        INSERT INTO metadata_fts (fk_inode, key, xvalue) VALUES (NEW.fk_inode, NEW.key, NEW.xvalue);
        END
        ''')

        mycursor.execute('''CREATE TRIGGER IF NOT EXISTS after_update
        AFTER UPDATE ON metadata BEGIN
        UPDATE metadata_fts SET 
        key = NEW.key,
        xvalue = NEW.xvalue
        WHERE fk_inode = NEW.fk_inode;
        END
        ''')

        mycursor.execute('''CREATE TRIGGER IF NOT EXISTS after_delete
        AFTER DELETE ON metadata BEGIN
        DELETE FROM metadata_fts WHERE metadata_fts.fk_inode = OLD.fk_inode;
        END
        ''')

        mycursor.execute('''CREATE VIEW IF NOT EXISTS metadata_by_path AS
        SELECT file.streampath, metadata.key, metadata.xvalue FROM metadata JOIN file ON metadata.fk_inode = file.inode
        ''')

def pathfrominode(inode):
    with get_db() as mycursor:
        query = f"SELECT streampath FROM file WHERE file.inode = {inode}"
        mypathresult = mycursor.execute(query).fetchone()
        return mypathresult

def getone(tab, itemid):
    with get_db() as mycursor:
        match tab:
            case 'artist':
                selection = 'ARTIST'
            case 'album':
                selection = 'ALBUM'
            case 'track':
                selection = 'TITLE'
            case 'genre':
                selection = 'GENRE'

        itemid_query = itemid
        releasedate_query = 'AND :releasedate = :releasedate'
        releasedate = 0

        if '---' in itemid:
            if itemid.split('---')[1] != '': #taking care of the case where there is no date attached
                itemid_query = itemid.split('---')[0]
                releasedate = itemid.split('---')[1]
                releasedate_query = "AND meta->>'$.DATE[0]' LIKE :releasedate"
            else:
                itemid_query = itemid.removesuffix('---')

        assert selection in ['ARTIST', 'ALBUM', 'TITLE', 'GENRE']
                
        query = f'''SELECT inode, ogfileinode, artinode,
        meta->>'$.ARTIST' as artists, 
        meta->>'$.TITLE[0]' as title, 
        streampath, 
        value as item 
        FROM file, json_each(file.meta, '$.{selection}') 
        WHERE item = :itemid_query {releasedate_query}'''

        myresult = mycursor.execute(query, {
            'itemid_query': itemid_query,
            'releasedate': releasedate
        }).fetchall()
        return myresult

#def item_select(sort, direction, searchvalue, artist, tab):
def item_select(filters): #artist not incorporated yet
    with get_db() as mycursor:


        if 'sortby' in filters.keys():
            sqlsortby = filters['sortby']
        else:
            sqlsortby = 'name'
        sqlsortby2 = ', namesort ASC' #'ARTIST ASC' makes it secondarily sort by the name so it's alphabetical when in other sorts

        if 'direction' in filters.keys():
            sqldirection = filters['direction']
        else:
            sqldirection = 'desc'

        if sqlsortby == 'name':
            sqlsortby = 'namesort'
            sqlsortby2 = ''
            if sqldirection.lower() == 'asc': #NEEDS TO BE LOWERCASE
                sqldirection = 'DESC' #REVERSE FOR MORE INTUITIVENESS, I assume only for sorting by name.
            elif sqldirection.lower() == 'desc': #NEEDS TO BE LOWERCASE
                sqldirection = 'ASC'

        if 'searchvalue' in filters.keys():
            sqlsearchvalue = filters['searchvalue']
        else:
            sqlsearchvalue = ''

        pprint(sqlsearchvalue)

        if 'id' in filters.keys():
            sqlidmatch = filters['id']
        else:
            sqlidmatch = ''

        '''
        if 'album' in filters.keys():
            duration_query = 'SUM(file.duration)'
        else:
            duration_query = 'file.duration'
        '''

        #Previously had: REPLACE(LOWER(value), '(', '') AS namesort
        commonselection = '''
        file.ogfileinode, 
        file.inode,
        file.artinode,
        LOWER(metadata.xvalue) AS namesort, 
        metadata.xvalue as namedisplay, 
        MAX(file.modtime) AS modified, 
        sum_unique_values(JSON_GROUP_OBJECT(file.inode, file.size)) AS size, 
        MAX(metadata_date.xvalue) as releasedate,
        sum_unique_values(JSON_GROUP_OBJECT(file.inode, file.duration)) as duration,
        file.streampath,
        COUNT(DISTINCT file.inode) AS filecount,
        COUNT(DISTINCT metadata_album.xvalue) AS albumcount,
        JSON_GROUP_ARRAY(DISTINCT metadata_artists.xvalue) AS artists_json,
        JSON_GROUP_ARRAY(DISTINCT metadata_genres.xvalue) AS genres_json
        '''

        # the word 'value' is important
        #https://sqlite.org/json1.html#jptr
        #https://stackoverflow.com/questions/58519714/how-to-extract-properly-when-sqlite-json-has-value-as-an-array
        '''
        match filters['tab']:
            case 'artist':
                #the "as" names need to match the "sort" value that comes in
                statement = f"SELECT {commonselection}, count(file.inode) AS filecount, COUNT(DISTINCT file.meta->'$.ALBUM') AS albumcount FROM file, json_each(file.meta, '$.ARTIST')"
                #statement2 = select mbids and somehow
            case 'album':
                statement = f"SELECT {commonselection}, file.meta->'$.ALBUMARTIST' AS artists_json, count(file.inode) AS filecount FROM file, json_each(file.meta, '$.ALBUM')"
            case 'genre':
                statement = f"SELECT {commonselection}, count(file.inode) AS filecount, COUNT(DISTINCT meta->'$.ALBUM') AS albumcount FROM file, json_each(file.meta, '$.GENRE')"
            case 'track':
                statement = f"SELECT {commonselection}, file.meta->'$.ARTIST' AS artists_json FROM file, json_each(file.meta, '$.TITLE')"
        '''

        if filters['tab'] == 'track':
            key_to_filterby = 'TITLE'
        else:
            key_to_filterby = filters['tab'].upper()

        statement = f'''SELECT {commonselection} 
        FROM file JOIN metadata ON file.inode = metadata.fk_inode 
        JOIN metadata AS metadata_album ON file.inode = metadata_album.fk_inode 
        JOIN metadata AS metadata_date ON file.inode = metadata_date.fk_inode
        JOIN metadata AS metadata_artists ON file.inode = metadata_artists.fk_inode
        JOIN metadata AS metadata_genres ON file.inode = metadata_genres.fk_inode
        WHERE metadata.key = '{key_to_filterby}' 
        AND metadata_album.key = 'ALBUM' 
        AND metadata_date.key = 'DATE'
        AND metadata_artists.key = 'ARTIST'
        AND metadata_genres.key = 'GENRE'
        '''
        
        possible_filters = ['artist', 'album', 'genre', 'date']
        '''
        for entity in sqlclauses.keys():

            if entity not in filters.keys():
                pass
            elif filters['tab'] != entity:
                sqlclauses[entity] = f"AND file.meta->'$.{entity.upper()}' LIKE '%{filters[entity]}%'"
            elif filters['tab'] == entity:
                sqlclauses[entity] = f"AND unicode(namedisplay) LIKE '%{filters[entity]}%'"
        '''

        pprint(filters)

        sqlclauses = ''
        for possible_filter in possible_filters:
            if possible_filter in filters.keys() and filters[possible_filter] != '': #2nd part is for example when there is an album with no date set and the split with --- returns an empty string
                match possible_filter:
                    case 'artist':
                        sqlclauses += f" AND (unicode(metadata_artists.xvalue) = '{filters[possible_filter]}' OR metadata_artists.xvalue = '{filters[possible_filter]}')" #for when a client is actually using a weird character as a search
                    case 'album':
                        sqlclauses += f" AND unicode(metadata_album.xvalue) = '{filters[possible_filter]}'"
                    case 'genre':
                        sqlclauses += f" AND unicode(metadata_genres.xvalue) = '{filters[possible_filter]}'"
                    case 'date':
                        sqlclauses += f" AND unicode(metadata_date.xvalue) = '{filters[possible_filter]}'"              

        #unicode is my defined function above
        if sqlsearchvalue != '':
            statement += f" AND unicode(namedisplay) LIKE '%{sqlsearchvalue}%'"
        
        if sqlidmatch != '':
            statement += f" AND namedisplay = '{sqlidmatch}'"

        if 'inode' in filters.keys():
            statement += f" AND file.inode = '{filters['inode']}'"

        statement += f'''{sqlclauses}
        AND namedisplay IS NOT NULL 
        GROUP BY namedisplay 
        ORDER BY {sqlsortby} {sqldirection}{sqlsortby2}'''

        myresult = {}
        myresult['namematch'] = mycursor.execute(statement).fetchall()

        '''
        for file in myresult['namematch']:

            for current_inode in file['inode'].split(','):

                artist_statement = f"SELECT metadata.xvalue FROM metadata WHERE metadata.key = 'ARTIST' AND metadata.fk_inode = '{current_inode}'"

                myresult[current_inode] = {}

                myresult[current_inode]['artists'] = mycursor.execute(artist_statement).fetchall()
        '''


        #NOT the sum of file.size here
        commonselection2 = '''
        GROUP_CONCAT(file.ogfileinode) AS ogfileinode, 
        GROUP_CONCAT(file.inode) as inode,
        GROUP_CONCAT(file.artinode) AS artinode,
        LOWER(metadata.xvalue) AS namesort, 
        metadata.xvalue as namedisplay, 
        MAX(file.modtime) AS modified, 
        file.size AS size,
        MAX(metadata_date.xvalue) as releasedate,
        file.duration,
        file.streampath,
        COUNT(file.inode) AS filecount,
        COUNT(metadata_album.xvalue) AS albumcount,
        JSON_GROUP_ARRAY(DISTINCT metadata_artists.xvalue) AS artists_json,
        JSON_GROUP_OBJECT(metadata_any.key, metadata_any.xvalue) as parseme
        '''

        #working right here to update this statement
        myresult['anymatch'] = {}
        if filters['tab'] == 'track':
            statement = f'''SELECT {commonselection2}
            FROM file JOIN metadata ON file.inode = metadata.fk_inode
            JOIN metadata AS metadata_any ON metadata_any.fk_inode = file.inode
            JOIN metadata AS metadata_date ON metadata_date.fk_inode = file.inode
            JOIN metadata AS metadata_album ON metadata_album.fk_inode = file.inode
            JOIN metadata AS metadata_artists ON metadata_artists.fk_inode = file.inode
            WHERE unicode(metadata.xvalue) NOT LIKE '%{sqlsearchvalue}%' AND unicode(metadata_any.xvalue) LIKE '%{sqlsearchvalue}%'
            AND metadata.key = 'TITLE'
            AND metadata_date.key = 'DATE'
            AND metadata_album.key = 'ALBUM'
            AND metadata_artists.key = 'ARTIST'
            GROUP BY file.inode 
            ORDER BY {sqlsortby} {sqldirection}{sqlsortby2}'''

            #print(statement)

            myresult['anymatch'] = mycursor.execute(statement).fetchall()

        return myresult

def update_meta(mycursor, diskfile_info):
    '''
    cover_art_exclude_list = ['APIC:cover', 'APIC:', 'metadata_block_picture', 'Cover Art (Front)', 'Cover Art (Back)']
    mutagen_metadata = mutagen.File(filesystem_path)
    
    reconstructed_dict = obj_to_json(mutagen_metadata) #black magic

    pprint(reconstructed_dict['tags'])
    
    for mykey in cover_art_exclude_list:
        try:
            reconstructed_dict['tags']['_DictProxy__dict'].pop(mykey, None)
        except TypeError: #if the art key does not exist
            pass
    '''

    if diskfile_info['streampath'].split('.')[-1] == 'tag':

        symlinkpath = pathlib.Path(f"{os.getcwd()}/symlink-for-taglib.mp3")
        symlinkpath_temp = symlinkpath.with_suffix('.temp')

        #https://stackoverflow.com/questions/8299386/modifying-a-symlink-in-python
        os.symlink(src=diskfile_info['streampath'], dst=symlinkpath_temp)
        os.replace(symlinkpath_temp, symlinkpath)

        path_for_taglib_consumption = symlinkpath

    else: #NOT A TAG FILE
        path_for_taglib_consumption = diskfile_info['streampath']

    mediainfo_audio_json = None
    mediainfo_video_json = None

    try:
        taglib_dict = taglib.File(path_for_taglib_consumption).tags
        taglib_json = json.dumps(taglib_dict)
    except OSError:
        #with the current set of files, we have not hit this condition yet
        taglib_json = None

        #yes these are nested. Intention is to save space by only saving these to db for video files/ things taglib can't parse
        mediainfo_audio_dict = MediaInfo.parse(diskfile_info['streampath']).to_data()['tracks'][0]
        mediainfo_video_dict = MediaInfo.parse(diskfile_info['streampath']).to_data()['tracks'][1]
        mediainfo_audio_json = json.dumps(mediainfo_audio_dict)
        mediainfo_video_json = json.dumps(mediainfo_video_dict)

    #separted this try-except because in the case of mkv files, the pathlib scanning of the .tag file is fine, but pathlib can't scan the real mkv for length
    try:
        diskfile_length = taglib.File(diskfile_info['streampath']).length
    except OSError:
        diskfile_length = float(MediaInfo.parse(diskfile_info['streampath'].removesuffix('.tag')).to_data()['tracks'][1]['duration'])/1000

    mycursor.execute(
        "UPDATE file SET meta = :meta, ogmeta_audio = :ogmeta_audio, ogmeta_video = :ogmeta_video, duration = :duration WHERE file.inode = :inode", 
        {
            'meta': taglib_json,
            'ogmeta_audio': mediainfo_audio_json,
            'ogmeta_video': mediainfo_video_json,
            'duration': diskfile_length, 
            'inode': diskfile_info['inode']
        }
    )

    def metadata_insert(key, listvalue):

        pprint(key)
        pprint(listvalue)

        mycursor.execute('''INSERT OR REPLACE INTO metadata (
        fk_inode, key, xvalue
        ) VALUES (
        :fk_inode, :key, :xvalue
        )''', {
            'fk_inode': diskfile_info['inode'],
            'key': key,
            'xvalue': listvalue
        })
        '''
        except sqlite3.IntegrityError: #UNIQUE constraint failed: metadata.key, metadata.xvalue, metadata.fk_inode
            #'PERFORMER:AUTHOR': ['Donald Roeser', 'Donald Roeser'], for this shit I guess
            pprint('error')
        '''

    for key in taglib_dict.keys():

        if type(taglib_dict[key]) is list:
            for listvalue in taglib_dict[key]:
                metadata_insert(key, listvalue)
        else:
            metadata_insert(key, taglib_dict[key])

    for entity in ['ARTIST', 'ALBUM', 'DATE', 'GENRE']:
        if entity not in taglib_dict.keys():
            pprint(entity)
            metadata_insert(entity, None)

def preliminary_insert_row(mycursor, diskfile_info):
    mycursor.execute('''INSERT INTO file (
    inode, scantime, streampath, size, modtime, hastagfile, artinode, ogfileinode
    ) VALUES (
    :inode, :scantime, :streampath, :size, :modtime, :hastagfile, :artinode, :ogfileinode
    )''', diskfile_info) #meta and duration not included here

    update_meta(mycursor, diskfile_info)

def artwork(filepath, inode):

    constructedpath = f"{os.getcwd()}/staticx/art/{inode}.jpg"

    if pathlib.Path(constructedpath).is_file():
        return inode
    else:
        #https://alexwlchan.net/til/2024/get-artwork-from-an-mp3-file/
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(filepath)
            .output(
                constructedpath#,{"codec:v": "copy"},
            )
        )
        try:
            ffmpeg.execute()
            pprint(f'NEW ART FILE: {filepath}')
            return inode
        except:
            return None

def diskfile_dict_generator(filesystem_livepath, scan_start_time):
    #attributes of current file
    #https://stackoverflow.com/questions/10374412/unique-file-id      
    #https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-file
    #https://www.pythonpool.com/python-hexadecimal-to-decimal/

    artinode = None

    if str(filesystem_livepath).split('.')[-1] == 'tag':
        filesystem_ogpath = pathlib.Path(str(filesystem_livepath).removesuffix('.tag'))
        sizetouse = filesystem_livepath.stat().st_size + filesystem_ogpath.stat().st_size
        modtime_touse = max(filesystem_livepath.stat().st_mtime, filesystem_ogpath.stat().st_mtime)
        tagfile_scantime = scan_start_time
        hastagfile = True
        ogfileinode = filesystem_ogpath.stat().st_ino
        artinode = artwork(str(filesystem_ogpath), filesystem_ogpath.stat().st_ino)
    else:
        sizetouse = filesystem_livepath.stat().st_size
        modtime_touse = filesystem_livepath.stat().st_mtime
        tagfile_scantime = None
        hastagfile = False
        ogfileinode = None

    if artinode is None:
        artinode = artwork(str(filesystem_livepath), filesystem_livepath.stat().st_ino)

    return {
        'inode': filesystem_livepath.stat().st_ino,
        'ogfileinode': ogfileinode,
        'scantime': scan_start_time,
        'tagfilescantime': tagfile_scantime,
        'streampath': str(filesystem_livepath),
        'size': sizetouse,
        'modtime': modtime_touse,
        'hastagfile': hastagfile, #sqlite doesn't have bools - will go into db as 0 and will be overwritten with a 1 if code wants to
        'artinode': artinode
        #meta columns and duration not included here
    }

def prepare_file_for_db(mycursor, diskfile_info, actlikenew):

    #we are doing a query instead of a "throw at the wall" try/except because we want to only have valid audio files in the db, and we also want to only mutagen/taglib-scan things when absolutely needed
    #we don't want to insert a row of a non-audio file just to have to drop the row later
    db_row = mycursor.execute( 
        "SELECT inode, streampath, modtime, hastagfile FROM FILE WHERE file.inode = :inode", 
        {
            'inode': diskfile_info['inode']
        }
    ).fetchone()  

    if db_row is None: #not in the db             
        preliminary_insert_row(mycursor, diskfile_info)
        print(colorama.Fore.GREEN + 'NEW: ' + diskfile_info['streampath'] + Style.RESET_ALL)
    #already in db, so need to do further testing! #sqlite3.IntegrityError: UNIQUE constraint failed: file.id
    else:
        #scantime is the only thing that will definitely change
        mycursor.execute(
            'UPDATE file SET scantime = :scantime, tagfilescantime = :tagfilescantime WHERE file.inode = :inode', 
            {
                'scantime': diskfile_info['scantime'],
                'tagfilescantime': diskfile_info['tagfilescantime'],
                'inode': diskfile_info['inode']
            }
        )

        changed_in_some_way = False #... initially

        #test #1 - if the file was modified
        if diskfile_info['modtime'] != db_row['modtime'] or actlikenew == 1: 
        #if mod time different, then must update size, modtime, and metadata
            mycursor.execute(
                "UPDATE file SET size = :size, modtime = :modtime, artinode = :artinode WHERE file.inode = :inode", 
                {
                    'size': diskfile_info['size'], #this includes the combined size of the tagfile and ogfile already
                    'modtime': diskfile_info['modtime'],
                    'artinode': diskfile_info['artinode'],
                    'inode': diskfile_info['inode']
                }
            )
            #then use the function to go and edit the metadata
            update_meta(mycursor, diskfile_info)
            print(colorama.Fore.YELLOW + "UPDATING: " + diskfile_info['streampath'] + Style.RESET_ALL)
            changed_in_some_way = True


        #test #2 - if the file was renamed, change the name
        if diskfile_info['streampath'] != db_row['streampath']:
            mycursor.execute(
                "UPDATE file SET streampath = :streampath WHERE file.inode = :inode",
                {
                    'streampath': diskfile_info['streampath'],
                    'inode': diskfile_info['inode']
                }
            )
            print(colorama.Fore.YELLOW + "RENAMING: " + diskfile_info['streampath'] + Style.RESET_ALL)
            changed_in_some_way = True

        #test #3 - if it changed from an "og file" to a regular file not connected to a .tag file
        if diskfile_info['hastagfile'] != db_row['hastagfile']:
            mycursor.execute(
                "UPDATE file SET hastagfile = :hastagfile WHERE file.inode = :inode",
                {
                    'hastagfile': diskfile_info['hastagfile'],
                    'inode': diskfile_info['inode']
                }
            )
            if diskfile_info['hastagfile'] == False:
                print(colorama.Fore.YELLOW + "SEPARATED FROM .TAG FILE: " + diskfile_info['streampath'] + Style.RESET_ALL)
            elif diskfile_info['hastagfile'] == True:
                print(colorama.Fore.YELLOW + "CONNECTED TO NEW .TAG FILE: " + diskfile_info['streampath'] + Style.RESET_ALL)
            changed_in_some_way = True      

        if changed_in_some_way == False:
            print(colorama.Fore.BLUE + 'NO CHANGE: ' + diskfile_info['streampath'] + Style.RESET_ALL)


def dbscan(myapp):

    dbcreate()

    with get_db() as mycursor:

        mediapath = myapp.config['MEDIAPATH']
        mediapath = pathlib.Path(mediapath)

        scan_start_time = int(time.time()) #https://realcoding.blog/2025/05/05/python-timestamp-complete-guide-en/
        pprint("SCAN START TIME: " + str(scan_start_time))

        inodes_to_exclude = []

        #PASS 1 - TAGFILES
        for filesystem_path in mediapath.rglob("*.tag"):
            if filesystem_path.is_file():

                diskfile_info = diskfile_dict_generator(
                    filesystem_livepath=filesystem_path, 
                    scan_start_time=scan_start_time
                )

                prepare_file_for_db(mycursor, diskfile_info, actlikenew=myapp.config['ACTLIKENEW'])

                inodes_to_exclude.append(diskfile_info['inode'])
                inodes_to_exclude.append(diskfile_info['ogfileinode'])
                
        #PASS 2 - EVERYTHING ELSE    
        audio_formats = ['mp3', 'mp2', 'flac', 'ogg', 'oga', 'm4a', 'wav', 'wma']
        for filesystem_path in mediapath.rglob("*.*"):
            if filesystem_path.is_file() and filesystem_path.stat().st_ino not in inodes_to_exclude:
                if filesystem_path.suffix.removeprefix('.') in audio_formats: #checking suffixes because otherwise you would be repeatedly scanning non-audio on every scan, or having non-audio in the database marked as a "do not scan"
                    diskfile_info = diskfile_dict_generator(filesystem_livepath=filesystem_path, scan_start_time=scan_start_time)
                    prepare_file_for_db(mycursor, diskfile_info, actlikenew=myapp.config['ACTLIKENEW'])

        #the other way to do this would be to iterate through all db rows and see if the file exists based on the path or inode. However, if the user ends up changing their path/scan filters, then things would not be properly deleted from the DB that way.
        
        left_behind_files = mycursor.execute('SELECT streampath, count(inode) AS left_behind_count FROM file WHERE file.scantime < :scan_start_time GROUP BY file.inode', 
        {'scan_start_time': scan_start_time}).fetchone()
        if left_behind_files != None:
            count_left_behind_files = left_behind_files['left_behind_count']
            pprint(left_behind_files['streampath'])
        else:
            count_left_behind_files = 0
        print(f'Deleting [{count_left_behind_files}] old files........:')
        mycursor.execute('DELETE FROM file WHERE file.scantime < :scan_start_time', {'scan_start_time': scan_start_time})

        if pathlib.Path(f"{os.getcwd()}/symlink-for-taglib.mp3").is_file():
            os.unlink(f"{os.getcwd()}/symlink-for-taglib.mp3") #to be nice and cleann

    '''
    while True:
        time.sleep(3)
        pprint("every 3 seconds")
    '''


'''
#old innefective manual method for mutagen dicts to json conversion
reconstructed_dict = {}
for mutagen_key in mutagen_metadata.keys():
    pprint(mutagen_key)
    if mutagen_key not in cover_art_exclude_list:
        reconstructed_dict[mutagen_key] = str(mutagen_metadata[mutagen_key])
        pprint(mutagen_metadata[mutagen_key])

'''