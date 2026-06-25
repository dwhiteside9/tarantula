from actions import * #actions.py
from app import * #app.py
from string import ascii_uppercase

def returnsubsonic(subsonic_endpoint, filesystem_path):

    def albumList2():

        base = {
            'album': []
        }

        filters = {'tab': 'album'}

        if request.values['type'] == 'byGenre':
            filters['genre'] = request.values['genre']

        myresult = item_select(filters)

        for item in myresult['namematch']:
            base['album'].append(AlbumID3(item))

        return base

    def artists():
        base = {
            "ignoredArticles": "The An A Die Das Ein Eine Les Le La",
            "index": []
        }

        for character in ascii_uppercase:
            base['index'].append({
                "name": character,
                "artist": []
            })

        myresult = item_select({'tab': 'artist'})

        for item in myresult['namematch']:
            artist_obj = ArtistID3(item)
            first_character = item['namedisplay'][0].upper()
            index_number = ascii_uppercase.index(first_character)
            base['index'][index_number]['artist'].append(artist_obj)

        return base

    def user():
        base = {
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

        return base

    def genres():

        base = {'genre': []}

        myresult = item_select({'tab': 'genre'})

        for item in myresult['namematch']:
            curr_album = {}

            curr_album['songCount'] = item['filecount']
            curr_album['albumCount'] = item['albumcount']
            curr_album['value'] = item['namedisplay']

            base['genre'].append(curr_album)

        return base

    def searchResult3(request):
        searchvalue = request.args['query']

        base = {
            'artist': [],
            'album': [],
            'song': []
        }

        for item in item_select({'tab': 'artist'})['namematch']:
            base['artist'].append(ArtistID3(item))            

        for item in item_select({'tab': 'album'})['namematch']:
            base['album'].append(AlbumID3(item))

        for item in item_select({'tab': 'track', 'searchvalue': searchvalue})['namematch']:
            base['song'].append(Child(item))

        return base

    def songsByGenre(request):
        base = {'songsByGenre': song()}

        for item in item_select({'genre': request.args['genre'], 'tab': 'track'})['namematch']:
            base['songsByGenre']['song'].append(Child(item))

        return base

    def randomSongs(request):
        base = {'randomSongs': songs()}

        myquery_args = {'tab': 'track'}

        if 'genre' in request.args:
            myquery_args['genre'] = request.args['genre']

        for item in item_select(myquery_args)['namematch']:
            base['randomSongs']['song'].append(Child(item))

        return base

    def songs():
        base = {'song': []}
        return base

    def topSongs(request):

        base = songs()

        myresult = item_select({'artist': request.args['artist'], 'tab': 'track'})

        for item in myresult['namematch']:
            base['song'].append(Child(item))

        return base

    def AlbumID3WithSongs(albumid):

        pprint('album id: ')
        pprint(albumid)

        pprint('datesplit: ')
        pprint(albumid.split('---')[1])

        for item in item_select({'tab': 'album','album': albumid.split('---')[0], 'date': albumid.split('---')[1]})['namematch']:
            #only one expected result
            base = AlbumID3(item)

        myresult = item_select({'album': albumid.split('---')[0], 'tab': 'track'})

        for item in myresult['namematch']:
            base['song'].append(Child(item))

        return base

    def ArtistWithAlbumsID3(artistid):

        base = {
            'artist': {}
        }

        for item in item_select({'id': artistid, 'tab': 'artist'})['namematch']:
            base['artist'] = ArtistID3(item)

        for item in item_select({'artist': artistid, 'tab': 'album'})['namematch']:
            base['artist']['album'].append(AlbumID3(item)) #yeah from what I can see the album is embedded inside the artist

        return base

    def artistInfo(artistid):
        return {
            'artistInfo': {
                'biography': 'biographyyyy'
            }
        }


    def artpath(artid):
        artpath = f"{os.getcwd()}/staticx/art/{artid}.jpg"

        if (pathlib.Path(artpath)).is_file():
            return artpath
        else:
            return 'deadpath'

    def Child(item):

        artistid3_array = []

        for artist_return in item_select({'inode': item['inode'], 'tab': 'artist'})['namematch']:
            artistid3_array.append(ArtistID3(artist_return))

        albumname = None
        albumdate = None

        for albumreturn in item_select({'tab': 'album', 'inode': item['inode']})['namematch']:
            albumname = albumreturn['namedisplay']
            albumdate = albumreturn['releasedate']

        return {
            'id': item['inode'],
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
        base = {
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

        return base

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
        '''
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
        '''

        curr_album['artists'] = []

        if item['artists_json'] is not None:
            for artistid in json.loads(item['artists_json']):
                myresult = item_select({'id': artistid, 'tab': 'artist'})
                for item in myresult['namematch']:
                    curr_album['artists'].append(ArtistID3(item))

        curr_album['year'] = item['releasedate']
        curr_album['genre'] = 'test genre - albumid3'

        curr_album['song'] = [] #for use with AlbumID3WithSongs

        return curr_album

    if subsonic_endpoint not in ['ping.view']:
        subsonic_endpoint = subsonic_endpoint.removesuffix('.view')

    match subsonic_endpoint:
        case 'ping.view':
            subobject = {}
        case 'ping': #for supersonic
            xmldata = '<subsonic-response status="ok" version="1.1.1"> </subsonic-response>'
            return Response(xmldata, mimetype='text/xml') #https://stackoverflow.com/a/11774026
        case 'getTopSongs':
            subobject = {
                'topSongs': topSongs(request)
            }
        case 'getArtists':
            subobject = {
                'artists': artists()
            }

        case 'getAlbumList2':
            subobject = {
                'albumList2': albumList2()
            }

        case 'getUser': #takes "username" argument
            subobject = user()

        case 'getGenres':
            subobject = {
                'genres': genres()
            }

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
            subobject = {
                'searchResult3': searchResult3(request)
            }

        case 'getSongsByGenre':
            subobject = songsByGenre(request)

        case 'getRandomSongs':
            subobject = randomSongs(request)

        case 'getArtist':
            subobject = ArtistWithAlbumsID3(request.args['id'])

        case 'getArtistInfo':
            subobject = artistInfo(request.args['id'])

        case 'getAlbum':
            subobject = {
                'album': AlbumID3WithSongs(request.args['id'])
            }

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

    subobject['status'] = 'ok'
    subobject['version'] = '1.16.1'
    subobject['type'] = "Tarantula (OpenSubsonic)"
    subobject['serverVersion'] = '0.0.1'
    subobject['openSubsonic'] = True

    return { #make this a class?????
        "subsonic-response": subobject
    }
        