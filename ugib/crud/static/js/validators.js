window.addEventListener('load', (event) => {
    let dv = document.getElementById("valid_div");
    let all_input = dv.getElementByTagName("input")
    for (const i in all_input){
        console.log(all_input[i].innerText)
    }
  });
