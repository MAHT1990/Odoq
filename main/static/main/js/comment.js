function open_cocomment(self, id){
    let cocomment_container = document.getElementById("comment_id_"+id+"_cocomment");
    
    cocomment_container.style.display = "block";
    
    self.setAttribute("onclick", "close_cocomment(this, "+id+")");
    console.log('BOOYAH');
}


function close_cocomment(self, id){
    let cocomment_container = document.getElementById("comment_id_"+id+"_cocomment");

    cocomment_container.style.display = "none";

    self.setAttribute("onclick", "open_cocomment(this, "+id+")");
    console.log('COOYAH');
}

function open_tool_box(e, self, id){
    console.log("mouse location:", e.pageX, e.pageY);
    console.log("this is ", self);

    let trgt_tool_box_popup = document.getElementById("comment_tool_box_popup_id_"+id);
    let trgt_tool_box = document.getElementById("comment_tool_box_id_"+id);
    console.log("tool box :", trgt_tool_box);
    console.log("tool box popup :", trgt_tool_box_popup);
    
    trgt_tool_box.style.display='block';
    trgt_tool_box.style.position='absolute';
    trgt_tool_box.style.left=e.pageX+'px';
    trgt_tool_box.style.top=e.pageY+'px';
    
    trgt_tool_box_popup.style.display='block';
}

function close_tool_box(self, id){
    self.style.display='none';
    let trgt_tool_box = document.getElementById("comment_tool_box_id_"+id);
    trgt_tool_box.style.display='none';
}

// comment_page_navigation
function comment_page_show(page_num, max_page){
                
    for (var i=1; i<=max_page; i++){
        if(i==page_num){
            trgt_page = document.getElementById("comment_list_page_"+page_num);
            trgt_page.style.display = "block";

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