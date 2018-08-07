function start_streaming() {
	$.get("127.0.0.1:5000/start_streaming")
	window.alert("started streaming!")
}

function stop_streaming() {
	$.get("127.0.0.1:5000/stop_streaming")
	window.alert("stopped streaming!")
}