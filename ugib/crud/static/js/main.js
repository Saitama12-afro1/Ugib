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
    console.log(d)
    $.post('/', {'create':"create",'data': d, "csrfmiddlewaretoken":csrfToken} ,function(response){
        div = $(response).find('.table-container')
        $('.table-container').html(div);
    }); 
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

function valInputMore(event){
    let but = event.target;
    let input_html = but.parentNode.parentNode
    let input = input_html.getElementsByTagName("textarea")[0]
    $(input).val(input.value + but.innerText + "; ")
    let area = document.getElementById("obj_assoc_inv_nums")
    let choise = document.getElementById("obj_sub_group").value
    if (choise == "01TSNIGRI"){
        $(area).val("ЦНИГРИ: ;" + input.value)
    } else if (choise == "02RFGF"){
        $(area).val("Росгеолфонд: ;" + input.value)
    } else if (choise == "03TGF"){
        let stor_phys = document.getElementById("stor_phys").value
        $(area).val(stor_phys+": ;" + input.value)
    }
}
function valInputMoreStorPhys(event){
    let but = event.target;
    let input_html = but.parentNode.parentNode
    let input = input_html.getElementsByTagName("textarea")[0]
    $(input).val(but.innerText)
    let area = document.getElementById("obj_assoc_inv_nums")
    let choise = document.getElementById("obj_sub_group").value

    if (choise == "03TGF"){
        let stor_phys = document.getElementById("stor_phys").value
        let stor_desc = document.getElementById("stor_desc").value
        $(area).val(stor_phys+": ;" + stor_desc)
    }
}
count = 0;

window.addEventListener('load', (event) => {
    let user = document.getElementById("info_user");
    let create_button = document.getElementById("create_button")
    create_button.addEventListener("click", function (event){
        if (count == 0){
        let sl = document.getElementById("select_sub")
            let this_choise = sl.value;
            if (this_choise == "01TSNIGRI")
            $.get( "get_html/", data = {'choise':this_choise}, function( data ) {
                $( "#valid_div" ).html( data );
                TSNIGRI_validation(this_choise)
              });
              else if (this_choise == "02RFGF"){
            $.get( "get_html/", data = {'choise':this_choise}, function( data ) {
                $( "#valid_div" ).html( data );
                TSNIGRI_validation(this_choise)
              });
              }
              else if (this_choise == "03TGF"){
                $.get( "get_html/", data = {'choise':this_choise}, function( data ) {
                    $( "#valid_div" ).html( data );
                    TSNIGRI_validation(this_choise)
                  });
              }else if (this_choise == "04OTHER_ORG"){
                $.get( "get_html/", data = {'choise':this_choise}, function( data ) {
                    $( "#valid_div" ).html( data );
                    TSNIGRI_validation(this_choise)
                  });
              }
        
    }count ++;
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
    let pattern = /,\s?[0-9-]+/
    let year = stor_folder_data.match(pattern)[0]
    year.slice(1)
    let obj_year = document.getElementById("obj_year")
    $(obj_year).val(year.slice(1))
    let path_local = document.getElementById("path_local")
    let path_local_ref = document.getElementById("path_local_ref")
    let path_cloud = document.getElementById("path_cloud")
    let obj_main_group = document.getElementById("obj_main_group")
    let obj_sub_group = document.getElementById("obj_sub_group")
    $(path_local).val("\\"+"\\pegas\\UDS\\" + obj_main_group.value + "\\" + obj_sub_group.value + "\\" + stor_folder_data)
    $(path_local_ref).val("\\"+"\\pegas\\UDS\\" + obj_main_group.value + "\\" + obj_sub_group.value + "_REF\\" + stor_folder_data)
    let choise = document.getElementById("select_sub").value
    if (choise == "01TSNIGRI"){
    $(path_cloud).val("http://cloud.tsnigri.ru/apps/files/?dir=/"+obj_main_group.value.slice(0,2) +"-"+obj_sub_group.value.slice(0,2)+"-ФОНДОВЫЕ МАТЕРИАЛЫ ЦНИГРИ/"+stor_folder_data)
    $(path_cloud_ref).val("http://cloud.tsnigri.ru/apps/files/?dir=/"+obj_main_group.value.slice(0,2) +"-"+obj_sub_group.value.slice(0,2)+"-РЕФЕРАТЫ ФОНДОВЫХ МАТЕРИАЛОВ ЦНИГРИ//"+stor_folder_data)
}else if (choise == "02RFGF"){
    $(path_cloud).val("http://cloud.tsnigri.ru/apps/files/?dir=/"+obj_main_group.value.slice(0,2) +"-"+obj_sub_group.value.slice(0,2)+"-МАТЕРИАЛЫ РОСГЕОЛФОНДА/"+stor_folder_data)
    $(path_cloud_ref).val("http://cloud.tsnigri.ru/apps/files/?dir=/"+obj_main_group.value.slice(0,2) +"-"+obj_sub_group.value.slice(0,2)+"-РЕФЕРАТЫ ФОНДОВЫХ МАТЕРИАЛОВ РФГФ/"+stor_folder_data)
}else if (choise == "03TGF"){
    $(path_cloud).val("http://cloud.tsnigri.ru/apps/files/?dir=/"+obj_main_group.value.slice(0,2) +"-"+obj_sub_group.value.slice(0,2)+"-МАТЕРИАЛЫ РЕГИОНАЛЬНЫХ ФОНДОВ/"+stor_folder_data)
    $(path_cloud_ref).val("http://cloud.tsnigri.ru/apps/files/?dir=/"+obj_main_group.value.slice(0,2) +"-"+obj_sub_group.value.slice(0,2)+"-РЕФЕРАТЫ ФОНДОВЫХ МАТЕРИАЛОВ ТГФ/"+stor_folder_data)
}else if(choise == "04OTHER_ORG"){
    $(path_cloud).val("http://cloud.tsnigri.ru/apps/files/?dir=/"+obj_main_group.value.slice(0,2) +"-"+obj_sub_group.value.slice(0,2)+"-ФОНДОВЫЕ%20МАТЕРИАЛЫ%20СТОРОННИХ%20ОРГАНИЗАЦИЙ/"+stor_folder_data)
    $(path_cloud_ref).val("http://cloud.tsnigri.ru/apps/files/?dir=/"+obj_main_group.value.slice(0,2) +"-"+obj_sub_group.value.slice(0,2)+"-ФОНДОВЫЕ МАТЕРИАЛЫ СТОРОННИХ ОРГАНИЗАЦИЙ/"+stor_folder_data)
}
}
