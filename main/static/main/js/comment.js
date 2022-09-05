function input_box_open(){
    console.log('input box will open');
}


function open_cocomment(self, id){
    let cocomment_container = document.getElementById("comment_id_"+id+"_cocomment");
    
    if (cocomment_container.style.display == "block"){
        cocomment_container.style.display = "none";
        if (localStorage.getItem('cocomment_open')){
            localStorage.removeItem('cocomment_open');
        }
        console.log(localStorage);

    } else {
        cocomment_container.style.display = "block";
        window.onbeforeunload = function(event) {
            localStorage.setItem('cocomment_open', "comment_id_"+id+"_cocomment");
            // cocomment_container.style.display = "block";
        };
        console.log(localStorage);
    }
    
    console.log('BOOYAH');
}


function open_tool_box(e, self, id){
    console.log("mouse location:", e.pageX, e.pageY);
    console.log("this is ", self);

    let prefix;
    if(self.getAttribute("class").indexOf('cocomment')<0){
        prefix = 'comment_' 
    } else {
        prefix = 'cocomment_'
    }

    let trgt_tool_box_popup = document.getElementById(prefix + "tool_box_popup_id_"+id);
    let trgt_tool_box = document.getElementById(prefix + "tool_box_id_"+id);
    console.log(prefix + "tool box :", trgt_tool_box);
    console.log(prefix + "tool box popup :", trgt_tool_box_popup);
    
    trgt_tool_box.style.display='block';
    trgt_tool_box.style.position='absolute';
    trgt_tool_box.style.left=e.pageX+'px';
    trgt_tool_box.style.top=e.pageY+'px';
    
    trgt_tool_box_popup.style.display='block';
}

function close_tool_box(self, id){

    let prefix;
    if(self.getAttribute("class").indexOf('cocomment')<0){
        prefix = 'comment_' 
    } else {
        prefix = 'cocomment_'
    }

    self.style.display='none';
    let trgt_tool_box = document.getElementById(prefix + "tool_box_id_"+id);
    trgt_tool_box.style.display='none';
}

// comment_page_navigation
function comment_page_show(page_num, max_page){
    let page_numbering = document.getElementById("comment_list_navigator_page_numbering");
                
    for (var i=1; i<=max_page; i++){
        if(i==page_num){
            trgt_page = document.getElementById("comment_list_page_"+page_num);
            trgt_page.style.display = "block";
            page_numbering.textContent = i +'/'+max_page;

            prev_button = document.getElementById("comment_list_navigator_prev")
            if(page_num == 1){
                prev_button.setAttribute("onclick", "comment_page_show("+page_num+","+max_page+")");
            } else {
                prev_button.setAttribute("onclick", "comment_page_show("+(page_num-1)+","+max_page+")");
            }

            next_button = document.getElementById("comment_list_navigator_next")
            if(page_num == max_page){
                next_button.setAttribute("onclick", "comment_page_show("+page_num+","+max_page+")");
            } else {
                next_button.setAttribute("onclick", "comment_page_show("+(page_num+1)+","+max_page+")");
            }

        } else {
            page = document.getElementById("comment_list_page_"+i);
            page.style.display = "none";
        }
    }
}