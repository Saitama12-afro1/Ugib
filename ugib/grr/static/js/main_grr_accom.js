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
    $.post('/grr-accom/', {'del':"del",'oid': tag, "csrfmiddlewaretoken":csrfToken}, function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div)});
}


function fixTextareaSize(textarea) {
    textarea.style.height = 'auto'
    textarea.style.height = textarea.scrollHeight + 2 + "px"
  }
  


function createPost(event){
    let form = event.target.parentNode;
    let d = {};
    let inp = form.getElementsByTagName('textarea');
    let cookie = document.cookie;
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    for (const i in inp){
       
        if (inp[i].name != undefined){
        d[(inp[i].name)] = inp[i].value
    
        }
    }
    $.post('/grr-accom/', {'create':"create",'data': d, "csrfmiddlewaretoken":csrfToken} ,function(response){
        div = $(response).find('.table-container')
        console.log(div)
        $('.table-container').html(div);
    });
    let div = document.getElementsByClassName("boss_div")[0]
    div.style = " position: sticky;"; 
    $(form).trigger("reset")
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
    $.post('/grr-accom/', {'upd_one':"upd_one",'oid':oid, 'cls':cls, 'upd_val':cell, "csrfmiddlewaretoken":csrfToken} ,function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div);
    });
}
  

function update_all_cells(event){
   let td_element = event.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
   console.log(td_element)
   let all_input = td_element.querySelectorAll("textarea")
   let data = {}
    for (const i in all_input){
        data[(all_input[i].name)] = all_input[i].value
    }
    let cookie = document.cookie;
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    $.post('/grr-accom/', {'update':"update",'data': data, "csrfmiddlewaretoken":csrfToken} ,function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div);
    });
}

function add_in_bascet(event) {
    let oid = event.target.value
    let cookie = document.cookie;
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    $.post('/grr-accom/', {'bascet':"bascet",'oid': oid, "csrfmiddlewaretoken":csrfToken} ,function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div);
    });
}


function valInput(event){
    let but = event.target;
    let input_html = but.parentNode.parentNode
    let input = input_html.getElementsByTagName("textarea")[0]
    $(input).val(but.innerText)
}
function valInputMoreElements(event){
    let but = event.target;
    let input_html = but.parentNode.parentNode
    let input = input_html.getElementsByTagName("textarea")[0]
    $(input).val(input.value + but.innerText + ", ")
}


function valInputMoreStorPhys(event){
    let but = event.target;
    let input_html = but.parentNode.parentNode
    let input = input_html.getElementsByTagName("textarea")[0]
    $(input).val(but.innerText)
}
count = 0;

window.addEventListener('load', (event) => {
    let user = document.getElementById("info_user");
    let create_button = document.getElementById("create_button")
    create_button.addEventListener("click", function (event){
        let sl = document.getElementById("select_sub")
            let this_choise = sl.value;
            if (this_choise == "GRR-ACCOM")
            $.get( "/get_html_grr_stage/", data = {'choise':this_choise}, function( data ) {
                $( "#valid_div" ).html( data );
                TSNIGRI_validation(this_choise)
              });
    count ++;
    })
    if (user.value == "False"){
        let all_btn = document.querySelectorAll("button.btn.btn-primary.test")
        for(const i in all_btn){
            all_btn[i].hidden = false;
        }}
    const config = { attributes: false, childList: true, subtree: true };
    var observer = new MutationObserver((mutationList, observer) =>{ let user = document.getElementById("info_user");
    if (user.value == "False"){
        let all_btn = document.querySelectorAll("button.btn.btn-primary.test")
        for(const i in all_btn){
            all_btn[i].hidden = false;
        }}
    });
    dv = document.getElementsByClassName("obs_table")[0]
    observer.observe(document, config);
})



function my_blur(event){
    let stor_folder_data = event.target.value
    let pattern = /[0-9]+/
    let year = stor_folder_data.match(pattern)[0]

    let obj_year = document.getElementById("obj_year")
    $(obj_year).val(year)
    let path_local = document.getElementById("path_local")
    let path_cloud = document.getElementById("path_cloud")
 
    $(path_local).val("\\"+"\\pegas\\UDS\\14GRR\\02_GRR_SOPROV\\" + stor_folder_data)
    $(path_cloud).val("http://cloud.tsnigri.ru/apps/files/?dir=/14-02-" + "МАТЕРИАЛЫ%20СОПРОВОЖДЕНИЕ%20ГРР/"+stor_folder_data)
}


function testik(event, record) {
    $.get( "/get_html_grr_stage/", data = {'oid_accom':record,}, function( data ) {
        $( ".upd_div" ).html( data );
      });
}

function change_style(event){
    let div = document.getElementsByClassName("boss_div")[0]
    div.style = " position: revert;";
    modal = document.getElementById("ModalLong")
    
}
function unchange_style(event){
    let div = document.getElementsByClassName("boss_div")[0]
    div.style = " position: sticky;";
}
