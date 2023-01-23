function dinamic_form(event) {
    let this_choise = event.target.value;
    if (this_choise == "01TSNIGRI")
    $.get( "get_html_uds/", data = {'choise':this_choise}, function( data ) {
        $( "#valid_div" ).html( data );
        TSNIGRI_validation(this_choise)
      });
      else if (this_choise == "02RFGF"){
    $.get( "get_html_uds/", data = {'choise':this_choise}, function( data ) {
        $( "#valid_div" ).html( data );
        TSNIGRI_validation(this_choise)
      });
      }
      else if (this_choise == "03TGF"){
        $.get( "get_html_uds/", data = {'choise':this_choise}, function( data ) {
            $( "#valid_div" ).html( data );
            TSNIGRI_validation(this_choise)
          });
      }else if (this_choise == "04OTHER_ORG"){
        $.get( "get_html_uds/", data = {'choise':this_choise}, function( data ) {
            $( "#valid_div" ).html( data );
            TSNIGRI_validation(this_choise)
          });
      }
}

function current_height(area){
    let count_row = Math.ceil(area.value.length / 55)
    area.style.height = count_row * 30 + "px";
}

  function TSNIGRI_validation(choise){
    let stor_folder = document.getElementById("stor_folder_valid");
    stor_folder.addEventListener("input", (event) => {
    fixTextareaSize(stor_folder);
    var pattern =/[0-9]+-[а-яА-ЯёЁ]+\s?[а-яА-ЯёЁ]?\.?\s?[а-яА-ЯёЁ]?\.?\,[0-9]+/
    const error = document.querySelector(".error");
    if (pattern.test(stor_folder.value)){
        error.textContent = "";
        error.className = "error";
    }else{
        showError()
    } 
    function showError() {
        error.textContent = "Не соответствует шаблону Число-Фамилия И.И.,Число"
        error.className = 'error active';
    }
    })

    let stor_reason = document.getElementById("stor_reason");
    current_height(stor_reason)
    stor_reason.addEventListener("input", function (e) { fixTextareaSize(stor_reason) })

    let obj_assoc_inv_nums = document.getElementById("obj_assoc_inv_nums")
    obj_assoc_inv_nums.addEventListener("input", function (e){fixTextareaSize(obj_assoc_inv_nums)})

    let spat_num_grid = document.getElementById("spat_num_grid_valid");
    spat_num_grid.addEventListener("input", (event) => {
        fixTextareaSize(spat_num_grid);
        var pattern =/[I-V]-[0-9][0-9]-[IVX]+/
        const error = document.querySelector("#error_spat_num_grid");
        if (pattern.test(spat_num_grid.value)){
            error.textContent = "";
            error.className = "error";
        }else{
            showError()
        }        
        function showError() {
            error.textContent = "Не соответствует шаблону N-46-XVI"
            error.className = 'error active';
        }
        })

    let obj_authors = document.getElementById("obj_authors_valid");
    obj_authors_valid.addEventListener("input", (event) => {
        fixTextareaSize(obj_authors);
        let count_comma = 0 
        for (const i in obj_authors.value){
            if (obj_authors.value[i] == ","){
                ++count_comma;
            };
        }
        const error = document.querySelector("#error_obj_authors");
        if (count_comma == 0){
        var pattern =/[А-я]+\s[А-я]\.[A-я]\./
            if (pattern.test(obj_authors.value)){
                error.textContent = "Не соответствует шаблону ";
                error.className = "error";
            }else{
                showError()
            }        
        } else if (count_comma == 1){
            var pattern =/[А-я]+\s[А-я]\.[A-я]\.\,\s[А-я]+\s[А-я]\.[A-я]\./
            if (pattern.test(obj_authors.value)){
                error.textContent = "";
                error.className = "error";
            }else{
                showError()
            }    
        }else if (obj_authors.value.indexOf("и др.", 10) != -1 ){
            var pattern =/[А-я]+\s[А-я]\.[A-я]\.\,\s[А-я]+\s[А-я]\.[A-я]\.,\s[А-я]+\s[А-я]\.[A-я]\.\sи\sдр\.$/
            if (pattern.test(obj_authors.value)){
                error.textContent = "";
                error.className = "error";
            }else{
                showError()
            } 
        }else if (count_comma == 2){
            var pattern =/[А-я]+\s[А-я]\.[A-я]\.\,\s[А-я]+\s[А-я]\.[A-я]\.,\s[А-я]+\s[А-я]\.[A-я]\.$/
            if (pattern.test(obj_authors.value)){
                error.textContent = "";
                error.className = "error";
            }else{
                showError()
            }
        } else if (count_comma >= 3){
            showError()
        }
        
        function showError() {
            error.textContent = "Не соответствует шаблону возможно не хватает запятых или же точек в инициалах"
            error.className = 'error active';
        }
        
        })
        
    let obj_terms = document.getElementById("obj_terms_valid");
    obj_terms.addEventListener("input", (event) => {
        fixTextareaSize(obj_terms);
        var pattern =/[А-я\,\s]+[^\.]$/
        const error = document.querySelector("#error_obj_terms");
        if (pattern.test(obj_terms.value)){
            error.textContent = "";
            error.className = "error";
        }else{
            showError()
        }        
        function showError() {
            error.textContent = "Не соответствует шаблону"
            error.className = 'error active';
        }
    })

    let stor_desc = document.getElementById("stor_desc")
    stor_desc.addEventListener("input", (event) =>{
        fixTextareaSize(stor_desc);
        let area = document.getElementById("obj_assoc_inv_nums")
        let choise = document.getElementById("obj_sub_group").value
        if (choise == "01TSNIGRI"){
            $(area).val("ЦНИГРИ: ;" + stor_desc.value)
        } else if (choise == "02RFGF"){
            $(area).val("Росгеолфонд: ;" + stor_desc.value)
        }
        else if (choise == "03TGF"){
            let stor_phys = document.getElementById("stor_phys").value
            $(area).val(stor_phys+": ;" + stor_desc.value)
        }
    })
    if ((choise == "03TGF")|| (choise == "04OTHER_ORG")){
    let stor_phys = document.getElementById("stor_phys")
    stor_phys.addEventListener("input", (event) =>{
        fixTextareaSize(area);
        let area = document.getElementById("obj_assoc_inv_nums")
        let choise = document.getElementById("obj_sub_group").value
        if (choise == "03TGF"){
            let stor_desc = document.getElementById("stor_desc").value
            $(area).val(stor_phys.value+": ; " + stor_desc)
        }
    })
    }

    let obj_main_min = document.getElementById("obj_main_min_valid");
    obj_main_min.addEventListener("input", (event) => {
        fixTextareaSize(obj_main_min);
        var pattern =/[А-я\s]+\,\s?/
        const error = document.querySelector("#error_obj_main_min");
        if (pattern.test(obj_main_min.value)){
            error.textContent = "";
            error.className = "error";
        }else{
            showError()
        }        
        function showError() {
            error.textContent = "Не соответствует шаблону"
            error.className = 'error active';
        }
    })
    let obj_supl_min = document.getElementById("obj_supl_min_valid");
    obj_supl_min.addEventListener("input", (event) => {
        fixTextareaSize(obj_supl_min);
        var pattern =/[А-я\s]+\,\s?/
        const error = document.querySelector("#error_obj_supl_min");
        if (pattern.test(obj_supl_min.value)){
            error.textContent = "";
            error.className = "error";
        }else{
            showError()
        }        
        function showError() {
            error.textContent = "Не соответствует шаблону"
            error.className = 'error active';
        }
    })
    

    let obj_rdoc_name = document.getElementById("obj_rdoc_name_valid");
    obj_rdoc_name.addEventListener("input", (event) => {
        fixTextareaSize(obj_rdoc_name);
        let mas = right_bracket(obj_rdoc_name.value)
        const error = document.querySelector("#error_obj_rdoc_name");
        if (mas.length == 0 && obj_rdoc_name.value.search(pattern1) == -1  && obj_rdoc_name.value.search(pattern2) == -1){
            error.textContent = "";
            error.className = "error";
        }else{
            showError()
        }        
        function showError() {
            error.textContent = "Не соответствует шаблону, не закрыта скобка или кавычка или же вы используете <<"
            error.className = 'error active';
        }
    })
    let obj_rdoc_num = document.getElementById("obj_rdoc_num_valid");
    obj_rdoc_num.addEventListener("input", (event) => {
        fixTextareaSize(obj_rdoc_num);
        let mas = right_bracket(obj_rdoc_num.value)
        const error = document.querySelector("#error_obj_rdoc_num");
        if (mas.length == 0  && obj_rdoc_num.value.search(pattern1) == -1  && obj_rdoc_num.value.search(pattern2) == -1){
            error.textContent = "";
            error.className = "error";
        }else{
            showError()
        }        
        function showError() {
            error.textContent = "Не соответствует шаблону, не закрыта скобка или кавычка или же вы используете <<"
            error.className = 'error active';
        }
    })
    let obj_name = document.getElementById("obj_name_valid");
    obj_name.addEventListener("input", (event) => {
        fixTextareaSize(obj_name);
        let mas = right_bracket(obj_name.value)
        const error = document.querySelector("#error_obj_name");
        if (mas.length == 0  && obj_name.value.search(pattern1) == -1  && obj_name.value.search(pattern2) == -1){
            error.textContent = "";
            error.className = "error";
        }else{
            showError()
        }        
        function showError() {
            error.textContent = "Не соответствует шаблону, не закрыта скобка или кавычка или же вы используете <<"
            error.className = 'error active';
        }
    })
    let obj_orgs = document.getElementById("obj_orgs_valid");
    obj_orgs.addEventListener("input", (event) => {
        let mas = right_bracket(obj_orgs.value);
        const error = document.querySelector("#error_obj_orgs");
        pattern1 = /<</;
        pattern2 = />>/;

        if (mas.length == 0 && obj_orgs.value.search(pattern1) == -1  && obj_orgs.value.search(pattern2) == -1){
            error.textContent = "";
            error.className = "error";
        }else{
            showError()
        }        
        function showError() {
            error.textContent = "Не соответствует шаблону, не закрыта скобка или кавычка или же вы используете <<"
            error.className = 'error active';
        }
    })
    let spat_atd_ate = document.getElementById("spat_atd_ate_valid");
    obj_orgs.addEventListener("input", (event) => {
        fixTextareaSize(spat_atd_ate);
        var pattern =/[(кр)(обл)]+([\s, .])/
        let p = pattern.exec(spat_atd_ate.value)
        const error = document.querySelector("#error_spat_atd_ate");
        if (p == null){
            error.textContent = "";
            error.className = "error";
        }else{
            showError()
        }        
        function showError() {
            error.textContent = "ээээээээ"
            error.className = 'error active';
        }
    })
  }

function right_bracket(str){
    let mas = []
    for (i in str){
        if (str[i] == "("){
            mas.push(str[i])
        }
        else if (str[i] == ")"){
                buff = mas.indexOf("(")
                if (buff != -1){
                mas.splice(buff, 1)
                }else{
                    mas.push([i])
                }
                
        }
        else if ((str[i] == "\"") && (mas.indexOf(str[i]) != -1)){
            buff = mas.indexOf("\"")
            mas.splice(buff, 1)
        }
        else if (str[i] == "\""){
            mas.push(str[i])
        }
    }
    return mas
}

