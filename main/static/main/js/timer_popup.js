// TIMER 관련 함수의 정의//


//10보다 작으면 앞에 0붙여주는 함수
function paddedFormat(num) {
    return num < 10 ? "0" + num : num; 
}

//실제 COUNTDOWN
function startCountDown(duration, element) {

    let secondsRemaining = duration;
    let min = 0;
    let sec = 0;

    let countInterval = setInterval(function () {
        hour = parseInt(secondsRemaining / 3600);
        min = parseInt((secondsRemaining % 3600) / 60);
        sec = parseInt(secondsRemaining % 60);

        element.textContent = `${paddedFormat(hour)}:${paddedFormat(min)}:${paddedFormat(sec)}`;

        secondsRemaining = secondsRemaining - 1;
        if (secondsRemaining < 0) { 
            clearInterval(countInterval);
            location.reload(); 
        };

    }, 1000);
}

//Popup 관련 함수의 정의//

function plan_popup(){
    let popup = document.getElementsByClassName("plan_popup")[0];

    popup.style.display = "block";
}

function close_plan_popup(){
    let popup = document.getElementsByClassName("plan_popup")[0];

    popup.style.display = "none";
}

function sms_popup(){
    let popup = document.getElementsByClassName("sms_popup")[0];

    popup.style.display = "block";
}

function close_sms_popup(){
    let popup = document.getElementsByClassName("sms_popup")[0];

    popup.style.display = "none";
}