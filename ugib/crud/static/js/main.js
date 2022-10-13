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


function deleteUds(event){
    var tag  = event.target.value;
    let cookie = document.cookie;
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    $.post('/', {'del':"del",'oid': tag, "csrfmiddlewaretoken":csrfToken}, function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div)});
}


function createPost(event){
    let form = event.target.parentNode;
    let d = {};
    let inp = form.getElementsByTagName('input');
    let cookie = document.cookie;
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    for (const i in inp){
        if (inp[i].name != undefined){
        d[(inp[i].name)] = inp[i].value
        }
    }
    $.post('/', {'create':"create",'data': d, "csrfmiddlewaretoken":csrfToken} ,function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div);
    }); 
    $(form).trigger("reset")
}


function fixTextareaSize(textarea) {
    textarea.style.height = 'auto'
    textarea.style.height = textarea.scrollHeight + 2 + "px"
  }
  

function update_one_cell(event){
    let but_val = event.target.parentNode.parentNode.parentNode.parentNode;
    let oid = but_val.getElementsByClassName("oid")[0].innerText;

    if (event.target.tagName == "IMG"){
     cell = event.target.parentNode.parentNode.parentNode.innerText;
    } else{
         cell = event.target.parentNode.parentNode.innerText;
    }

    let area = document.getElementById("modal_area")
    $(area).val(cell);
    $('#upd_btn').val(oid)
    area.addEventListener('input', function (e) { fixTextareaSize(area) })
    let count_row = Math.ceil(cell.length / 55)
    area.style.height = count_row * 30 + "px";
    let cls = event.target.closest("td").className;
    $('#close_btn').val(cls)
}


function upd_post(event){
    let oid = document.getElementById('upd_btn').value
    let cookie = document.cookie;
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    cell = document.getElementById('modal_area').value
    let cls = document.getElementById('close_btn').value
    $.post('/', {'upd_one':"upd_one",'oid':oid, 'cls':cls, 'upd_val':cell, "csrfmiddlewaretoken":csrfToken} ,function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div);
    });
}
  

function update_all_cells(event){
   let td_element = event.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
   let all_input = td_element.querySelectorAll("input")
   let data = {}
    for (const i in all_input){
        data[(all_input[i].name)] = all_input[i].value
    }
    let cookie = document.cookie;
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    $.post('/', {'update':"update",'data': data, "csrfmiddlewaretoken":csrfToken} ,function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div);
    });
}

function add_in_bascet(event) {
    let oid = event.target.value
    let cookie = document.cookie;
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    $.post('/', {'bascet':"bascet",'oid': oid, "csrfmiddlewaretoken":csrfToken} ,function(response){
        div = $(response).find('.table-container')
        console.log(div)
        $('.table-container').html(div);
    });
}


function valInput(event){
    let but = event.target;
    let input_html = but.parentNode.parentNode
    let input = input_html.getElementsByTagName("input")[0]
    $(input).val(but.innerText)
    
}

window.addEventListener('load', (event) => {
    let user = document.getElementById("info_user");
    $("#ModalLong").on("hidden.bs.modal", (event) => {console.log("hi!")})
    if (user.value == "False"){
        let all_btn = document.querySelectorAll("button.btn.btn-primary.test")
        for(const i in all_btn){
            all_btn[i].hidden = false;
        } 
    }
  });

