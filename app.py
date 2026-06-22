from flask import Flask, send_from_directory, redirect, render_template, request, url_for, make_response, Response, send_file, g
import pathlib
from pprint import pprint
import tomllib
from actions import * #actions.py
from subsonic import * #subsonic.py
import webview
import subprocess
import time
import re
import urllib.parse #https://stackoverflow.com/questions/5607551/how-to-urlencode-a-querystring-in-python


commonsorts = ['name', 'modified', 'releasedate', 'size']
directions = ['desc', 'asc']

navitems = {
    'artist': commonsorts + ['filecount', 'albumcount'],
    'album': commonsorts + ['filecount'],
    'track': commonsorts,
    'genre': commonsorts + ['filecount', 'albumcount'],
}

navitemorder = ['artist', 'album', 'track', 'genre']

iconstemp = {
    'album': '💿',
    'artist': '🧍',
    'artists': '🧍',
    'track': '🎼',
    'genre':'🎶',
    'modified':'⌛',
    'name':'📜',
    'size':'📦',
    'filecount':'📁',
    'albumcount':'💿',
    'releasedate': '🏁',
    'x': '❎',
    'uparrow': '🔼',
    'downarrow': '🔽',
    'empty': '📪',
    'upright': '🔗',
}

icons = {}

defined_sortcolor = 'purple'

for icon in iconstemp.keys():
    icons[icon] = f"<span class=noto>{iconstemp[icon]}</span>"

#stub_url = 'https://static.vecteezy.com/system/resources/previews/005/720/408/original/crossed-image-icon-picture-not-available-delete-picture-symbol-free-vector.jpg'

def navhtml(tab, sort, direction, searchvalue):

    innerdivs = ''
    for navitem in navitems.keys():
    
        if sort in navitems[navitem]:
            moldedsort = sort
            moldeddirection = direction
            asterisk = ''
        else:
            moldedsort = commonsorts[0]
            moldeddirection = directions[0]
            asterisk = f"<span style='font-size:15px;color:gray;'>{icons[commonsorts[0]]}</span>" #to notify that if you choose this item to view, then the way things are sorted will not align with how the current page is sorted

        if tab == navitem:
            selected_status = 'selected'
            hx_trigger = '' #every 5s?
        else:
            selected_status = 'notselected'
            hx_trigger = 'click'

        innerdivs += f'''<div class='{selected_status}' hx-push-url='true' hx-post='/tab/{navitem}/{moldedsort}/{moldeddirection}?s={urllib.parse.quote_plus(searchvalue)}' hx-target='#everythingb4audio' hx-trigger='{hx_trigger}'>
        {asterisk}
        {icons[navitem]}
        <span class=hideshrink>{navitem.upper()}</span>'''
        #innerdivs += "<img class='htmx-indicator' src='/ball-triangle.svg' alt='Loading...'>"
        innerdivs += "</div>"

    return innerdivs

def radiobuttonhtml(sort, direction, tab):

    myhtml = '''<div class='flexcontainer nav' style='z-index:1'>'''

    sortmethods = navitems[tab]

    for sortmethod in sortmethods:
        if sortmethod == sort:
            selected_status = 'selected'
            #direction, NOT futuredirection because it's the current state of the page and HIDDEN
            #for some reason, putting text here will still show up even when display:none is activated
            myhtml += f'''<input style='display:none' checked='' type='radio' class='inputguy' name='sortinfo' value='{sortmethod}--{direction}'></input>'''
            if direction == 'asc':
                arrow = icons['uparrow']
                futuredirection = 'desc'
            elif direction == 'desc':
                arrow = icons['downarrow']
                futuredirection = 'asc'
        else:
            selected_status = 'notselected'
            arrow = ''
            futuredirection = 'desc'

        arrow = f"<span style='color:{defined_sortcolor};'>{arrow}</span>"

        #the name= part is the most important!!!
        #GOLD: https://stackoverflow.com/questions/77932229/htmx-active-search-with-multiple-input-sources
        method_direction_id = f'{sortmethod}--{futuredirection}'
        myhtml += f'''<input style='display:none' type='radio' class='inputguy' name='sortinfo' value='{method_direction_id}' id='{method_direction_id}'></input>
        <div class='{selected_status}' onclick="document.querySelector('input#{method_direction_id}').click()">
        {arrow}
        {icons[sortmethod]}
        <span class=hideshrink>{sortmethod.upper()}</span>
        </div>'''

    myhtml += '</div>'

    return myhtml

def singular_art_image(inode, extras, source):
    constructedpath = f"{os.getcwd()}/.art/{inode}.jpg"

    if pathlib.Path(constructedpath).is_file():

        imgurl = f"/art/{inode}.jpg"

        return f"<img decoding='async' loading='lazy' style='vertical-align:middle' src='{imgurl}' alt='' {extras}></img>"

    else:
        if source == 'bigtable':
            return ''
        else:
            return f"<div style='border:2px dotted gray;width:120px;'>No art</div>"
    

def htmlblocks(mydict, sort, direction, searchvalue, tab):

    myhtml = ''

    colorcounter = 1
    for item in mydict:

        #id values must not start with a number, hence them beginning with an '_'
        #https://stackoverflow.com/questions/2340319/python-3-string-to-hex
        id_value = f'_{item['namedisplay'].encode("utf-8").hex()}'

        #multiplier = int ( 8 * ( colorcounter/len(mydict) ) * (256 / len(mydict)) )
        #bgcolor = f'rgb(10,{multiplier},{multiplier}'
        bgcolor = 'black'

        def cooldisplay(searchvalue, db_direct_value):

            if searchvalue != '':
                cooldisplay = ''

                def capchecker(character, counter): #checks for difference in capitalization OR an accented character
                    if db_direct_value[counter] != character: #the character variable will be the "unidecoded" one from the forloop below
                        return db_direct_value[counter]
                    else:
                        return character

                db_direct_value = db_direct_value.replace('©', '(c)') #because the unidecode turns it into 3 characters instead of 1, so it throws off the numbers in the capchecker loop

                split_display = unidecode(db_direct_value).lower().split(searchvalue.lower())

                counter = 0
                firstloop = True
                for subpart in split_display:
                    if not firstloop:
                        cooldisplay += "<span style=color:var(--accentcolor);text-decoration:underline;>"
                        
                        for character in searchvalue:
                            cooldisplay += capchecker(character, counter)
                            counter += 1
                        
                        cooldisplay += "</span>"

                    for character in subpart:
                        cooldisplay += capchecker(character, counter)
                        counter += 1
                    if firstloop:
                        firstloop = False
                return cooldisplay
            else:
                return db_direct_value

        notospan = "<span style=color:gray>"

        myhtml += f'''<tr 
        style='white-space:nowrap;background:{bgcolor};'>'''
        
        myhtml += "<td style='padding-bottom:5px;text-align:center;'>" #padding bottom to get it to visually actually align vertically            

        inodes_used_in_html = []

        if item['artinode'] is not None:
            for artinode in item['artinode'].split(','):
                if artinode not in inodes_used_in_html:
                    myhtml += singular_art_image(inode=artinode, extras='', source='bigtable')
                inodes_used_in_html.append(artinode)
        else:
            myhtml += "<div style='height:20px;'>?</div>" #No art

        myhtml += "</td>"

        if sort == 'name':
            iconcolor = defined_sortcolor
        else:
            iconcolor = ''        
        
        myhtml += f'''<td hx-post='/oneitem/{tab}/{urllib.parse.quote_plus(item['namedisplay'])}' hx-target='#everythingb4audio' hx-push-url='true' class=namecell
        style='width:30%;font-weight:bold;'>
        <span style='color:{iconcolor}'>{icons[tab]}</span>{cooldisplay(searchvalue, item['namedisplay'])}'''

        td_html = "<td class=hideshrink style='width:30%;white-space:nowrap;'>"

        rest_of_columns = ''

        if 'artists_json' in item.keys() and tab in ['album', 'track']:
            rest_of_columns += f"{td_html} {icons['artists']} {splitartists(mylist=json.loads(item['artists_json']), itemtype='artist')} </td>"

        modified_int = item['modified']
        modified_readable = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(modified_int)) #time.gmtime for gmt

        size_rounded = str(round(item['size']/1000000, 2)) + " MB"

        for navitem in navitems[tab]:

            if navitem != 'name':

                shown_value = item[navitem]

                if navitem == 'modified':
                    shown_value = modified_readable
                if navitem == 'size':
                    shown_value = size_rounded
                if navitem == 'albumcount':
                    shown_value = str(shown_value) + " album(s)"

                if navitem == sort:
                    iconcolor = defined_sortcolor
                else:
                    iconcolor = ''

                rest_of_columns += f"{td_html}<span style='color:{iconcolor}'>{icons[navitem]}</span>{shown_value}</td>"

        onlysortvalue = ''
        if sort != 'name':
            onlysortvalue += f"{notospan}{icons[sort]}</span>"

        match sort:
            case 'filecount':
                onlysortvalue += str(item['filecount'])
            case 'modified':
                onlysortvalue += modified_readable
            case 'size':
                onlysortvalue += size_rounded
            case 'releasedate':
                onlysortvalue += str(item['releasedate'])
            case 'albumcount':
                onlysortvalue += str(item['albumcount']) + " album(s)"

        myhtml += f"<span class=showshrink><br>{onlysortvalue}</span></td>"
        myhtml += rest_of_columns
        myhtml += f'''</tr>'''

        if tab == 'track' and 'parseme' in item.keys():
            myhtml += f'''<tr><td colspan=100 style='width:30%'>'''
            myhtml += "<span style=font-size:10px>"

            pprint(item['parseme'])

            for key in json.loads(item['parseme']).keys():
                myhtml += key + ': '
                myhtml += cooldisplay(searchvalue, json.loads(item['parseme'])[key])
                myhtml += "<br>"
            myhtml += "</span>"
        
            myhtml += f'''</td></tr>'''
        
        colorcounter += 1
        #{item['allpaths']}

    return myhtml

def tabhtml(sort, direction, searchvalue, tab):

    myhtml = ''

    mydict = item_select({
        'sortby': sort,
        'direction': direction,
        'searchvalue': searchvalue,
        'tab': tab
    })

    if len(mydict['namematch']) + len(mydict['anymatch']) == 0:
        myhtml += f"<span style='font-size:20px;'>{icons['empty']} No results </span>"
    else:
        myhtml += "<table>"
        myhtml += htmlblocks(mydict['namematch'], sort, direction, searchvalue, tab)

        if tab == 'track' and mydict['anymatch'] != []:
            
            myhtml += '<tr><td colspan=100 style=text-align:center;height:50px;><i>Fuzzy results</i></td></tr>'
            myhtml += htmlblocks(mydict['anymatch'], sort, direction, searchvalue, tab)
        
        myhtml += "</table>"

    return myhtml

def fullpage_link(item, itemtype):
    return f"<a href='/oneitem/{itemtype}/{item}' hx-post='/oneitem/{itemtype}/{item}' hx-target='#everythingb4audio' hx-push-url='true'>{item}</a>"

def splitartists(mylist, itemtype):
    myhtml = ''
    firstitem = True
    for item in mylist:
        if not firstitem:
            myhtml += ", "
        if firstitem:
            firstitem = False

        myhtml += fullpage_link(item, itemtype)

    return myhtml

def create_app():

    static_folder_name = 'static'
    myapp = Flask(
        __name__, 
        static_folder = static_folder_name, #https://youtu.be/9At5sg-jPpU?list=PL7yh-TELLS1EyAye_UMnlsTGKxg8uatkM&t=125
        static_url_path = '/',
        template_folder = 'templates'
    )

    myapp.config.from_file("config.toml", load=tomllib.load, text=False) #https://flask.palletsprojects.com/en/stable/config/

    with myapp.app_context():
        g.static_folder_name = static_folder_name
        dbscan(myapp) #also includes the dbcreate

    #https://pythongeeks.org/redirect-errors-flask/
    @myapp.errorhandler(404)
    def incorrectpage(error):
        print('INVALID URL')
        #return redirect(url_for('index'))

    @myapp.route('/', methods = ['GET'])
    def index():
        return redirect(f"/tab/{navitemorder[0]}/{commonsorts[0]}/{directions[0]}?s=")

    @myapp.route('/playmedia', methods=['POST']) #importing the media path via hx-vals as well
    def playmedia():

        myhtml = ''

        stream_rest_path = request.values['stream_rest_path']

        try:
            if request.values['extension'].removeprefix('.') in ['mp4', 'mkv']:
                controls_or_not = 'controls'
                videowidth = 'auto'
                imghtml = ''
            else:
                controls_or_not = ''
                videowidth = 0
                imghtml = singular_art_image(inode=request.values['artinode'], extras=f"id=nowplayingart height=128", source='playbar')
            
            myhtml += f'''<video style='height:128px;' {controls_or_not} width={videowidth} id=hiddenaudio src="{stream_rest_path}" onloadstart="wavesurf('{stream_rest_path}')" onpause='visualtoggleplaybutton();' onplay='visualtoggleplaybutton();'></video>''' #remove "controls" to make audio hidden

            myhtml += imghtml

        except KeyError:
            pass

        return myhtml

    @myapp.route('/nothing', methods=['POST'])
    def nothing():
        return ''

    @myapp.route('/artist/<id>', methods=['POST'])
    def artist(id):
        return id

    @myapp.route('/album/<id>', methods=['POST'])
    def album(id):
        return id

    @myapp.route('/genre/<id>', methods=['POST'])
    def genre(id):
        return id

    @myapp.route('/track/<id>', methods=['POST'])
    def track(id):
        return id

    @myapp.route('/oneitem/<tab>/<path:itemid>', methods=['GET', 'POST']) #using path: is what makes it actually escape a slash such as in Rap/Hiphop
    def oneitem(tab, itemid):

        myhtml = f"<a href='/' hx-post='/tab/{navitemorder[0]}/{commonsorts[0]}/{directions[0]}?s=' hx-push-url='true' hx-target='#everythingb4audio'>Home</a><br><br>"

        itemid = urllib.parse.unquote_plus(itemid)

        myresult = getone(tab, itemid)

        myhtml += f"<button hx-post='/nothing' hx-target='#_{itemid.encode("utf-8").hex()}' hx-swap='innerHTML'>X</button><br>"

        for result in myresult:

            streampath = result['streampath'].removesuffix('.tag')
            fileextension = pathlib.Path(streampath).suffix
            
            inode = result['inode']

            stream_rest_path = f'/rest/stream?id={inode}'

            myhtml += f'''<div class=buttonesque hx-post="/playmedia" hx-vals='{{"stream_rest_path":"{stream_rest_path}", "inode":"{inode}", "artinode":"{result['artinode']}", "extension":"{fileextension}"}}' hx-target='#video_and_art' onclick=showbar();>{result['title']}</div>'''

            myhtml += icons['artist']

            myhtml += splitartists(mylist=json.loads(result['artists']), itemtype='artist')
            myhtml += '<br>'

        match request.method:
            case 'GET':
                return render_template('index.html', myhtml=myhtml)
            case 'POST':
                return myhtml

    @myapp.route('/tabdiv/<tab>', methods=['POST'])
    def artistdivroute(tab):

        #pprint(request.url_root)

        #https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
        if request.url_root == "http://127.0.0.1:5000/":
            #subprocess.Popen(r'explorer /select,"C:\mydata"')
            pass

        searchvalue = request.values['search'] #https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
        
        sort = request.values['sortinfo'].split('--')[0]
        direction = request.values['sortinfo'].split('--')[1]

        htmlpartofresponse = ''
        htmlpartofresponse += f'''<div id=topnav hx-swap-oob='true' class='flexcontainer nav' style='z-index:2'>{navhtml(tab, sort, direction, searchvalue)}</div>'''
        htmlpartofresponse += f'''<div id="radiobuttons" hx-swap-oob="true">{radiobuttonhtml(sort, direction, tab)}</div>'''
        htmlpartofresponse += tabhtml(sort, direction, searchvalue, tab)

        #https://stackoverflow.com/a/40211663
        myresponse = make_response(htmlpartofresponse)
        #https://stackoverflow.com/questions/76255150/htmx-push-url-with-form-value
        myresponse.headers['HX-Push-Url'] = f"/tab/{tab}/{sort}/{direction}?s={urllib.parse.quote_plus(searchvalue)}" #no slash before the ? is vital
        return myresponse

    @myapp.route('/tab/<tab>/<sort>/<direction>', methods = ['GET', 'POST'])
    def tab(tab, sort, direction):

        searchvalue = request.args['s']

        myhtml = f"<div id=topnav class='flexcontainer nav' style='z-index:2'>{navhtml(tab, sort, direction, searchvalue)}</div>"

        #so the keyboard does not popup repeatedly on mobile
        input_autofocus_status = ''
        onchange_action = ''
        if 'Mobile' not in request.headers['User-Agent']:
            input_autofocus_status = 'autofocus'
            onchange_action = 'focusthesearchbar();'
        else:
            input_autofocus_status = ''
            onchange_action = ''

        #.select() seems to not always work 
        # #for more specifics, can do "change from:input.inputguy"  
        # onchange="document.getElementById('searchbar').select()" got rid of this because the onfocusout on the actual input element seems to be better
        myhtml += f'''<form hx-post="/tabdiv/{tab}" hx-target='#tabdiv' hx-trigger="input changed delay:0ms throttle:0ms, click from:button#clear" id="artistform" onchange={onchange_action}>'''

        #https://stackoverflow.com/questions/5772124/input-value-doesnt-display-how-is-that-possible
        #https://stackoverflow.com/questions/511088/use-javascript-to-place-cursor-at-end-of-text-in-text-input-element specifically #https://stackoverflow.com/a/56719955
        #removed bc you can't highlight stuff now: onfocusout="document.getElementById('searchbar').focus()"
        myhtml += f'''<div style='display:flex;height:45px;margin:10px;gap:1px'>
        <input {input_autofocus_status} id=searchbar style='flex-grow:10' onfocus="this.setSelectionRange(-1, -1);" autocomplete="off" value="{searchvalue}" name="search" placeholder="Search..." style="height:100%;width:100%;">
        <button id=clear style='flex-grow:1;background:rgb(22,22,22);color:white;' onclick="document.getElementById('searchbar').value='';{onchange_action}">
        {icons['x']}
        </button>
        </div>
        '''

        myhtml += f'''<div id=radiobuttons style="align-items:center">{radiobuttonhtml(sort, direction, tab)}</div>''' #div id=radiobuttons will be replaced with the hx-swap-oob div from the artistdiv response
                  
        myhtml += "</form>"

        myhtml += f'''<br><div id=tabdiv>{tabhtml(sort, direction, searchvalue, tab)}</div>'''
        
        match request.method:
            case 'GET':
                return render_template('index.html', myhtml=myhtml)
            case 'POST':
                return myhtml

    #https://stackoverflow.com/questions/77569410/flask-possible-to-cache-images
    #resp.headers['Cache-Control'] = 'max-age'

    @myapp.route("/rest/<subsonic_endpoint>", methods=['GET', 'POST'])
    def subsonic(subsonic_endpoint): #any functions named in here cannot have the same name as "subsonic"
        subsonic_response = returnsubsonic(
            subsonic_endpoint=subsonic_endpoint, 
            static_folder_name=static_folder_name,
            filesystem_path=myapp.config['MEDIAPATH'],
        )
        return subsonic_response

    @myapp.route("/.well-known/appspecific/com.chrome.devtools.json", methods=['GET'])
    def shutup():
        return {}

    return myapp

if __name__ == "__main__":
    myapp = create_app()
    #https://stackoverflow.com/questions/9449101/how-to-stop-flask-from-initialising-twice-in-debug-mode #use_reloader=False
    myapp.run(host='0.0.0.0', port=myapp.config['PORT'], debug=True, use_reloader=True)


#c:/mydata/mypython/spiderflask/.venv/Scripts/Activate.ps1
#COMMAND: flask --app app --debug run 