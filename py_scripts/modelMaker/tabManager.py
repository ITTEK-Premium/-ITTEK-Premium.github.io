from js import document
from utils import *
import json

# This function create tabs for each class found in the selected json
# 1. Reset all tabs
# 2. Get new tabs
# 3. Create Tabs
# 4. Select Current Tab
def create_tabs(selected_tab, selected_option, click_event):
    
    # Set Variables
    class_name = get_class_name()
    data = get_json_in_element("insertJsonArea")
    tabs = []
    html = ""

    # Delete all tabs
    document.querySelector("#tabMenu").innerHTML = ""; 

    # Get the necessary tabs
    tabs = get_tabs(data)

    # Create Tabs
    create_tabs_html(class_name, tabs, selected_option)
    create_tabs_click_events(class_name, tabs, selected_option, click_event)

    select_tab(selected_tab)


# This function returns all tabs in a json structure
def get_tabs(data):
    tabs = []

    for item in data:
        if (get_item_type(data[item]) == "list" or get_item_type(data[item]) == "dict"):
            tabs.append(get_tab(item, data))
            try:
                tabs += get_tabs(data[item][0]) 
            except:
                tabs += get_tabs(data[item]) 
            
    return tabs


# This function return the tab in the current json structure
def get_tab(item, data):
    try:
        return {"name": str(item), "body":data[item][0]}
    except:
        return {"name": str(item), "body":data[item]}


# This function create all tabs inner html
def create_tabs_html(class_name, tabs, selected_option):
    html = ""

    if (len(tabs) != 0):
        html += "<button id=\"tab-all\" class=\"tablinks\" onclick=\"openTab(event)\">All</button>"

    html += "<button id=\"tab-" + class_name + "\" class=\"tablinks\" onclick=\"openTab(event)\">" + str(class_name).capitalize() + "</button>"

    for tab in tabs:
        html += "<button id=\"tab-" + tab["name"] + "\" class=\"tablinks\" onclick=\"openTab(event)\">" + tab["name"].capitalize() + "</button>"
    
    if (selected_option == "flutter"):
        html += "<button id=\"tab-service\" class=\"tablinks\" onclick=\"openTab(event)\">Service</button>"

    document.querySelector("#tabMenu").innerHTML += html; 


# This function creates the on click event for all tabs
def create_tabs_click_events(class_name, tabs, selected_option, event):
    if (len(tabs) != 0):
        add_tab_listener("all", event)

    add_tab_listener(class_name, event)

    for tab in tabs:
        add_tab_listener(tab["name"], event)

    if (selected_option == "flutter"):
        add_tab_listener("service", event)
