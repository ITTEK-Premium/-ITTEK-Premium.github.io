import js
from pyodide import create_proxy
import json

def get_item_type(item):

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


def add_tab_listener(tabName, event):
    convertButton = js.document.getElementById("tab-" + tabName)
    cc = create_proxy(event)
    convertButton.addEventListener("click", cc)


def get_selected_tab():
    tablinks = js.document.getElementsByClassName("tablinks")
    selectedTab = "all"
    for tab in tablinks:
        if ("active" in tab.className):
            selectedTab = tab.id
            selectedTab = selectedTab.replace("selected", "")
            selectedTab = selectedTab.replace(" ", "")
            selectedTab = selectedTab.replace("tab-", "")
    
    return selectedTab


def select_tab(tabName):
    tablinks = js.document.getElementsByClassName("tablinks")
    for tab in tablinks:
        if (tab.id == "tab-" + tabName):
            js.document.getElementById(tab.id).className += " active"


def get_json_in_element(elementName): # insertJsonArea

    jsonStr = js.document.getElementById(elementName).value
    jsonStr = jsonStr.replace("\n", "")
    jsonStr = jsonStr.replace("\t", "")
    data = json.loads(jsonStr)

    return data
    

def get_class_name():
    value = js.document.getElementById("inputClassName").value

    if (value == ""):
        value = "Default"

    return value


def get_package_name():
    return js.document.getElementById("inputPackage").value

    
def get_selected_option():
    return js.document.getElementById("selectModelType").value


def set_result(result):
    js.document.getElementById('textAreaResult').value = result
    js.updateDart(result)


def find_all(a_str, sub):
    return [i for i in range(len(a_str)) if a_str.startswith(sub, i)]