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

function comment_delete(self, id){
    var url = '';
    var tgrt_comment_line = null;
    var data = '';
    
    if(self.getAttribute("class").indexOf('coco')<0){
        url = '/comment/delete/';
        tgrt_comment_line = document.getElementById('comment_id_'+id);
        data = "comment_id="+id;
    } else {
        url = '/cocomment/delete/';
        tgrt_comment_line = document.getElementById('cocomment_id_'+id);
        data = "cocomment_id="+id;
    }

    let req = new XMLHttpRequest();
    req.open('POST', url);
    req.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            const jsonResponse = JSON.parse(req.responseText);
            const debugging = jsonResponse['debugging'];
            console.log(debugging);
            tgrt_comment_line.remove();
        }
    }

    var csrftoken = getCookie('csrftoken');

        req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
        req.setRequestHeader("X-CSRFToken", csrftoken)

        // 보낼 data 양식 맞춰서, send로 보내기.

        req.send(data);
}

// 댓글 수정 INTERFACE
function comment_edit_open(self, id){
    let trgt_comment_content = document.getElementById('comment_content_'+id);

    let comment_edit_input_box = document.createElement('div');
    let comment_edit_input = document.createElement('input');
    let comment_edit_button = document.createElement('button');

    // comment의 id에 맞추어 id 지어주기 & button 이름 지어주기
    comment_edit_input_box.setAttribute("id", "comment_edit_input_box_"+id);
    comment_edit_input.setAttribute("id", "comment_edit_input_"+id);
    comment_edit_button.setAttribute("id", "comment_edit_button_"+id); 
    comment_edit_button.innerHTML="수정";

    // input 창의 값은 현재 댓글 내용을 있는 그대로 반영
    comment_edit_input.value = trgt_comment_content.innerHTML;

    // input 의 onclick EVENT 넣어주기 - comment_edit(id) 실행되도록
    comment_edit_button.setAttribute("onclick", "comment_edit("+id+")");

    // 만든 child 요소 : input, button 를 comment_edit_input_box에 넣어주기
    comment_edit_input_box.appendChild(comment_edit_input);
    comment_edit_input_box.appendChild(comment_edit_button);

    // 기존의 댓글창을 comment_edit_input_box로 교체.
    trgt_comment_content.parentNode.replaceChild(comment_edit_input_box, trgt_comment_content);
}

// 실제 댓글 수정 AJAX
function comment_edit(id){
    let comment_edit_content = document.getElementById("comment_edit_input_"+id).value;
    console.log(comment_edit_content);

    let url = '/comment/edit/';
    let req = new XMLHttpRequest();
    req.open('POST', url, true);
    req.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            location.reload();
        }
    }

    // POST 관련 보안을 위한 Cookie 처리
        
    var csrftoken = getCookie('csrftoken');

    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    req.setRequestHeader("X-CSRFToken", csrftoken)

    // 보낼 data 양식 맞춰서, send로 보내기.

    let data = "";
    data += 'comment_id='+ id + '&' + 'content=' + comment_edit_content;
    console.log(data);
    req.send(data);
}

// 댓글 및 대댓글 좋아요 관련 function

function like(self, id, zero_xor_one){
    var url = '';
    
    if(self.getAttribute("class").indexOf('coco')<0){
        url = '/comment/like/' + id + '/' + zero_xor_one + '/';
    } else {
        url = '/cocomment/like/' + id +'/' + zero_xor_one + '/';
    }

    let req = new XMLHttpRequest();
    req.open('GET', url);
    req.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            const jsonResponse = JSON.parse(req.responseText);
            var like_count = jsonResponse['comment_like_count'];
            if (like_count == null){
                like_count = jsonResponse['cocomment_like_count'];
            }
            console.log(like_count);
            self.innerHTML = like_count;
        }
    }
    if(zero_xor_one == 0){
        self.setAttribute("onclick", "like(this, "+id+", 1"+")");
        console.log('DOOYAH');
    } else {
        self.setAttribute("onclick", "like(this, "+id+", 0"+")");
        console.log('EOOYAH');
    }

    req.send();
}