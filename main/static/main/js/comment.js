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