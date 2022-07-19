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
    result += "import io.ktor.client.request.*\n"
    result += "import io.ktor.client.statement.*\n"
    result += "import kotlinx.serialization.SerialName\n"
    result += "import kotlinx.serialization.Serializable\n\n"

    return result


def generate_kotlin_model_code(className, data):
    text = ""
    text += "@Serializable\n"
    text += "data class "+className+"(\n"

    for item in data:
        item_type = get_item_type(data[item])
        text += "\t@SerialName(\""+str(item)+"\")\n"
        text += "\tvar "+str(item)+": "+item_type+"? = null,\n"
    
    text += ")\n"
    text += "\n"

    text += "suspend fun response"+className+"("

    
    # for item in data:
    #     text += item[]"nome: tipo,"

    text += "suspend fun response"+className+"( --- onComplete: () -> Unit) {\n"
    text += "\tval req: HttpResponse = client.post(\"http://${defaultDataRequest}/api/"+className+"\") {\n"
    text += "\t\tsetBody("+className+"(1, 1, 1))\n"
    text += "\t}\n"
    text += "\tprintln(req.status)\n"
    text += "\tonComplete()\n"
    text += "}\n"

    return text


def generate_kotlin_all_model_code(className, data):

    text = ""
    text += "@Serializable\n"
    text += "data class "+className+"(\n"

    for item in data:
        item_type = get_item_type(data[item])
        text += "\t@SerialName(\""+str(item)+"\")\n"
        text += "\tvar "+str(item)+": "+item_type+"? = null,\n"
    
    text += ")\n"
    text += "\n"

    text += "suspend fun response"+className+"("

    
    # for item in data:
    #     text += item[]"nome: tipo,"

    text += "suspend fun response"+className+"("
    
    for item in data:
        item_type = get_item_type(data[item])
        text += str(item).lower() + ": " + item_type + ", "
    text += "onComplete: () -> Unit) {\n"

    text += "\tval req: HttpResponse = client.post(\"http://${defaultDataRequest}/api/"+className+"\") {\n"
    text += "\t\tsetBody("+className+"("
    for index, item in enumerate(data):
        text += str(item).lower()
        if (index < len(data)-1):
            text += ", "

    text += "))\n"
    text += "\t}\n"
    text += "\tprintln(req.status)\n"
    text += "\tonComplete()\n"
    text += "}\n"

    return text
