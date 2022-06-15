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

function download() {

    const zip = new JSZip();

    zip.file("Hello.txt", "Hello World\n");

    zip.generateAsync({type:"blob"}).then(function(content) {
        saveAs(content, "model.zip");
    });

  }



