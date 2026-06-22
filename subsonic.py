from actions import * #actions.py
from app import * #app.py
from string import ascii_uppercase

def returnsubsonic(subsonic_endpoint, filesystem_path):

    def AlbumID3WithSongs(albumid):
        pprint('album id: ')
        pprint(albumid)

        for item in item_select({'tab': 'album','album': albumid.split('---')[0], 'date': albumid.split('---')[1]})['namematch']:
            #only one expected result
            baseresponse = AlbumID3(item)

        baseresponse['song'] = []

        myresult = item_select({'album': albumid.split('---')[0], 'tab': 'track'})

        for item in myresult['namematch']:
            baseresponse['song'].append(Child(item))

        pprint(baseresponse)
        return baseresponse

    def ArtistWithAlbumsID3(artistid):

        pprint(artistid)

        for item in item_select(
            {
                'artist': artistid, 
                'tab': 'artist'
            }
        )['namematch']:
            baseresponse = ArtistID3(item)

        for item in item_select({'artist': artistid, 'tab': 'album'})['namematch']:
            baseresponse['album'].append(AlbumID3(item))

        return baseresponse

    def artistInfo(artistid):
        return {
            'biography': 'biographyyyy'
        }


    def artpath(artid):
        artpath = f"{os.getcwd()}/staticx/art/{artid}.jpg"

        if (pathlib.Path(artpath)).is_file():
            return artpath
        else:
            return 'deadpath'

    def Child(item):

        artistid3_array = []

        for artist in json.loads(item['artists_json']):
            for artist_return in item_select({'id': artist, 'tab': 'artist'})['namematch']:
                #should be only 1 iteration of this for loop
                artistid3_array.append(ArtistID3(artist_return))

        pprint(item['inode'].split(',')[0])

        albumname = None
        albumdate = None

        for albumreturn in item_select({'tab': 'album', 'inode': item['inode'].split(',')[0]})['namematch']:
            albumname = albumreturn['namedisplay']
            albumdate = albumreturn['releasedate']

        return {
            'id': item['inode'].split(',')[0],
            'parent': 'parentalbum',
            'isDir': False,
            'title': item['namedisplay'],
            'album': albumname,
            'artist': json.loads(item['artists_json'])[0],
            'track': 1,
            'genre': 'genreee',
            'coverArt': item['artinode'],
            'size': item['size'],
            'contenttype': 'audio/mpeg',
            'suffix': item['streampath'].split('.')[-1],
            'transcodedContentType': 'mp3',
            'transcodedSuffix': 'mp3',
            'duration': item['duration'],
            'bitRate': 444,
            'bitDepth': 0,
            'samplingRate': 0,
            'channelCount': 2,
            'path': 'path',
            'isVideo': False,
            'userRating': 1,
            'averageRating': 1,
            'playCount': 0,
            'discNumber': 1,
            'created': '2000-01-01T00:00:00',
            'starred': '2000-01-01T00:00:00',
            'albumId': f'{albumname}---{albumdate}',
            'artistId': json.loads(item['artists_json'])[0],
            'type': 'music',
            'mediaType': 'song', #song/album/artist??
            'bookmarkPosition': 0,
            'originalwidth': 100,
            'played': '2000-01-01T00:00:00',
            'bpm': 100,
            'comment': 'testcomment',
            'sortName': item['namesort'],
            'musicBrainzId': item['namedisplay'],
            'isrc': '',
            'genres': [],
            'artists': artistid3_array,
            'displayArtist': 'display artist',
            'albumArtists': [],
            'displayAlbumArtist': 'display album artist',
            'contributors': [],
            'displayComposer': 'display composer',
            'moods': [],
            'replaygain': {},
            'explicitStatus':'', #explicit/clean/""
        }

    def ArtistID3(item):
        artistid3_return = {
            'whatami?': 'artistid3',
            'id': item['namedisplay'],
            'name': item['namedisplay'],
            'coverArt': item['artinode'],
            'albumCount': item['albumcount'],
            'userRating': 2,
            'artistImageUrl': '',
            'starred': '2001-01-01T000:00:00',
            'musicBrainzId': item['namedisplay'],
            'sortName': item['namesort'],
            'roles': [],
            'album': [] #for use with artistswithalbumsid3
        }

        return artistid3_return

    def AlbumID3(item):
        curr_album = {}
        albumid = item['namedisplay'] + '---'

        if item['releasedate'] is not None:
            albumid += item['releasedate']

        curr_album['id'] = albumid

        curr_album['album'] = item['namedisplay']
        curr_album['name'] = item['namedisplay']
        curr_album['title'] = item['namedisplay']
   
        curr_album['coverArt'] = item['artinode']

        curr_album['songCount'] = item['filecount']
        #curr_album['created'] = "2021-07-22T02:09:31+00:00"
        curr_album['created'] = item['modified']
        curr_album['duration'] = item['duration']
        curr_album['playCount'] = 0
        


        #EDIT TO ROUTE TO ARTISTID3
        if item['artists_json'] is not None:

            curr_album['artistId'] = json.loads(item['artists_json'])[0]

            curr_album['artists'] = []
            for artist in json.loads(item['artists_json']):
                indiv_artist = {}
                indiv_artist['id'] = artist
                indiv_artist['name'] = artist
                curr_album['artists'].append(indiv_artist)
            if subsonic_endpoint == 'getAlbumList2':
                curr_album['artist'] = json.loads(item['artists_json'])[0]
        else:
            curr_album['artistId'] = 'idkyet'

            if subsonic_endpoint == 'getAlbumList2':
                curr_album['artist'] = ''
            curr_album['artists'] = []
        curr_album['year'] = item['releasedate']
        curr_album['genre'] = 'test genre'

        #pprint(curr_album)

        return curr_album

    if subsonic_endpoint not in ['ping.view', 'ping']:
        subsonic_endpoint = subsonic_endpoint.removesuffix('.view')

    match subsonic_endpoint:
        case 'ping.view':
            subobject = {}
        case 'ping': #for supersonic
            xmldata = '<subsonic-response status="ok" version="1.1.1"> </subsonic-response>'
            return Response(xmldata, mimetype='text/xml') #https://stackoverflow.com/a/11774026
        case 'getArtists':

            subobject = {
                "ignoredArticles": "The An A Die Das Ein Eine Les Le La",
                "index": []
            }

            for character in ascii_uppercase:
                subobject['index'].append({
                    "name": character,
                    "artist": []
                })

            myresult = item_select({'tab': 'artist'})

            for item in myresult['namematch']:
                artist_obj = ArtistID3(item)
                first_character = item['namedisplay'][0].upper()
                index_number = ascii_uppercase.index(first_character)
                subobject['index'][index_number]['artist'].append(artist_obj)

        case 'getAlbumList2':

            filters = {'tab': 'album'}

            if request.values['type'] == 'byGenre':
                filters['genre'] = request.values['genre']

            pprint(filters)

            myresult = item_select(filters)

            subobject = {}
            subobject['album'] = []

            for item in myresult['namematch']:
                curr_album = AlbumID3(item)

                subobject['album'].append(curr_album)

        case 'getUser':

            #pprint(getUser)

            subobject = {

                "username": "drew",
                "email": "sindre@activeobjects.no",
                "scrobblingEnabled": "true",
                "adminRole": "false",
                "settingsRole": "true",
                "downloadRole": "true",
                "uploadRole": "false",
                "playlistRole": "true",
                "coverArtRole": "true",
                "commentRole": "true",
                "podcastRole": "true",
                "streamRole": "true",
                "jukeboxRole": "true",
                "shareRole": "false"
            }

        case 'getGenres':
            myresult = item_select({'tab': 'genre'})

            subobject = {}
            subobject['genre'] = []

            for item in myresult['namematch']:
                curr_album = {}

                curr_album['songCount'] = item['filecount']
                curr_album['albumCount'] = item['albumcount']
                curr_album['value'] = item['namedisplay']

                subobject['genre'].append(curr_album)

        case 'getCoverArt':
            artid = request.args.get('id')
            filename = artpath(artid)
            #https://stackoverflow.com/a/53026574

            if filename != 'deadpath':
                return send_file(filename, mimetype='image/jpg')
            else:
                #returning any xml document to show a failure - according to opensubsonic
                xmldata = '<iamdead> </iamdead>'
                return Response(xmldata, mimetype='text/xml')

        case 'search3':

            searchvalue = request.args['query']

            pprint(searchvalue)

            subobject = {
                'artist': [],
                'album': [],
                'song': []
            }

            for item in item_select({'tab': 'artist'})['namematch']:

                subobject['artist'].append(ArtistID3(item))            

            for item in item_select({'tab': 'album'})['namematch']:

                subobject['album'].append(AlbumID3(item))

            for item in item_select({'tab': 'track', 'searchvalue': searchvalue})['namematch']:

                subobject['song'].append(Child(item))

        case 'getSongsByGenre':
            subobject = {
                'song': []
            }

            if 'genre' in request.args:
                genre = request.args['genre']
                result_part_to_use = 'anymatch'
            else:
                genre = ''
                result_part_to_use = 'namematch'

            myresult = item_select({'genre': genre,  'tab': 'track'})

            for item in myresult[result_part_to_use]:
                curr_song = Child(item)

                subobject['song'].append(curr_song)

        case 'getArtist':
            subobject = ArtistWithAlbumsID3(request.args['id'])

        case 'getArtistInfo':
            subobject = artistInfo(request.args['id'])

        case 'getAlbum':
            subobject = AlbumID3WithSongs(request.args['id'])

        case 'stream':
            fileid = request.args.get('id')
            streampath = pathfrominode(fileid)['streampath']

            filesystem_path = pathlib.Path(streampath).parent
            streampath = pathlib.Path(streampath).name.removesuffix('.tag')
            return make_response( send_from_directory(filesystem_path, streampath) )

        case 'art2':
            '''
            f = taglib.File(r'D:\data\music\scan\public\_sync\a_\4 Lit _ B.o.B; T.I._Ty Dolla $ign.mp3')

            pic_binary_data = f.pictures[0].data

            return Response(pic_binary_data, mimetype='image/jpeg')
            '''

            return 'hi'
    
        case _: #default case
            return 'not valid!!1!'

    endpoint_mapper = {
        'ping': '',
        'ping.view': '',
        'getArtist': 'artist',
        'getArtists': 'artists',
        'getAlbumList2': 'albumList2',
        'getUser': 'user',
        'getGenres' : 'genres',
        'getAlbum': 'album',
        'search3': 'searchResult3',
        'getSongsByGenre': 'songsByGenre',
        'getArtistInfo': 'artistInfo',
        'getAlbum': 'album'
    }

    return { #make this a class?????
        "subsonic-response": {
            "status": "ok",
            "version": "1.16.1",
            "type": "Spider Server (OpenSubsonic)",
            "serverVersion": "0.0.1",
            "openSubsonic": True,
            endpoint_mapper[subsonic_endpoint]: subobject
        }
    }
        