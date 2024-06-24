from BaseHTTPServer import BaseHTTPRequestHandler
import SocketServer as socketserver
import textwrap
import json

index = """
<html>
	<head>
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@0,200..900;1,200..900&display=swap" rel="stylesheet">

		<style>

			body{
			  margin: 0px;
			  border: 0px;
			  padding: 0px;
			  position: absolute;
			  background-color: #020611;
			  color: #ffffff;
			}

			#text {
			  font-family: "Source Code Pro", monospace;
			  font-optical-sizing: 20px;
			  font-weight: 400;
			  font-style: normal;
			  text-align:center;
			  line-height: 12px;
			}
		</style>
	</head>
	<body>
		<pre id='text'>hello world</pre>
	</body>


</html>
<script>

function resize(){
var width = window.innerWidth;
var height = window.innerHeight;

var text = document.getElementById('text');
text.innerHTML = '#'.repeat(Math.floor(width/10));
text.innerHTML += ("\\n"+"#" + ' '.repeat(Math.floor(width/10 - 2)) + "#").repeat(Math.floor(height/12-2));
text.innerHTML += '\\n' + '#'.repeat(Math.floor(width/10));
}

window.addEventListener("resize", (x) => {resize(); askQuestion(); drawTitle();});
window.addEventListener("load", (x) => {resize(); askQuestion(); drawTitle();});
window.addEventListener("keydown", input);


resize();

function insert(string, substring, start){
	var tempString = 
		string.substring(0,start) + 
		substring + 
		string.substring(start + substring.length, string.length);
	return tempString;
}

function drawTitle(){

var width = window.innerWidth;
var height = window.innerHeight;
var text = document.getElementById('text');

var title = [
"|    ______  ____ _______         __      __  ____   ______ |",
"|   / __  / / __//__  __/        / / __  / / / __/  / /_  / |",
"|  / /_/ / / __/   / /          / / / / / / / __/  / __  /  |",
"| / ____/ / /__   / /          / /_/ /_/ / / /__  / /__ /   |",
"|/_/     /____/  /_/          /_________/ /____/ /_____/    |"
];


var position = (x,y) => y*(Math.floor(width/10)+1)+x;

var temp = title.map(
	(a, i) => {text.innerHTML = insert(text.innerHTML,a,position(Math.floor(width/20)-30,i+4)); return '';}
	);

if(width < 615){
text.innerHTML = "please resize window to fit content. Or switch to a device with a bigger screen, preferably a computer with a html5 capable browser.";
}

}

var state = 0;
var latitude = 0;
var longitude = 0;
var pet = 0;

function askQuestion(){

var width = window.innerWidth;
var height = window.innerHeight;
var text = document.getElementById('text');
var position = (x,y) => y*(Math.floor(width/10)+1)+x;

switch(state){
	case 0:
		text.innerHTML = insert(text.innerHTML, "to register a pet press p,", position(Math.floor(width/20)-18,Math.floor(height/24)));
		text.innerHTML = insert(text.innerHTML, "to browse pets press b", position(Math.floor(width/20)-16,Math.floor(height/24)+2));
		break;
	case 1:
		pet = "1";
		text.innerHTML = insert(text.innerHTML, "what is the pets name", position(Math.floor(width/20)-10,Math.floor(height/24)));
		text.innerHTML = insert(text.innerHTML, textInput, position(Math.floor(width/20-textInput.length/2),Math.floor(height/24)+2));
		break;
	case 3:
		text.innerHTML = insert(text.innerHTML, "please turn on location settings", position(Math.floor(width/20)-16,Math.floor(height/24)));
		text.innerHTML = insert(text.innerHTML, "(press enter to continue)", position(Math.floor(width/20)-12,Math.floor(height/24)+2));
		navigator.geolocation.getCurrentPosition((position) => {
		    let lat = position.coords.latitude;
		    let long = position.coords.longitude;

		    latitude = lat;
		    longitude = long;
		  });
		break;
	case 2:
		pet = "0";
		text.innerHTML = insert(text.innerHTML, "please turn on location settings", position(Math.floor(width/20)-16,Math.floor(height/24)));
		text.innerHTML = insert(text.innerHTML, "(press enter to continue)", position(Math.floor(width/20)-12,Math.floor(height/24)+2));
		navigator.geolocation.getCurrentPosition((position) => {
		    let lat = position.coords.latitude;
		    let long = position.coords.longitude;

		    latitude = lat;
		    longitude = long;
		  });
		break;
	case 4:
		text.innerHTML = insert(text.innerHTML, "what is the pets email", position(Math.floor(width/20)-10,Math.floor(height/24)));
		text.innerHTML = insert(text.innerHTML, textInput, position(Math.floor(width/20-textInput.length/2),Math.floor(height/24)+2));
		break;
}
}

var textInput ='';
var name ='';
var email ='';

var blankString='';

function input(e){
var width = window.innerWidth;
var height = window.innerHeight;
var text = document.getElementById('text');
var position = (x,y) => y*(Math.floor(width/10)+1)+x;

switch(state){
	case 0:
		console.log(e.key);
		if(e.key=="p"){
			state = 1;
		}
		if(e.key=="b"){
			state = 2;
		}
		textInput ='';
		resize(); askQuestion(); drawTitle();
		break;
	case 1:
		if(e.key=="Backspace"){
			textInput = textInput.substring(0, textInput.length - 1);
			resize(); askQuestion(); drawTitle();
		} else {
			if(e.key=="Shift"){
				
			} else {
				if(e.key=="Enter"){
					name = textInput;
					textInput = '';
					state = 4;
					resize(); askQuestion(); drawTitle();
				} else {
					textInput += e.key;
				}
			}
		}
		console.log(textInput);
		text.innerHTML = insert(text.innerHTML, textInput, position(Math.floor(width/20-textInput.length/2),Math.floor(height/24)+2));
		break;
	case 2:
		pet = 0;
		if(e.key=="Enter"){
			state = 0;
			resize(); askQuestion(); drawTitle();
			window.location.href = 'http://localhost:8000/?data='+encode(
				""+pet+
				String.fromCharCode(30)+
				longitude+
				String.fromCharCode(30)+
				latitude
			);		}
		break;
	case 3:
		if(e.key=="Enter"){
			state = 0;
			resize(); askQuestion(); drawTitle();
			window.location.href = 'http://localhost:8000/?data='+encode(
				""+pet +
				String.fromCharCode(30)+
				name+String.fromCharCode(30)+
				longitude+
				String.fromCharCode(30)+
				latitude+
				String.fromCharCode(30)+
				email
			);
		}
		break;
	case 4:
		if(e.key=="Backspace"){
			textInput = textInput.substring(0, textInput.length - 1);
			resize(); askQuestion(); drawTitle();
		} else {
			if(e.key=="Shift"){
				
			} else {
			if(e.key=="Enter"){
				email = textInput;
				textInput = '';
				state = 3;
				resize(); askQuestion(); drawTitle();
			} else {
			textInput += e.key;
			}
			}
		}
		console.log(textInput);
		text.innerHTML = insert(text.innerHTML, textInput, position(Math.floor(width/20-textInput.length/2),Math.floor(height/24)+2));
		break;
}
}

function encode(a){
var tempString = '';
for(let i = 0; i < a.length; i++){
	tempString += a.charCodeAt(i).toString(16);	
}
return tempString;
}


</script>
"""

petPage = """
<html><head>
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
		<link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@0,200..900;1,200..900&amp;display=swap" rel="stylesheet">

		<style>

			body{
			  margin: 0px;
			  border: 0px;
			  padding: 20px;
			  position: absolute;
			  background-color: #020611;
			  color: #ffffff;
			}

			#text {
			  font-family: "Source Code Pro", monospace;
			  font-optical-sizing: 20px;
			  font-weight: 400;
			  font-style: normal;
			  text-align:left;
			  line-height: 25px;
			}
			
			#link {
			  color: #0000ff;
			}
		</style>
	</head>
	<body>
		<div id="text">

		</div>	



<script>
var index = 1;

window.addEventListener("load", main);
window.addEventListener("keydown", input);

var pets=[
doogad
];


function highlight(){
	for(let I = 1; I < pets.length+1; I++){
		document.getElementById("a"+I.toString()).style.backgroundColor = "rgba(0.0,0.0,0.0,0.0)";
		document.getElementById("a"+I.toString()).style.color = "#ffffff";
		document.getElementById("b"+I.toString()).style.display = "none";
	}
	document.getElementById("a"+index.toString()).style.backgroundColor = "#ffffff";
	document.getElementById("a"+index.toString()).style.color = "rgb(0,0,0)";
	document.getElementById("b"+index.toString()).style.display = "inline";
}

function input(e){
	if(e.code == "ArrowDown" && index<pets.length){
		index++;
	}
	if(e.code == "ArrowUp"&& index > 1){
		index--;
	}
	highlight();
}

function main(){
	for(let i = 0; i < pets.length; i++){
	console.log('<div id="a'+(i+1)+'"><div>'+pets[i][0]+'</div></div>');
	document.getElementById('text').innerHTML += '<div id="a'+(i+1)+'"><span>'+pets[i][0]+'</span><span id="b'+(i+1)+'">'+'  '+pets[i][1]+'</span></div>';
	}
	document.getElementById('text').innerHTML += '<a id="link">Back to home page</a>';
	document.getElementById("link").href = window.location.href.split("?")[0];
	highlight();
}

</script></body></html>
"""

submitPet = """
<head>
		<style>

			body{
			  margin: 0px;
			  border: 0px;
			  padding: 20px;
			  position: absolute;
			  background-color: #020611;
			  color: #ffffff;
			}

			#text {
			  font-family: "Source Code Pro", monospace;
			  font-optical-sizing: 20px;
			  font-weight: 400;
			  font-style: normal;
			  text-align:left;
			  line-height: 25px;
			}
		</style>
</head>
<body>
	<pre id="text">
		tank you for uploading your pet, you will receive an email regarding our pet if anyone takes interest in it.

			<a id="link">Back to home page</a><script> document.getElementById("link").href = window.location.href.split("?")[0];</script>
	</pre>
</body>
"""

pets = []

class Pet:
	def __init__(self, name, email, x, y):
		self.name = name
		self.email = email
		self.x = x
		self.y = y

def arrayToPet(array):
	return Pet(array[1],array[4],array[2],array[3])

def sortPets(x, y):
	global pets
	return pets.sort(key = lambda a : int((float(a['x'])-x)*(float(a['x'])-x) + (float(a['y'])-y)*(float(a['y'])-y)))

def saveFile():
	global pets
	f = open("save.txt", "w")
	f.write(json.dumps(pets))
	f.close()

def loadFile():
	global pets
	f = open("save.txt", "r")
	pets = json.loads(f.read())

def decode(a):
	return (''.join(chr(i) for i in map(lambda x : int(x,16), textwrap.wrap(a[7:],2)))).split(chr(30))

PORT = 8000

class handler(BaseHTTPRequestHandler):
	def do_GET(self):
		global pets
		loadFile()
		print(pets[0])
		if self.path == '/':
			self.send_response(200)
        		self.send_header("Set-Cookie", "foo=bar")
			self.send_header("text/html", "charset=utf-8")
        		self.end_headers()
			self.wfile.write(bytes(index).encode("utf-8"))
		else:
			array = decode(self.path)
			if array[0] == '1':
				loadFile()
				print(pets)
				pets.append(vars(arrayToPet(array)))
				print(pets)
				saveFile()
				self.send_response(200)
        			self.send_header("Set-Cookie", "foo=bar")
				self.send_header("text/html", "charset=utf-8")
        			self.end_headers()
				self.wfile.write(bytes(submitPet).encode("utf-8"))
			elif array[0] == '0':
				loadFile()
				self.send_response(200)
        			self.send_header("Set-Cookie", "foo=bar")
				self.send_header("text/html", "charset=utf-8")
        			self.end_headers()
				sortPets(0,0)
				self.wfile.write(bytes(petPage.replace("doogad",",".join(map(lambda x: "['"+x["name"]+"','"+x["email"]+"']", pets[:20])))).encode("utf-8"))




httpd = socketserver.TCPServer(("", PORT), handler)
print("serving at port", PORT)
httpd.serve_forever()