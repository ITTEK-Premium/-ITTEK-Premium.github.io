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

    if (selectedOption == "kotlin" || selectedOption == "kotlin-ktor") {
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

function download(files, folderName) {

    const zip = new JSZip();

    const objects = JSON.parse(files);  
    
    for (let i = 0; i < objects.length; i++) {
      zip.file(objects[i].filename, objects[i].code);
    }

    zip.generateAsync({type:"blob"}).then(function(content) {
        saveAs(content, folderName +".zip");
    });
    
  }

function downloadAPI(models, controllers, context, custom_models, custom_controllers, db_data, folderName) {

    const zip = new JSZip();

    // Create models
    const modelObjects = JSON.parse(models);  
    for (let i = 0; i < modelObjects.length; i++) {
      zip.folder("Models").file(modelObjects[i].filename, modelObjects[i].code);
    }

    // Create controllers
    const controllerObjects = JSON.parse(controllers);  
    for (let i = 0; i < controllerObjects.length; i++) {
      zip.folder("Controllers").file(controllerObjects[i].filename, controllerObjects[i].code);
    }
    
    // Create custom models
    const customModelsObjects = JSON.parse(custom_models);  
    for (let i = 0; i < customModelsObjects.length; i++) {
      zip.folder("Models").folder("CustomModels").file(customModelsObjects[i].filename, customModelsObjects[i].code);
    }
    
    // Create custom controllers
    const customControllersObjects = JSON.parse(custom_controllers);  
    for (let i = 0; i < customControllersObjects.length; i++) {
      zip.folder("Controllers").folder("CustomControllers").file(customControllersObjects[i].filename, customControllersObjects[i].code);
    }

    // Create context
    const contextObject = JSON.parse(context);  
    zip.folder("Context").file(contextObject.filename, contextObject.code);

    // Create dbData json file
    // const dbDataObject = JSON.parse(db_data);  
    // zip.file(dbDataObject.filename, dbDataObject.code);

    zip.generateAsync({type:"blob"}).then(function(content) {
        saveAs(content, folderName +".zip");
    });
    
  }


  function downloadAPI6(models, controllers, context, custom_models, custom_controllers, launch_settings, app_settings, app_settings_dev, program, project_file, middleware, readme, folderName) {

    const zip = new JSZip();

    // Create models
    const modelObjects = JSON.parse(models);  
    for (let i = 0; i < modelObjects.length; i++) {
      zip.folder("Models").file(modelObjects[i].filename, modelObjects[i].code);
    }

    // Create controllers
    const controllerObjects = JSON.parse(controllers);  
    for (let i = 0; i < controllerObjects.length; i++) {
      zip.folder("Controllers").file(controllerObjects[i].filename, controllerObjects[i].code);
    }
    
    // Create custom models
    const customModelsObjects = JSON.parse(custom_models);  
    for (let i = 0; i < customModelsObjects.length; i++) {
      zip.folder("Models").folder("StoredProcedures").file(customModelsObjects[i].filename, customModelsObjects[i].code);
    }
    
    // Create custom controllers
    const customControllersObjects = JSON.parse(custom_controllers);  
    for (let i = 0; i < customControllersObjects.length; i++) {
      zip.folder("Controllers").folder("StoredProcedures").file(customControllersObjects[i].filename, customControllersObjects[i].code);
    }

    // Create context
    const contextObject = JSON.parse(context);  
    const middlewareObject = JSON.parse(middleware);  
    zip.folder("Data").file(contextObject.filename, contextObject.code);
    zip.folder("Data").file(middlewareObject.filename, middlewareObject.code);

    // Create Properties
    const launchObject = JSON.parse(launch_settings);  
    zip.folder("Properties").file(launchObject.filename, launchObject.code);
    
    // Create App settings
    const app_settings_Object = JSON.parse(app_settings);  
    zip.file(app_settings_Object.filename, app_settings_Object.code);
    const app_settings_dev_Object = JSON.parse(app_settings_dev);  
    zip.file(app_settings_dev_Object.filename, app_settings_dev_Object.code);

    // Create Program & project
    const program_Object = JSON.parse(program);  
    zip.file(program_Object.filename, program_Object.code); 

    // Create Readme
    const readme_Object = JSON.parse(readme);  
    zip.file(readme_Object.filename, readme_Object.code); 
    
    const project_file_Object = JSON.parse(project_file);  
    zip.file(project_file_Object.filename, project_file_Object.code);

    zip.generateAsync({type:"blob"}).then(function(content) {
        saveAs(content, folderName +".zip");
    });
    
  }


function getSelectedDbData() {
  return document.getElementById('output').textContent;
}

function getApiName() {
  var value = document.getElementById('inputClassName').value

  if (value == "")
    return "Default"

  return (value != null) ? value : "Default";
}

function getConnectionString() {
  var value = document.getElementById('inputConnectionString').value
  if (value == "")
    return "MISSING"
  return (value != null) ? value : "MISSING";
}

function getApiType() {
  return document.getElementById('selectApiType').value;
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
