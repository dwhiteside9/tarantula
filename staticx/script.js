/*
$(function() { //on load, fill the wrapper div with html that can be received through the "/home" endpoint
    $.post(
		"/home",
		(data) => {
			//console.log(data);
			$("#wrapper").html(data);
            console.log('Filling #wrapper with data on first load of page')
		}
	);
});
*/


/* for visual purposes only 

function addselectedclass(){
	$(document).find('nav a').removeClass('selected')
	var selectedtab = $(document).find("nav a[hx-post='" + location.pathname + "']");
	selectedtab.addClass('selected');
}

$(function() {
	
	// runs any time history changes - back/forward button, etc
	window.onpopstate = function () {
		addselectedclass();
	}
});

//runs on first page load
window.onload = function () {
	addselectedclass();
}

$(document).on('click', 'nav a', function() {
	var panel = $(this).closest('nav');
	panel.find('a').removeClass('selected');
	$(this).addClass('selected');
});

 END for visual purposes only */



$(function() {
	//auto-clicking an input that SHOULD be selected and comes in technically as selected, but does not visually show, and the text input box also can't see unless this command is run
	checked_element = document.querySelector("[checked='']")
	if (checked_element != null) {
		checked_element.click()
		console.log('clicked the checked element')
	}
})

function focusthesearchbar () {
	document.querySelector("#searchbar").focus()
}

var accentcolor = window.getComputedStyle(document.body).getPropertyValue('--accentcolor')
var bgcolor = window.getComputedStyle(document.body).getPropertyValue('--bgcolor')

// Create a canvas gradient
const ctx = document.createElement('canvas').getContext('2d')
const gradient = ctx.createLinearGradient(0, 0, 0, 150)
//https://stackoverflow.com/questions/41725725/access-css-variable-from-javascript
gradient.addColorStop(0, accentcolor)
gradient.addColorStop(0.8, 'rgb(100, 0, 100)')
gradient.addColorStop(1, 'rgb(0, 0, 0)')

var wavesurfer = {}
var needtodestroy = 'no'

function wavesurf(filepath) {

	currentaudio = document.querySelector(`video[src='${filepath}']`) //needs to be no space between "audio" and "["
	currentaudio.play()

	if (needtodestroy == 'yes'){
		wavesurfer.destroy()
	}

	//maybe add some .thens to make it not pop on mobile?

	wavesurfer = WaveSurfer.create({
		container: '#waveform',
		waveColor: 'gray',
		progressColor: accentcolor,
		cursorWidth: 0,
		//cursorColor: 'rgb(25,25,25)', //inherits progresscolor
		barWidth: 0,
		mediaControls: false,
		backend: 'MediaElement', //WebAudio //MediaElement
		media: currentaudio,
		//peaks: [],
	})

	needtodestroy = 'yes'

	//old method, had lag bc it had to generate the waveform before playing the audio
	/*
	wavesurfer.load(filepath).then(
		function(){
			wavesurfer.play()
		}
	)*/
}

function showbar() {
	document.getElementById('waveformcontainer').style.display = 'grid' //going frome none to grid
}

function visualtoggleplaybutton() {
	button_element = document.querySelector('#playbutton')

	if (button_element.innerText == '⏸️') {
		button_element.innerHTML = '▶️'
	}
	else {
		button_element.innerHTML = '⏸️'
	}
}

//https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/key
document.addEventListener("keydown", (e) => {
	if (e.key == 'ArrowUp') { //or ArrowRight
		console.log(`Key "${e.key}" released [event: keyup]`)
		focusthesearchbar()
	}

	if (e.key == ' ') { //spacebar
		
		//https://stackoverflow.com/questions/36430561/how-can-i-check-if-my-element-id-has-focus
		if (document.activeElement != document.querySelector('#searchbar')) {
			e.preventDefault(); // to stop from scrolling page down. https://www.jankollars.com/posts/preventing-space-scrolling/
			video_element = document.querySelector('#hiddenaudio')
			if (video_element != null) {
				wavesurfer.playPause();
				/*
				if (video_element.paused) {
					video_element.play()
				}
				else {
					video_element.pause()
				}*/
			}

		}
	}
  
});


if (window.location.href.includes('localhost')) {
	//https://www.w3schools.com/howto/howto_js_redirect_webpage.asp
	// Becase localhost has latency for some reason!!!!!
	//https://stackoverflow.com/questions/38944323/google-chrome-http-get-on-localhost-inconsistent-load-times
	//https://stackoverflow.com/questions/77496046/why-is-my-own-webserver-slow-with-chrome-fast-with-firefox-initial-connection
	window.location.replace(window.location.href.replace('localhost', '127.0.0.1'));
}