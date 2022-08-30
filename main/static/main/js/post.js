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

function enter_form_submit(e){
    let x = e.key;
    if(x == "Enter"){
        form_submit();
    }
}

function form_submit(){
    let url = '/comment/new/';
    let input_box_form = document.getElementsByClassName('comment_input_box_form')[0];
    let form = new FormData(input_box_form);
    let data = '';
    
    let req = new XMLHttpRequest();
    req.open('POST', url);
    req.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            const jsonResponse = JSON.parse(req.responseText);
            const debugging = jsonResponse['debugging'];
            
            location.reload(true);
        }
    }
    
    var csrftoken = getCookie('csrftoken');
    
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    req.setRequestHeader("X-CSRFToken", csrftoken)
    
    // 보낼 data 양식 맞춰서, send로 보내기.
    for (const [key, value] of form) {
        data+=(`${key}=${value}&`);
    }
    // input_box.submit();
    // location.reload();
    
    req.send(data);
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
    
    let prefix = '';

    if(self.getAttribute("class").indexOf('coco')<0){
        prefix = 'comment';
    } else {
        prefix = 'cocomment';
    }

    let trgt_content = document.getElementById(prefix+'_content_'+id);

    let edit_input_box = document.createElement('div');
    let edit_input = document.createElement('input');
    let edit_button = document.createElement('button');
    let edit_cancel_button = document.createElement('button');

    // comment의 id에 맞추어 id 지어주기 & button 이름 지어주기
    edit_input_box.setAttribute("class", prefix+"_edit_input_box");
    edit_input_box.setAttribute("id", prefix+"_edit_input_box_"+id);

    edit_input.setAttribute("class", prefix+"_edit_input");
    edit_input.setAttribute("id", prefix+"_edit_input_"+id);

    edit_button.setAttribute("class", prefix+"_edit_button");
    edit_button.setAttribute("id", prefix+"_edit_button_"+id);
    edit_button.innerHTML="수정";

    edit_cancel_button.setAttribute("class", prefix+"_edit_cancel_button");
    edit_cancel_button.setAttribute("id", prefix+"_edit_cancel_button_"+id); 
    edit_cancel_button.innerHTML="취소";

    // input 창의 값은 현재 댓글 내용을 있는 그대로 반영
    edit_input.value = trgt_content.innerHTML;

    // input 의 onclick EVENT 넣어주기 - comment_edit(id) 실행되도록
    edit_button.setAttribute("onclick", "comment_edit("+"this, "+id+")");

    // cancle_button 의 onclick EVENT 넣어주기 - comment_edit_cancel
    edit_cancel_button.setAttribute("onclick", "comment_edit_cancel()");

    // 만든 child 요소 : input, button 를 comment_edit_input_box에 넣어주기
    edit_input_box.appendChild(edit_input);
    edit_input_box.appendChild(edit_button);
    edit_input_box.appendChild(edit_cancel_button);
    

    // 기존의 댓글창을 comment_edit_input_box로 교체.
    trgt_content.parentNode.replaceChild(edit_input_box, trgt_content);
    
    // tool_box와 tool_box_popup을 닫아줘야한다.
    let trgt_tool_box = document.getElementById(prefix+"_tool_box_id_"+id);
    let trgt_tool_box_popup = document.getElementById(prefix+"_tool_box_popup_id_"+id);

    trgt_tool_box.style.display="none";
    trgt_tool_box_popup.style.display="none";
}

// 실제 댓글 수정 AJAX
function comment_edit(self, id){
    let url = '';
    let prefix = '';

    if(self.getAttribute("id").indexOf('coco')<0){
        prefix = 'comment';
        url = '/comment/edit/';
    } else {
        prefix = 'cocomment';
        url = '/cocomment/edit/';
    }

    let edit_content = document.getElementById(prefix+"_edit_input_"+id).value;
    console.log(edit_content);

    let req = new XMLHttpRequest();
    req.open('POST', url, true);
    req.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            location.reload(true);
        }
    }

    // POST 관련 보안을 위한 Cookie 처리
        
    var csrftoken = getCookie('csrftoken');

    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    req.setRequestHeader("X-CSRFToken", csrftoken)

    // 보낼 data 양식 맞춰서, send로 보내기.

    let data = "";
    data += (prefix+'_id=')+ id + '&' + 'content=' + edit_content;
    console.log(data);
    req.send(data);
}

function comment_edit_cancel(){
    location.reload(true);
}

// 댓글 및 대댓글 좋아요 관련 function

function like(self, id, zero_xor_one){
    var url = '';
    
    if(self.getAttribute("class").indexOf('coco')<0){
        url = '/comment/like/' + id + '/';
    } else {
        url = '/cocomment/like/' + id +'/';
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
            let bfr_like_count = self.children[1].innerHTML
            console.log(bfr_like_count,like_count);
            
            if(bfr_like_count < like_count){
                self.setAttribute("onclick", "like(this, "+id+", 1"+")");
                self.children[0].setAttribute("class", "fa-solid fa-thumbs-up")
            } else {
                self.setAttribute("onclick", "like(this, "+id+", 0"+")");
                self.children[0].setAttribute("class", "fa-regular fa-thumbs-up")
            }

            self.children[1].innerHTML = like_count;
        }
    }
    

    req.send();
}