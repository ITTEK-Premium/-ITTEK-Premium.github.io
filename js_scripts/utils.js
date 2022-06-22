function copyToClipBoard() {
    /* Get the text field */
    var copyText = document.getElementById("textAreaResult");

    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */

    /* Copy the text inside the text field */
    navigator.clipboard.writeText(copyText.value);
}

function changeModelType() {
    selectModelType = document.getElementById("selectModelType")
    selectedOption = selectModelType.value

    if (selectedOption == "kotlin") {
        document.getElementById("inputPackage").style.display = 'block';
    }
    else {
        document.getElementById("inputPackage").style.display = 'none';
    }
}

function openTab(evt) {
    var i, tablinks;

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    evt.currentTarget.className += " active";
}

function download(files) {


    const zip = new JSZip();

    const objects = JSON.parse(files);  
    
    /*
    for (let i = 0; i < objects.length; i++) {
      console.log(`${i} id:${objects[i].filename}, name:${objects[i].code}`)
    }*/

    
    for (let i = 0; i < objects.length; i++) {
      zip.file(objects[i].filename, objects[i].code);
    }

    zip.generateAsync({type:"blob"}).then(function(content) {
        saveAs(content, "model.zip");
    });
    
  }


// Code Highlights

function updateJson(text) {
    let result_element = document.querySelector("#highlighting-content-json");
    // Handle final newlines (see article)
    if(text[text.length-1] == "\n") {
      text += " ";
    }
    // Update code
    result_element.innerHTML = text.replace(new RegExp("&", "g"), "&amp;")
                                    .replace(new RegExp("<", "g"), "&lt;"); 
                                    
                                    
                                    /* Global RegExp */
    
    // Syntax Highlight
    Prism.highlightElement(result_element);
  }

  function updateDart(text) {
    let result_element = document.querySelector("#highlighting-content-dart");
    // Handle final newlines (see article)
    if(text[text.length-1] == "\n") {
      text += " ";
    }
    // Update code
    result_element.innerHTML = text.replace(new RegExp("&", "g"), "&amp;")
                                    .replace(new RegExp("<", "g"), "&lt;"); 
                                    
                                    
                                    /* Global RegExp */
    
    // Syntax Highlight
    Prism.highlightElement(result_element);
  }
  
  function sync_scroll(element) {
    /* Scroll result to scroll coords of event - sync with textarea */
    let result_element = document.querySelector("#highlighting-json");
    // Get and set x and y
    result_element.scrollTop = element.scrollTop;
    result_element.scrollLeft = element.scrollLeft;
  }
  
  function sync_scroll_dart(element) {
    /* Scroll result to scroll coords of event - sync with textarea */
    let result_element = document.querySelector("#highlighting-dart");
    // Get and set x and y
    result_element.scrollTop = element.scrollTop;
    result_element.scrollLeft = element.scrollLeft;
  }

  function check_tab(element, event) {
    let code = element.value;
    if(event.key == "Tab") {
      /* Tab key pressed */
      event.preventDefault(); // stop normal
      let before_tab = code.slice(0, element.selectionStart); // text before tab
      let after_tab = code.slice(element.selectionEnd, element.value.length); // text after tab
      let cursor_pos = element.selectionEnd + 1; // where cursor moves after tab - moving forward by 1 char to after tab
      element.value = before_tab + "\t" + after_tab; // add tab char
      // move cursor
      element.selectionStart = cursor_pos;
      element.selectionEnd = cursor_pos;
      update(element.value); // Update text to include indent
    }
  }
