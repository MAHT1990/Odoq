// 답안제출 POST AJAX//
function answer_post(){
    var answer_box_element = document.getElementById('answer_input');
    if(answer_box_element.value != ''){
        let url = 'answer_post/';
        let req = new XMLHttpRequest();
        req.open('POST', url);
        req.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200) {
                const jsonResponse = JSON.parse(req.responseText);
                const debugging = jsonResponse['debugging'];
                console.log(debugging);
                answer_box_element.value = jsonResponse['answer_response'];
            }
        }

    // POST 관련 보안을 위한 Cookie 처리
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                    }
                }
            }   
            return cookieValue;
        }

        var csrftoken = getCookie('csrftoken');

        req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
        req.setRequestHeader("X-CSRFToken", csrftoken)

        // 보낼 data 양식 맞춰서, send로 보내기.

        var data = "";
        data += 'answer_input='+document.getElementById('answer_input').value;
        req.send(data);
    }else{
        console.log('empty value');
    }
}