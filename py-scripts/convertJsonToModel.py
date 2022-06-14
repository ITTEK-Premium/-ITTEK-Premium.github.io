from js import document
from pyodide import create_proxy
import json

def convertJson(event):
    textAreaResult = document.getElementById('textAreaResult')
    selectedOption = document.getElementById("selectModelType").value
    result = ""

    # Get Selected Tab
    selectedTab = getSelectedTab()

    if (selectedOption == "flutter"):
        result = convertToFlutter(selectedTab)
    elif (selectedOption == "kotlin"):
        result = convertToKotlin()

    textAreaResult.value = result


def convertToFlutter(selectedTab):

    className = document.getElementById("inputClassName").value
    jsonStr = document.getElementById('insertJsonArea').value
    jsonStr = jsonStr.replace("\n", "")
    jsonStr = jsonStr.replace("\t", "")
    document.querySelector("#tabMenu").innerHTML = ""; 
    data = json.loads(jsonStr)
    fullCode = ""
    html = ""
    htmlList = ""
    tabItems = []

    # Create Tabs
    for item in data:
        if (getItemType(data[item]) == "list"):
            htmlList += "<button id=\"tab-" + item + "\" class=\"tablinks\" onclick=\"openTab(event)\">" + item + "</button>"
            tabItems.append({"name": item, "body":data[item][0]})

    if (htmlList == ""):
        html += "<button id=\"tab-" + className + "\" class=\"tablinks\" onclick=\"openTab(event)\">" + className + "</button>"

        document.querySelector("#tabMenu").innerHTML += html; 
        addTabListener(className)
    
    # List Code Needed
    else:
        html += "<button id=\"tab-all\" class=\"tablinks\" onclick=\"openTab(event)\">All</button>"
        html += "<button id=\"tab-" + className + "\" class=\"tablinks\" onclick=\"openTab(event)\">" + className + "</button>"
        html += htmlList

        document.querySelector("#tabMenu").innerHTML += html; 

        addTabListener("all")
        addTabListener(className)

        # Generate List Code for All Tab
        for item in tabItems:
            addTabListener(item["name"])
            fullCode += generateFlutterModelCode(item["name"], item["body"])

    # Generate Base Code
    if (selectedTab == className):
        fullCode = generateFlutterModelCode(className, data)
    elif (selectedTab == "all"):
        fullCode += generateFlutterModelCode(className, data)
    else:
        fullCode = generateFlutterModelCode(selectedTab, data[selectedTab][0])

    SelectTab(selectedTab)
    return fullCode


def generateFlutterModelCode(className, data):

    model_code = "class " + className + " {\n\t"
    
    for item in data:
        model_code += "final " + getItemType(data[item]) +" " + item + ";\n\t"

    model_code += "\n\tconst " + className + "({"
    
    for item in data:
        model_code += "\n\t\trequired this." + item + ","

    model_code += "\n\t});\n\n\t"
    model_code += "factory " + className + ".fromJson(Map<String, dynamic> json) {\n\t\t"
    model_code += "return " + className + "("
    
    for item in data:
        model_code += "\n\t\t\t" + item + ": json['" + item + "'],"
    
    model_code += "\n\t\t);\n\t"
    model_code += "}\n\n\t"
    model_code += "Map<String, dynamic> toJson() => {"
    
    for item in data:
        model_code += "\n\t\t'" + item + "': " + item + ","

    model_code += "\n\t};\n"
    model_code += "}\n\n"

    return model_code


def convertToKotlin():
    className = document.getElementById("inputClassName").value
    packageName = document.getElementById("inputPackage").value
    jsonStr = document.getElementById('insertJsonArea').value
    jsonStr = jsonStr.replace("\n", "")
    jsonStr = jsonStr.replace("\t", "")
    data = json.loads(jsonStr)

    result = "package " + packageName + ".models\n\n"
    result += "import org.json.JSONObject\n\n"
    result += "class " + className + " {\n\t"

    for item in data:
        result += "\n\tvar " + item + ": " + getItemType(data[item]) + "? = null"

    result += "\n\n\tconstructor(){\n\t"
    result += "}\n\n\t"
    result += "constructor(\t\t"

    for item in data:
        result += "\n\t\t" + item + ": " + getItemType(data[item]) + ","

    result += "\n\t){\t\t"

    for item in data:
        result += "\n\t\tthis." + item + " = " + item

    result += "\n\t}\n\n\t"
    result += "companion object {\n\t\t"
    result += "fun fromJson(jsonObject: JSONObject) : " + className + " {\n\t\t\t"
    result += "val " + str("_" + className).lower() + " = " + className + "()\n\n\t\t\t"

    for item in data:
        result += "" + str("_" + className).lower() + "." + item + " = if (!jsonObject.isNull(\"" + item + "\")) jsonObject.get" + getItemType(data[item]).capitalize() + "(\"" + item + "\") else null\n\t\t\t"
    
    result += "\n\t\t\treturn " + str("_" + className).lower() + "\n\t\t"
    result += "}\n\t"
    result += "}\n\n"
    result += "}"
    
    return result


def getItemType(item):

    itemType = type(item)
    itemType = str(itemType)
    itemType = itemType.replace("<", "")
    itemType = itemType.replace(">", "")
    itemType = itemType.replace("'", "")
    itemType = itemType.replace(" ", "")
    itemType = itemType.replace("class", "")
    
    if (itemType == "str"):
        itemType = "String"

    return itemType


def addTabListener(tabName):
    convertButton = document.getElementById("tab-" + tabName)
    cc = create_proxy(convertJson)
    convertButton.addEventListener("click", cc)


def getSelectedTab():
    tablinks = document.getElementsByClassName("tablinks")
    selectedTab = "all"
    for tab in tablinks:
        if ("active" in tab.className):
            selectedTab = tab.id
            selectedTab = selectedTab.replace("selected", "")
            selectedTab = selectedTab.replace(" ", "")
            selectedTab = selectedTab.replace("tab-", "")
    
    return selectedTab


def SelectTab(tabName):
    tablinks = document.getElementsByClassName("tablinks")
    for tab in tablinks:
        if (tab.id == "tab-" + tabName):
            document.getElementById(tab.id).className += " active"
