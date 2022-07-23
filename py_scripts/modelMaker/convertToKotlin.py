from js import document
from utils import *
import json

def get_kotlin_code(selectedTab):
    
    className = get_class_name()
    data = get_json_in_element("insertJsonArea")
    packageName = get_package_name()
    fullCode = generate_imports(packageName)
    
    # Generate List Code
    try:
        for item in data:
            if (get_item_type(data[item]) == "list"):
                fullCode += generate_kotlin_model_code(item, data[item][0])

        # Generate Base Code
        if (selectedTab == className):
            fullCode = generate_kotlin_model_code(className, data)
        elif (selectedTab == "all"):
            fullCode += generate_kotlin_all_model_code(className, data)
        else:
            fullCode = generate_kotlin_model_code(selectedTab, data[selectedTab][0])
    except:
        for item in data[0]:
            if (get_item_type(data[0][item]) == "list"):
                fullCode += generate_kotlin_model_code(item, data[0][item][0])

        # Generate Base Code
        if (selectedTab == className):
            fullCode = generate_kotlin_model_code(className, data[0])
        elif (selectedTab == "all"):
            fullCode += generate_kotlin_all_model_code(className, data[0])
        else:
            fullCode = generate_kotlin_model_code(selectedTab, data[0][selectedTab][0])


    return fullCode


def generate_imports(packageName):
    result = "package " + packageName + ".models\n\n"
    result += "import org.json.JSONObject\n\n"
    return result


def generate_kotlin_model_code(className, data):

    result = "class " + className + " {\n\t"

    for item in data:
        item_type = get_item_type(data[item])
        if (item_type != "list"):
            result += "\n\tvar " + item + ": " + item_type + "? = null"

    result += "\n\n\tconstructor(){\n\t"
    result += "}\n\n\t"
    result += "constructor(\t\t"

    for item in data:
        item_type = get_item_type(data[item])
        if (item_type != "list"):
            result += "\n\t\t" + item + ": " + item_type + ","

    result += "\n\t){\t\t"

    for item in data:
        item_type = get_item_type(data[item])
        if (item_type != "list"):
            result += "\n\t\tthis." + item + " = " + item

    result += "\n\t}\n\n\t"
    result += "companion object {\n\t\t"
    result += "fun fromJson(jsonObject: JSONObject) : " + className + " {\n\t\t\t"
    result += "val " + str("_" + className).lower() + " = " + className + "()\n\n\t\t\t"

    for item in data:
        item_type = get_item_type(data[item])
        if (item_type != "list"):
            result += "" + str("_" + className).lower() + "." + item + " = if (!jsonObject.isNull(\"" + item + "\")) jsonObject.get" + item_type.capitalize() + "(\"" + item + "\") else null\n\t\t\t"
    
    result += "\n\t\t\treturn " + str("_" + className).lower() + "\n\t\t"
    result += "}\n\t"
    result += "}\n\n"
    result += "}\n\n"

    return result


def generate_kotlin_all_model_code(className, data):

    result = "class " + className + " {\n\t"

    for item in data:
        item_type = get_item_type(data[item])
        if (item_type == "list"):
            item_type = "ArrayList<" + item + ">"
            result += "\n\tvar " + item + ": " + item_type + "? = null"
        else:
            result += "\n\tvar " + item + ": " + item_type + "? = null"

    result += "\n\n\tconstructor(){\n\t"
    result += "}\n\n\t"
    result += "constructor(\t\t"

    for item in data:
        item_type = get_item_type(data[item])
        if (item_type != "list"):
            result += "\n\t\t" + item + ": " + get_item_type(data[item]) + ","

    result += "\n\t){\t\t"

    for item in data:
        item_type = get_item_type(data[item])
        if (item_type == "list"):
            result += "\n\t\tthis." + item + " = arrayListOf()"
        else:
            result += "\n\t\tthis." + item + " = " + item

    result += "\n\t}\n\n\t"
    result += "companion object {\n\t\t"
    result += "fun fromJson(jsonObject: JSONObject) : " + className + " {\n\t\t\t"
    result += "val " + str("_" + className).lower() + " = " + className + "()\n\n\t\t\t"

    # Create Basic From Json
    for item in data:
        item_type = get_item_type(data[item])
        if (item_type != "list"):
            result += "" + str("_" + className).lower() + "." + item + " = if (!jsonObject.isNull(\"" + item + "\")) jsonObject.get" + get_item_type(data[item]).capitalize() + "(\"" + item + "\") else null\n\t\t\t"
        
    # Create From Json to Lists
    for item in data:
        item_type = get_item_type(data[item])
        if (item_type == "list"):
            result += "\n\t\t\tval " + item + "JsonArray = (if (!jsonObject.isNull(\"" + item + "\")) jsonObject.getJSONArray(\"" + item + "\") else null) ?: return "+str("_" + className).lower()+"\n\t\t\t"

            result += "\n\t\t\tfor (i in 0 until " + item + "JsonArray.length()) {\n\t\t\t\t"
            result += "val _" + item + "Json = " + item + "JsonArray.getJSONObject(i)\n\t\t\t\t"
            result += "val _" + item + " = " + item + ".fromJson(_" + item + "Json)\n\n\t\t\t\t"
            result += "_" + className + "." + item + "!!.add(_" + item + ")\n\t\t\t"
            result += "}\n\t\t\t"

    result += "\n\t\t\treturn " + str("_" + className).lower() + "\n\t\t"
    result += "}\n\t"
    result += "}\n\n"
    result += "}\n\n"

    return result
