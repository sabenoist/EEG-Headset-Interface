function start_streaming() {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("GET", "127.0.0.1:5000/start_streaming", false);
	xmlHttp.send(null);

	window.alert("started streaming!")
}

function stop_streaming() {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("GET", "127.0.0.1:5000/stop_streaming", false);
	xmlHttp.send(null);

	window.alert("stopped streaming!")
}