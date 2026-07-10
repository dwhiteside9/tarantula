from actions import * #actions.py
from app import * #app.py
from string import ascii_uppercase

def returnsubsonic(subsonic_endpoint, filesystem_path):

    #boiler
    def playlists():
        base = {
            "playlist": [
                {
                "id": "562949953630815",
                "name": "random - admin - private (admin)",
                "owner": "admin",
                "public": False,
                "created": "2017-04-11T10:42:50.842Z",
                "changed": "2017-04-11T10:42:50.842Z",
                "songCount": 43,
                "duration": 17875
                },
                {
                "id": "562949953630815",
                "name": "random - admin - public (admin)",
                "owner": "admin",
                "public": True,
                "created": "2017-04-11T10:42:50.842Z",
                "changed": "2017-04-11T10:42:50.842Z",
                "songCount": 43,
                "duration": 17786
                }
            ]
        }

        return base

    #boiler
    def starred2():
        base = {
            "artist": [
                {
                "id": "37ec820ca7193e17040c98f7da7c4b51",
                "name": "2 Mello",
                "coverArt": "ar-37ec820ca7193e17040c98f7da7c4b51_0",
                "albumCount": 1,
                "userRating": 5,
                "artistImageUrl": "https://demo.org/image.jpg",
                "starred": "2017-04-11T10:42:50.842Z"
                }
            ],
            "album": [
                {
                "id": "ad0f112b6dcf83de5e9cae85d07f0d35",
                "name": "8-bit lagerfeuer",
                "artist": "pornophonique",
                "year": 2007,
                "coverArt": "al-ad0f112b6dcf83de5e9cae85d07f0d35_640a93a8",
                "starred": "2023-03-22T01:51:06Z",
                "duration": 1954,
                "playCount": 97,
                "genre": "Hip-Hop",
                "created": "2023-03-10T02:19:35.784818075Z",
                "artistId": "91c3901ac465b9efc439e4be4270c2b6",
                "songCount": 8
                }
            ],
            "song": [
                {
                "id": "082f435a363c32c57d5edb6a678a28d4",
                "parent": "e8a0685e3f3ec6f251649af2b58b8617",
                "isDir": False,
                "title": "\"polar expedition\"",
                "album": "Live at The Casbah - 2005-04-29",
                "artist": "The New Deal",
                "track": 4,
                "year": 2005,
                "coverArt": "mf-082f435a363c32c57d5edb6a678a28d4_6410b3ce",
                "size": 19866778,
                "contentType": "audio/flac",
                "suffix": "flac",
                "starred": "2023-03-27T09:45:27Z",
                "duration": 178,
                "bitRate": 880,
                "bitDepth": 16,
                "samplingRate": 44100,
                "channelCount": 2,
                "path": "The New Deal/Live at The Casbah - 2005-04-29/04 - \"polar expedition\".flac",
                "playCount": 8,
                "discNumber": 1,
                "created": "2023-03-14T17:51:22.112827504Z",
                "albumId": "e8a0685e3f3ec6f251649af2b58b8617",
                "artistId": "97e0398acf63f9fb930d7d4ce209a52b",
                "type": "music",
                "isVideo": False
                }
            ]
        }

        return base


    #boiler
    def starred():
        base = {
            "artist": [
                {
                "id": "100000002",
                "name": "Synthetic",
                "coverArt": "ar-100000002",
                "starred": "2021-02-22T05:54:18Z"
                }
            ],
            "album": [
                {
                "id": "200000021",
                "parent": "100000036",
                "album": "Forget and Remember",
                "title": "Forget and Remember",
                "name": "Forget and Remember",
                "isDir": True,
                "coverArt": "al-200000021",
                "songCount": 20,
                "created": "2017-04-11T10:42:50.842Z",
                "duration": 4248,
                "playCount": 0,
                "artistId": "100000036",
                "artist": "Comfort Fit",
                "year": 2005,
                "genre": "Hip-Hop"
                }
            ],
            "song": [
                {
                "id": "082f435a363c32c57d5edb6a678a28d4",
                "parent": "e8a0685e3f3ec6f251649af2b58b8617",
                "isDir": False,
                "title": "\"polar expedition\"",
                "album": "Live at The Casbah - 2005-04-29",
                "artist": "The New Deal",
                "track": 4,
                "year": 2005,
                "coverArt": "mf-082f435a363c32c57d5edb6a678a28d4_6410b3ce",
                "size": 19866778,
                "contentType": "audio/flac",
                "suffix": "flac",
                "starred": "2023-03-27T09:45:27Z",
                "duration": 178,
                "bitRate": 880,
                "bitDepth": 16,
                "samplingRate": 44100,
                "channelCount": 2,
                "path": "The New Deal/Live at The Casbah - 2005-04-29/04 - \"polar expedition\".flac",
                "playCount": 8,
                "discNumber": 1,
                "created": "2023-03-14T17:51:22.112827504Z",
                "albumId": "e8a0685e3f3ec6f251649af2b58b8617",
                "artistId": "97e0398acf63f9fb930d7d4ce209a52b",
                "type": "music",
                "isVideo": False
                }
            ]
        }

        return base


    #boiler
    def openSubsonicExtensions():
        base = [
            {
                "name": "template",
                "versions": [
                    1,
                    2
                ]
            }
        ]

        return base

    #boiler
    def directory():
        base = {
            "id": "1",
            "name": "music",
            "child": [
                {
                    "id": "100000016",
                    "parent": "1",
                    "isDir": True,
                    "title": "CARNÚN",
                    "artist": "CARNÚN",
                    "coverArt": "ar-100000016"
                },
                {
                    "id": "100000027",
                    "parent": "1",
                    "isDir": True,
                    "title": "Chi.Otic",
                    "artist": "Chi.Otic",
                    "coverArt": "ar-100000027"
                }
            ]
        }
        return base

    #boiler
    def lyrics():
        base = {
            "artist": "Metallica",
            "title": "Blitzkrieg",
            "value": "Let us have peace, let us have life\n\nLet us escape the cruel night\n\nLet us have time, let the sun shine\n\nLet us beware the deadly sign\n\n\n\nThe day is coming\n\nArmageddon's near\n\nInferno's coming\n\nCan we survive the blitzkrieg?\n\nThe blitzkrieg\n\nThe blitzkrieg\n\n\n\nSave us from fate, save us from hate\n\nSave ourselves before it's too late\n\nCome to our need, hear our plea\n\nSave ourselves before the earth bleeds\n\n\n\nThe day is dawning\n\nThe time is near\n\nAliens calling\n\nCan we survive the blitzkrieg?"
        }
        return base

    #boiler
    def license():
        base = {
            "valid": True,
            "email": "demo@demo.org",
            "licenseExpires": "2097-04-11T10:42:50.842Z",
            "trialExpires": "2097-04-11T10:42:50.842Z"
        }
        return base

    #boiler
    def internetRadioStations():
        base = {
            "internetRadioStation": [
                {
                "id": "1",
                "name": "HBR1.com - Dream Factory",
                "streamUrl": "http://ubuntu.hbr1.com:19800/ambient.aac",
                "homePageUrl": "http://www.hbr1.com/",
                "coverArt": "ir-1"
                },
                {
                "id": "2",
                "name": "HBR1.com - I.D.M. Tranceponder",
                "streamUrl": "http://ubuntu.hbr1.com:19800/trance.ogg",
                "homePageUrl": "http://www.hbr1.com/",
                "coverArt": "ir-2"
                },
                {
                "id": "3",
                "name": "4ZZZ Community Radio",
                "streamUrl": "https://stream.4zzz.org.au:9200/4zzz",
                "homePageUrl": "https://4zzzfm.org.au",
                "coverArt": "ir-3"
                }
            ]
        }
        return base

    #boiler
    def indexes():
        base = {
            "shortcut": [
                {
                "id": "11",
                "name": "Audio books"
                },
                {
                "id": "10",
                "name": "Podcasts"
                }
            ],
            "index": [
                {
                "artist": [
                    {
                    "id": "1",
                    "name": "ABBA"
                    },
                    {
                    "id": "2",
                    "name": "Alanis Morisette"
                    },
                    {
                    "id": "3",
                    "name": "Alphaville",
                    "starred": "2017-04-11T10:42:50.842Z"
                    }
                ],
                "name": "A"
                },
                {
                "artist": {
                    "name": "Bob Dylan",
                    "id": "4"
                },
                "name": "B"
                }
            ],
            "child": [
                {
                "id": "111",
                "parent": "11",
                "title": "Dancing Queen",
                "isDir": "false",
                "album": "Arrival",
                "artist": "ABBA",
                "track": "7",
                "year": "1978",
                "genre": "Pop",
                "coverArt": "24",
                "size": "8421341",
                "contentType": "audio/mpeg",
                "suffix": "mp3",
                "duration": "146",
                "bitRate": "128",
                "path": "ABBA/Arrival/Dancing Queen.mp3"
                },
                {
                "id": "112",
                "parent": "11",
                "title": "Money, Money, Money",
                "isDir": "false",
                "album": "Arrival",
                "artist": "ABBA",
                "track": "7",
                "year": "1978",
                "genre": "Pop",
                "coverArt": "25",
                "size": "4910028",
                "contentType": "audio/flac",
                "suffix": "flac",
                "transcodedContentType": "audio/mpeg",
                "transcodedSuffix": "mp3",
                "duration": "208",
                "bitRate": "128",
                "path": "ABBA/Arrival/Money, Money, Money.mp3"
                }
            ],
            "lastModified": "237462836472342",
            "ignoredArticles": "The El La Los Las Le Les"
        }

        return base


    def xmlresponse():
        xmldata = '<subsonic-response status="ok" version="1.1.1"> </subsonic-response>'
        return Response(xmldata, mimetype='text/xml') #https://stackoverflow.com/a/11774026

    def stream_or_download(request, filesystem_path):
        fileid = request.args.get('id')
        streampath = pathfrominode(fileid)['streampath']

        filesystem_path = pathlib.Path(streampath).parent
        streampath = pathlib.Path(streampath).name.removesuffix('.tag')
        return make_response( send_from_directory(filesystem_path, streampath) )

    #boiler
    def agent():
        base = {
            "id": "lead",
            "role": "main",
            "name": "Chris Martin"
        }

        return base

    def AlbumID3(item):

        albumid = item['namedisplay'] + '---'

        if item['releasedate'] is not None:
            albumid += item['releasedate']

        try:
            year = int(item['releasedate'].split('-')[0])
        except:
            year = None

        base = {
            'id': albumid,
            'name': item['namedisplay'],
            'version': 'Version Placeholder',
            'artist': 'artistplaceholder',
            'year': year,
            'coverArt': str(item['artinode']),
            'starred': '2017-04-11T10:42:50.842Z',
            'duration': int(item['duration']),
            'playCount': 99,
            'genre': 'genreplaceholder',
            'created': '2017-04-11T10:42:50.842Z', #eventually change to modified
            'artistId': 'artistid placeholder',
            'songCount': item['filecount'],
            'played': '2017-04-11T10:42:50.842Z',
            'userRating': 0,
            #'recordLabels': [],
            'musicBrainzId': 'musicbrainz temp',
            'genres': [],
            'artists': [],
            'displayArtist': 'Display Artist placeholder',
            #'releaseTypes': [],
            #'moods': [],
            'sortName': item['namesort'],
            #'originalReleaseDate': {},
            #'releaseDate': {},
            'isCompilation': False,
            'explicitStatus': 'explicit',
            #'discTitles': []
        }
        
        if item['artists_json'] is not None:
            for artistid in json.loads(item['artists_json']):
                myresult = item_select({'id': artistid, 'tab': 'artist'})
                for item in myresult['namematch']:
                    base['artists'].append(ArtistID3(item))

        if item['genres_json'] is not None:
            for genre in json.loads(item['genres_json']):
                myresult = item_select({'id': genre, 'tab': 'genre'})
                for item in myresult['namematch']:
                    base['genres'].append(ItemGenre(item))

        base['genre'] = base['genres'][0]['name'] #Aonsoku only shows it on the album page if this is a key
        
        return base

    def AlbumID3WithSongs(albumid):

        pprint('album id: ')
        pprint(albumid)

        pprint('datesplit: ')
        pprint(albumid.split('---')[1])

        for item in item_select({'tab': 'album','album': albumid.split('---')[0], 'date': albumid.split('---')[1]})['namematch']:
            #only one expected result
            base = AlbumID3(item)

        base['song'] = []

        myresult = item_select({'album': albumid.split('---')[0], 'tab': 'track'})

        for item in myresult['namematch']:
            base['song'].append(Child(item))

        return base

    #boiler
    def albuminfo():
        base = {
            "notes": "Download the full release here (creative commons). These cripsy beats are ripe with thumping funk and techno influences, sample wizardry and daring shuffles. Composed with the help of unique sound plugins which were especially programmed to measure Comfort Fit’s needs and wishes, we think the chances aren’t bad that you’ll fall for the unique sound signature, bounce and elegance of this unusual Hip Hop production. Ltj bukem / Good looking Rec., UK: \"Really love this music.\" Velanche / XLR8R, UK: \"Awesome job he's done... overall production is dope.\" Kwesi / BBE Music, UK: \"Wooooooowwwww... WHAT THE FUCK! THIS IS WHAT",
            "musicBrainzId": "6e1d48f7-717c-416e-af35-5d2454a13af2",
            "smallImageUrl": "http://localhost:8989/play/art/0f8c3cbd6b0b22c3b5402141351ac812/album/21/thumb34.jpg",
            "mediumImageUrl": "http://localhost:8989/play/art/41b16680dc1b3aaf5dfba24ddb6a1712/album/21/thumb64.jpg",
            "largeImageUrl": "http://localhost:8989/play/art/e6fd8d4e0d35c4436e56991892bfb27b/album/21/thumb174.jpg"
        }

        return base

    #boiler
    def albumList():
        base = {
            "album": [
                {
                "id": "200000021",
                "parent": "100000036",
                "album": "Forget and Remember",
                "title": "Forget and Remember",
                "name": "Forget and Remember",
                "isDir": true,
                "coverArt": "al-200000021",
                "created": "2017-04-11T10:42:50.842Z",
                "duration": 4248,
                "playCount": 0,
                "artistId": "100000036",
                "artist": "Comfort Fit",
                "year": 2005,
                "genre": "Hip-Hop"
                },
                {
                "id": "200000012",
                "parent": "100000019",
                "album": "Buried in Nausea",
                "title": "Buried in Nausea",
                "name": "Buried in Nausea",
                "isDir": true,
                "coverArt": "al-200000012",
                "created": "2017-04-11T10:42:50.842Z",
                "duration": 1879,
                "playCount": 0,
                "artistId": "100000019",
                "artist": "Various Artists",
                "year": 2012,
                "genre": "Punk"
                }
            ]
        }

    def albumList2(request):

        base = {
            'album': []
        }

        pprint(request.args['offset'])

        if request.args['offset'] == '0' or 'offset' not in request.args:

            filters = {'tab': 'album'}

            if request.values['type'] == 'byGenre':
                filters['genre'] = request.values['genre']

            myresult = item_select(filters)

            for item in myresult['namematch']:
                pprint(item['inode'])
                base['album'].append(AlbumID3(item))

        return base

    #boiler
    def artist():
        base = {
            "id": "100000002",
            "name": "Synthetic",
            "coverArt": "ar-100000002",
            "starred": "2021-02-22T05:54:18Z"
        }

        return base

    #boiler
    def ArtistID3():
        base = {
            "id": "37ec820ca7193e17040c98f7da7c4b51",
            "name": "2 Mello",
            "coverArt": "ar-37ec820ca7193e17040c98f7da7c4b51_0",
            "albumCount": 1,
            "userRating": 5,
            "artistImageUrl": "https://demo.org/image.jpg",
            "starred": "2017-04-11T10:42:50.842Z",
            "musicBrainzId": "189002e7-3285-4e2e-92a3-7f6c30d407a2",
            "sortName": "Mello (2)",
            "roles": [
                "artist",
                "albumartist",
                "composer"
            ]
        }

        return base

    #boiler
    def artistInfo(artistid):
        base = {
            "biography": "Empty biography",
            "musicBrainzId": "1",
            "smallImageUrl": "http://localhost:8989/play/art/f20070e8e11611cc53542a38801d60fa/artist/2/thumb34.jpg",
            "mediumImageUrl": "http://localhost:8989/play/art/2b9b6c057cd4bf21089ce7572e7792b6/artist/2/thumb64.jpg",
            "largeImageUrl": "http://localhost:8989/play/art/e18287c23a75e263b64c31b3d64c1944/artist/2/thumb174.jpg"
        }

        return base

    #boiler
    def artistInfo2():
        base = {
            "biography": "Empty biography",
            "musicBrainzId": "1",
            "smallImageUrl": "http://localhost:8989/play/art/f20070e8e11611cc53542a38801d60fa/artist/2/thumb34.jpg",
            "mediumImageUrl": "http://localhost:8989/play/art/2b9b6c057cd4bf21089ce7572e7792b6/artist/2/thumb64.jpg",
            "largeImageUrl": "http://localhost:8989/play/art/e18287c23a75e263b64c31b3d64c1944/artist/2/thumb174.jpg"
        }

        return base    

    #boiler
    def ArtistsID3():
        base = {
            "ignoredArticles": "The An A Die Das Ein Eine Les Le La",
            "index": [
                {
                "name": "C",
                "artist": [
                    {
                    "id": "100000016",
                    "name": "CARNÚN",
                    "coverArt": "ar-100000016",
                    "albumCount": 1
                    },
                    {
                    "id": "100000027",
                    "name": "Chi.Otic",
                    "coverArt": "ar-100000027",
                    "albumCount": 0
                    }
                ]
                },
                {
                "name": "I",
                "artist": [
                    {
                    "id": "100000013",
                    "name": "IOK-1",
                    "coverArt": "ar-100000013",
                    "albumCount": 1
                    }
                ]
                }
            ]
        }

        return base

    def ArtistWithAlbumsID3(request):

        base = {
            'artist': {}
        }

        for item in item_select({'id': request.args['id'], 'tab': 'artist'})['namematch']:
            base['artist'] = ArtistID3(item)

        base['artist']['album'] = []

        for item in item_select({'artist': request.args['id'], 'tab': 'album'})['namematch']:
            base['artist']['album'].append(AlbumID3(item)) #yeah from what I can see the album is embedded inside the artist

        return base

    def bookmark():
        base = {
            "entry": {
                "id": "113bf5989ad15ce2cf1834ba9622983f",
                "parent": "b87a936c682c49d4494c7ccb08c22d23",
                "isDir": False,
                "title": "Stay Out Here",
                "album": "Shaking The Habitual",
                "artist": "The Knife",
                "track": 11,
                "year": 2013,
                "genre": "Electronic",
                "coverArt": "al-b87a936c682c49d4494c7ccb08c22d23_0",
                "size": 21096309,
                "contentType": "audio/mp4",
                "suffix": "m4a",
                "duration": 642,
                "bitRate": 257,
                "bitDepth": 16,
                "samplingRate": 44100,
                "channelCount": 2,
                "path": "The Knife/Shaking The Habitual/11 - Stay Out Here.m4a",
                "created": "2023-03-13T16:30:35Z",
                "albumId": "b87a936c682c49d4494c7ccb08c22d23",
                "artistId": "b29e9a9d780cb0e133f3add5662771b9",
                "type": "music",
                "isVideo": False,
                "bookmarkPosition": 129000
            },
            "position": 129000,
            "username": "demo",
            "comment": "",
            "created": "2023-03-13T16:30:35Z",
            "changed": "2023-03-13T16:30:35Z"
        }

        return base
        
    def bookmarks():
        base = {
            'bookmark': [
                bookmark()
            ]
        }
        return base

    def ItemGenre(item):
        base = {
            'name': item['namedisplay']
        }

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
            pprint(item['namedisplay'])
            first_character = item['namedisplay'][0].upper()
            index_number = ascii_uppercase.index(first_character)
            base['index'][index_number]['artist'].append(artist_obj)

        return base

    def user(request):
        base = {
            "username": "drew",
            "email": "sindre@activeobjects.no",
            "scrobblingEnabled": "true",
            "adminRole": "true",
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

        try:
            searchvalue = request.args['query']
        except:
            return 'FAILURE'

        base = {
            'artist': [],
            'album': [],
            'song': []
        }

        pprint(request.args['artistOffset'])

        if request.args['artistOffset'] == '0' or 'artistOffset' not in request.args:
            for item in item_select({'tab': 'artist'})['namematch']:
                base['artist'].append(ArtistID3(item)) 

        if request.args['albumOffset'] == '0' or 'albumOffset' not in request.args:
            for item in item_select({'tab': 'album'})['namematch']:
                base['album'].append(AlbumID3(item))

        if request.args['songOffset'] == '0' or 'songOffset' not in request.args:
            for item in item_select({'tab': 'track', 'searchvalue': searchvalue})['namematch']:
                base['song'].append(Child(item))

        return base

    def song(request):
        myresult = item_select({'inode': request.args['id'], 'tab': 'track'})

        base = {}

        for item in myresult['namematch']:
            base = Child(item)

        if base == {}: #quick n dirty error checking, def not needed in reality
            for item in item_select({'inode': '562949953630815', 'tab': 'track'})['namematch']:
                base = Child(item)

        return base

    def songs():
        base = {'song': []}
        return base

    def songsByGenre(request):
        base = {'songsByGenre': songs()} #plural songs does not send an argument

        if request.args['offset'] == '0':
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

    def topSongs(request):

        base = songs()

        myresult = item_select({'artist': request.args['artist'], 'tab': 'track'})

        for item in myresult['namematch']:
            base['song'].append(Child(item))

        return base

    def artpath(artid):
        artpath = f"{os.getcwd()}/staticx/art/{artid}.jpg"

        if (pathlib.Path(artpath)).is_file():
            return artpath
        else:
            return 'deadpath'

    def Child(item):

        base = {
            'id': str(item['inode']),
            'parent': 'parentalbum',
            'isDir': False,
            'title': item['namedisplay'],
            'album': 'album temp',
            'artist': json.loads(item['artists_json'])[0],
            'track': 1,
            'year': 2001,
            'coverArt': str(item['artinode']),
            'size': item['size'],
            'contenttype': 'audio/mpeg',
            'suffix': item['streampath'].split('.')[-1],
            'starred': '2017-04-11T10:42:50.842Z',
            'duration': int(item['duration']),
            'bitRate': 444,
            'bitDepth': 0,
            'samplingRate': 0,
            'channelCount': 2,
            'path': 'path',
            'playCount': 0,
            'played': '2017-04-11T10:42:50.842Z',
            'discNumber': 1,
            'created': '2017-04-11T10:42:50.842Z',
            'albumId': '---',
            'artistId': 'artistidtemp',
            'type': 'music',
            'mediaType': 'song', #song/album/artist??
            'isVideo': False,
            'bpm': 0,
            'comment': 'Commentplaceholder',
            'sortName': item['namesort'],
            'musicBrainzId': 'musicbrainztemp',
            'isrc': [],
            'genres': [],
            'artists': [],
            'displayArtist': 'display artist',
            'albumArtists': [],
            'displayAlbumArtist': 'display album artist',
            'contributors': [],
            'displayComposer': 'display composer',
            'moods': [],
            'explicitStatus': 'explicit', #explicit/clean/""
            'replaygain': {},
            'works': [],
            'movements': [],
            'groupings': []
        }
        try:
            base['bpm'] = int(singularattribute(item['inode'], 'BPM'))
        except:
            pass

        for album in item_select({'inode': item['inode'], 'tab': 'album'})['namematch']:
            base['album'] = album['namedisplay']

        for genre in item_select({'inode': item['inode'], 'tab': 'genre'})['namematch']:
            base['genres'].append(ItemGenre(genre))

        for artist_return in item_select({'inode': item['inode'], 'tab': 'artist'})['namematch']:
            base['artists'].append(ArtistID3(artist_return))

        if len(base['artists']) < 2:
            base['artistId'] = base['artists'][0]['name']

        for albumreturn in item_select({'tab': 'album', 'inode': item['inode']})['namematch']:
            base['album'] = albumreturn['namedisplay']
            base['albumId'] = f'{albumreturn['namedisplay']}---{albumreturn['releasedate']}'

        return base

    def ArtistID3(item):
        base = {
            'whatami?': 'artistid3',
            'id': item['namedisplay'],
            'name': item['namedisplay'],
            'coverArt': str(item['artinode']),
            'albumCount': item['albumcount'],
            'userRating': 2,
            'artistImageUrl': '',
            'starred': '2017-04-11T10:42:50.842Z',
            'musicBrainzId': item['namedisplay'],
            'sortName': item['namesort'],
            'roles': []
        }

        return base

    match subsonic_endpoint.removesuffix('.view'):
        case 'addChatMessage':
            sub = {}
        case 'changePassword':
            sub = {}
        case 'createBookmark':
            sub = {}
        case 'createInternetRadioStation':
            sub = {}
        case 'createPlaylist':
            sub = {
                'playlist': playlist() #todo
            }
        case 'createPodcastChannel':
            sub = {}
        case 'createShare':
            sub = {
                'shares': shares() #todo
            }
        case 'createUser':
            sub = {}
        case 'deleteBookmark':
            sub = {}
        case 'deleteInternetRadio':
            sub = {}
        case 'deletePlaylist':
            sub = {}
        case 'deletePodcastchannel':
            sub = {}
        case 'deletePodcastEpisode':
            sub = {}
        case 'deleteShare':
            sub = {}
        case 'deleteUser':
            sub = {}
        case 'download':
            return stream_or_download(request, filesystem_path)
        case 'downloadPodcastEpisode':
            sub = {}
        case 'findSonicPath':
            sub = {
                'sonicMatch': sonicMatch() #todo
            }
        case 'getAlbum':
            sub = {
                'album': AlbumID3WithSongs(request.args['id'])
            }
        case 'getAlbumInfo':
            sub = {
                'albumInfo': albumInfo(request) #todo
            }
        #yes this is the same thing as getAlbumInfo on the site
        case 'getAlbumInfo2':
            sub = {
                'albumInfo': albumInfo(request) #todo
            }
        case 'getAlbumList':
            sub = {
                'albumList': albumList() #todo
            }
        case 'getAlbumList2':
            sub = {
                'albumList2': albumList2(request)
            }
        case 'getArtist':
            sub = ArtistWithAlbumsID3(request) #netlify website does not say this, but it shows it at https://opensubsonic.netlify.app/docs/endpoints/getartist/
        case 'getArtistInfo':
            sub = {
                'artistInfo': artistInfo(request.args['id'])
            }
        case 'getArtistInfo2':
            sub = {
                'artistInfo2': artistInfo2() #todo
            }
        case 'getArtists':
            sub = {
                'artists': artists()
            }
        case 'getAvatar':
            return xmlresponse #didnt built in returning a binary image yet
        case 'getBookmarks':
            sub = {
                'bookmarks': bookmarks()
            }
        #getcaptions
        case 'getChatMessages':
            sub = {
                'chatMessages': chatMessages() #todo
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
        case 'getGenres':
            sub = {
                'genres': genres()
            }
        case 'getIndexes':
            sub = {
                'indexes': indexes()
            }
        case 'getInternetRadioStations':
            sub = {
                'internetRadioStations': internetRadioStations()
            }
        case 'getLicense':
            sub = {
                'license': license()
            }
        case 'getLyrics':
            sub = {
                'lyrics': lyrics()
            }
        #omitted getLyricsBySongId
        case 'getMusicDirectory':
            sub = {
                'directory': directory()
            }
        case 'ping':
            if request.args['f'] == 'json':
                sub = {}
            else:
                return xmlresponse()
        case 'getOpenSubsonicExtensions':
            sub = {
                'openSubsonicExtensions': openSubsonicExtensions()
            }
        case 'getPlaylist':
            sub = {}
        case 'getPlaylists':
            sub = {
                'playlists': playlists()
            }
        case 'getStarred':
            sub = {
                'starred': starred()
            }
        case 'getStarred2':
            sub = {
                'starred2': starred2()
            }
        case 'getTopSongs':
            sub = {
                'topSongs': topSongs(request)
            }




        case 'getUser': #takes "username" argument
            sub = {
                'user': user(request)
            }





        case 'search3':
            sub = {
                'searchResult3': searchResult3(request)
            }

        case 'getSongsByGenre':
            sub = songsByGenre(request)

        case 'getRandomSongs':
            sub = randomSongs(request)





        case 'getSong':
            sub = {
                'song': song(request)
            }



        case 'stream':
            return stream_or_download(request, filesystem_path)

        case 'art2':
            '''
            f = taglib.File(r'D:\data\music\scan\public\_sync\a_\4 Lit _ B.o.B; T.I._Ty Dolla $ign.mp3')

            pic_binary_data = f.pictures[0].data

            return Response(pic_binary_data, mimetype='image/jpeg')
            '''

            return 'hi'
    
        case _: #default case
            return {}

    sub['status'] = 'ok'
    sub['version'] = '1.16.1'
    sub['type'] = "Tarantula (OpenSubsonic)"
    sub['serverVersion'] = '0.0.1'
    sub['openSubsonic'] = True

    return { #make this a class?????
        "subsonic-response": sub
    }
        