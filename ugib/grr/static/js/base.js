function window_form(){
    var tag_visable = document.getElementById("loginForm");
    tag_visable.hidden = !tag_visable.hidden
    var tag3 = document.getElementById("closeButton")
    tag3.hidden = !tag3.hidden    
    };

function window_form_order(){
        var tag_visable = document.getElementById("order");
        tag_visable.hidden = !tag_visable.hidden
        // tag2.hidden = !tag2.hidden
        var tag3 = document.getElementById("closeButton")
        tag3.hidden = !tag3.hidden    
        };


function fixTextareaSize(textarea) {
            textarea.style.height = 'auto'
            textarea.style.height = textarea.scrollHeight + 2 + "px"
          }