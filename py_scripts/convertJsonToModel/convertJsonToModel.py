from utils import *
from convertToFlutter import get_flutter_code
from convertToKotlin import get_kotlin_code
from tabManager import create_tabs

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

    #js2py.eval_js('console.log( "Hello World!" )')

    #result = parse('window.alert(1);')

    #print(result)