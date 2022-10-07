function window_form(){
    var tag_visable = document.getElementById("loginForm");
    tag_visable.hidden = !tag_visable.hidden
    // var tag2 = document.getElementById("loginButton")
    // tag2.hidden = !tag2.hidden
    var tag3 = document.getElementById("closeButton")
    tag3.hidden = !tag3.hidden    
    };
function window_form_order(){
    var tag_visable = document.getElementById("order");
    tag_visable.hidden = !tag_visable.hidden
    // var tag2 = document.getElementById("loginButton")
    // tag2.hidden = !tag2.hidden
    var tag3 = document.getElementById("closeButton")
    tag3.hidden = !tag3.hidden    
    };

function deleteUds(event){
    var ch = []
    var tag  = event.target.value;
    let cookie = document.cookie;
    let td_element = event.target.parentNode.parentNode.parentNode;
    // for (const i in td_element.children){
    //     console.log(td_element.children[i].innerHTML)
    // }
    // document.location.reload()
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    $.post('/table', {'del':"del",'oid': tag, "csrfmiddlewaretoken":csrfToken}, function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div)});
}


function createPost(event){
    let form = event.target.parentNode;
    let d = {};
    let inp= form.getElementsByTagName('input');
    let cookie = document.cookie;
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    let t = 0
    for (const i in inp){
        if (inp[i].name != undefined){
        t = t + 1
        d[(inp[i].name)] = inp[i].value
        }
    }
    $.post('/table', {'create':"create",'data': d, "csrfmiddlewaretoken":csrfToken} ,function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div);
        
        
    });
        
    $(form).trigger("reset")
}

function update_one_cell(event){
    console.log(11111111)
    let but_val = event.target.parentNode.parentNode.parentNode.parentNode
    let oid = but_val.getElementsByClassName("Oid")
    oid = oid[0].innerText
   
    let cell = event.target.parentNode.parentNode.innerText;
    console.log(cell)
}