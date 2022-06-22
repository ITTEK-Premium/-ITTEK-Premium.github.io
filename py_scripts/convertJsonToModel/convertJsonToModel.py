from utils import *
from convertToFlutter import get_flutter_code
from convertToKotlin import get_kotlin_code
from tabManager import create_tabs, get_tabs

# Main function of the convert json to model functionality
def convert_json(event):
    
    # Get Selected Variables
    selected_tab = get_selected_tab()
    selected_option = get_selected_option()

    # Create Tabs
    create_tabs(selected_tab, selected_option, convert_json)

    # Get Code
    if (selected_option == "flutter"):
        set_result(get_flutter_code(selected_tab))
    elif (selected_option == "kotlin"):
        set_result(get_kotlin_code(selected_tab))


def download_files(event):

    data = get_json_in_element("insertJsonArea")
    selected_option = get_selected_option()
    class_name = get_class_name()
    tabs = get_tabs(data)
    extension = ".dart" if (selected_option == "flutter") else ".kt"
    files = []
    
    # Download All class
    if (len(tabs) != 0):
        code = get_flutter_code("all") if (selected_option == "flutter") else get_kotlin_code("all")
        filename = class_name + extension
        files.append({"filename": str(filename), "code": str(code)})

    # Download Main class
    code = get_flutter_code(class_name) if (selected_option == "flutter") else get_kotlin_code(class_name)
    code = get_flutter_code(class_name)
    
    if (len(tabs) != 0):
        filename = class_name + " (base class)" + extension
    else:
        filename = class_name + extension

    files.append({"filename": str(filename), "code": str(code)})

    # Donwload Service
    if (selected_option == "flutter"):
        code = get_flutter_code("service")
        filename = "Service" + extension
        files.append({"filename": str(filename), "code": str(code)})

    # Download Sub classes
    for tab in tabs: 
        code = get_flutter_code(tab["name"]) if (selected_option == "flutter") else get_kotlin_code(tab["name"])
        filename = tab["name"] + extension
        files.append({"filename": str(filename), "code": str(code)})

    result = json.dumps(files)
    js.download(str(result))
