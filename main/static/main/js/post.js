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

// 답안제출 POST AJAX//

function answer_post(){
    var answer_box_element = document.getElementById('answer_input');
    if(answer_box_element.value != ''){
        let url = '/answer_post/';
        let req = new XMLHttpRequest();
        req.open('POST', url, true);
        req.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200) {
                const jsonResponse = JSON.parse(req.responseText);
                const debugging = jsonResponse['debugging'];
                console.log(debugging);
                answer_box_element.value = jsonResponse['answer_response'];
            }
        }

    // POST 관련 보안을 위한 Cookie 처리
        

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

function phone_number_post(){
    var phone_number_input_box_element = document.getElementById("phone_number_input");

    if(phone_number_input_box_element.value !=''){
        let url = '/sms_new/';
        let req = new XMLHttpRequest();
        req.open('POST', url);
        req.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200) {
                const jsonResponse = JSON.parse(req.responseText);
                const debugging = jsonResponse['debugging'];
                console.log(debugging);
                phone_number_input_box_element.value = jsonResponse['answer_response'];
            }
        }

        var csrftoken = getCookie('csrftoken');

        req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
        req.setRequestHeader("X-CSRFToken", csrftoken)

        // 보낼 data 양식 맞춰서, send로 보내기.

        var data = "";
        data += 'phone_number_input='+document.getElementById('phone_number_input').value;
        req.send(data);

    }else{
        console.log('empty value');
    }
}

function phone_number_delete(){
    var phone_number_input_box_element = document.getElementById("phone_number_input");

    if(phone_number_input_box_element.value !=''){
        let url = '/sms_delete/';
        let req = new XMLHttpRequest();
        req.open('POST', url);
        req.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200) {
                const jsonResponse = JSON.parse(req.responseText);
                const debugging = jsonResponse['debugging'];
                console.log(debugging);
                phone_number_input_box_element.value = jsonResponse['answer_response'];
            }
        }

        var csrftoken = getCookie('csrftoken');

        req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
        req.setRequestHeader("X-CSRFToken", csrftoken)

        // 보낼 data 양식 맞춰서, send로 보내기.

        var data = "";
        data += 'phone_number_input='+document.getElementById('phone_number_input').value;
        req.send(data);

    }else{
        console.log('empty value');
    }
}

function comment_delete(id){
    let url = '/comment/delete/';
    let req = new XMLHttpRequest();
    req.open('POST', url);
    req.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            const jsonResponse = JSON.parse(req.responseText);
            const debugging = jsonResponse['debugging'];
            console.log(debugging);
            var tgrt_comment_line = document.getElementById('comment_id_'+id);
            tgrt_comment_line.remove();
        }
    }

    var csrftoken = getCookie('csrftoken');

        req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
        req.setRequestHeader("X-CSRFToken", csrftoken)

        // 보낼 data 양식 맞춰서, send로 보내기.

        var data = "";
        data += "comment_id="+id;
        req.send(data);
}

function open_cocomment(self, id){
    var tgrt_comment_line = document.getElementById('comment_id_'+id);
    var cocomment_list = document.createElement('div');
    
    cocomment_list.setAttribute("id", "cocomment_list_"+id);

    var test_text = document.createTextNode('TestTextTestText');
    cocomment_list.appendChild(test_text);
    tgrt_comment_line.appendChild(cocomment_list);

    self.setAttribute("onclick", "close_cocomment(this, "+id+")");
    console.log('BOOYAH')
}

function close_cocomment(self,id){
    var tgrt_cocoment_list = document.getElementById('cocomment_list_'+id);
    tgrt_cocoment_list.remove();

    self.setAttribute("onclick", "open_cocomment(this, "+id+")");

}