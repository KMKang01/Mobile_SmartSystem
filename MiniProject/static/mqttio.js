let client = null; // MQTT 클라이언트의 역할을 하는 Client 객체를 가리키는 전역변수
let connectionFlag = false; // 연결 상태이면 true
const CLIENT_ID = "client-"+Math.floor((1+Math.random())*0x10000000000).toString(16) // 사용자 ID 랜덤 생성

function connect() { // 브로커에 접속하는 함수
	if(connectionFlag == true)
		return; // 현재 연결 상태이므로 다시 연결하지 않음

	// 사용자가 입력한 브로커의 IP 주소와 포트 번호 알아내기
	let broker = document.getElementById("broker").value; // 브로커의 IP 주소
	let port = 9001 // mosquitto를 웹소켓으로 접속할 포트 번호

	// id가 message인 DIV 객체에 브로커의 IP와 포트 번호 출력
	document.getElementById("messages").innerHTML += '<span>접속 : ' + broker + ' 포트 ' + port + '</span><br/>';
	document.getElementById("messages").innerHTML += '<span>사용자 ID : ' + CLIENT_ID + '</span><br/>';

	// MQTT 메시지 전송 기능을 모두 가징 Paho client 객체 생성
	client = new Paho.MQTT.Client(broker, Number(port), CLIENT_ID);

	// client 객체에 콜백 함수 등록 및 연결
	client.onConnectionLost = onConnectionLost; // 접속 끊김 시 onConnectLost() 실행 
	client.onMessageArrived = onMessageArrived; // 메시지 도착 시 onMessageArrived() 실행

	// client 객체에게 브로커에 접속 지시
	client.connect({
		onSuccess:onConnect, // 브로커로부터 접속 응답 시 onConnect() 실행
	});
}

// 브로커로의 접속이 성공할 때 호출되는 함수
function onConnect() {
	document.getElementById("messages").innerHTML += '<span>connected' + '</span><br/>';
	connectionFlag = true; // 연결 상태로 설정
	client.subscribe("switch")
	client.subscribe("cds")
}

function publish(topic, msg) {
	if(connectionFlag != true) { // 연결되지 않은 경우
		alert("연결되지 않았음");
		return false;
	}
	client.send(topic, msg, 0, false);
}

function unsubscribe(topic) {
	if(connectionFlag != true) return; // 연결되지 않은 경우
	
	// 구독 신청 취소를 <div> 영역에 출력
	document.getElementById("messages").innerHTML += '<span>구독신청취소: 토픽 ' + topic + '</span><br/>';
	client.unsubscribe(topic, null); // 브로커에 구독 신청 취소
}

// 접속이 끊어졌을 때 호출되는 함수
function onConnectionLost(responseObject) { // responseObject는 응답 패킷
	document.getElementById("messages").innerHTML += '<span>오류 : 접속 끊어짐</span><br/>';
	if (responseObject.errorCode !== 0) {
		document.getElementById("messages").innerHTML += '<span>오류 : ' + responseObject.errorMessage + '</span><br/>';
	}
	connectionFlag = false; // 연결 되지 않은 상태로 설정
}

// 메시지가 도착할 때 호출되는 함수
function onMessageArrived(msg) { // 매개변수 msg는 도착한 MQTT 메시지를 담고 있는 객체
	console.log("onMessageArrived: " + msg.payloadString);
	var payload = msg.payloadString;
	var data = JSON.parse(payload);
	// 도착한 메시지 출력
	switch (msg.destinationName){
		case "switch":
			document.getElementById("chatWindow").innerHTML += '<span class="switch">' + data.morse + '<br>─────────────<br>' + data.sentence + '</span>';
			break;
		case "cds":
			document.getElementById("chatWindow").innerHTML += '<span class="cds">' + data.morse + '<br>─────────────<br>' + data.sentence +  '</span>';
			break;
	}
}

// disconnection 버튼이 선택되었을 때 호출되는 함수
function disconnect() {
	if(connectionFlag == false) 
		return; // 연결 되지 않은 상태이면 그냥 리턴
	client.disconnect(); // 브로커와 접속 해제
	document.getElementById("messages").innerHTML += '<span>연결종료</span><br/>';
	connectionFlag = false; // 연결 되지 않은 상태로 설정
}

function toggleImage(){
	var image = document.getElementById("morsecodetable");
	// 이미지가 현재 보이는 상태이면 숨김, 숨겨진 상태이면 보이게 설정
	if (image.style.display === "none") {
		image.style.width = "560px";
        image.style.height = "450px";
        image.style.top = "30px";
        image.style.right = "20px";
        image.style.display = "inline";
	} else {
		image.style.display = "none";
	}
}

function init(){
	var chatWindow = document.getElementById("chatWindow");

	chatWindow.innerHTML = "";
}