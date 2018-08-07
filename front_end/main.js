function start_streaming() {
	$("#button_start").hide();
	$("#button_stop").show();

	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("GET", "http://127.0.0.1:5000/start_streaming", false);
	xmlHttp.send(null);
}

function stop_streaming() {
	$("#button_start").show();
	$("#button_stop").hide();

	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("GET", "http://127.0.0.1:5000/stop_streaming", false);
	xmlHttp.send(null);
}

function hide_stop_button() {
	$("#button_stop").hide();
}