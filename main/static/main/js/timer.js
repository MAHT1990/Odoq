function paddedFormat(num) {
    return num < 10 ? "0" + num : num; 
}

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
        if (secondsRemaining < 0) { clearInterval(countInterval) };

    }, 1000);
}