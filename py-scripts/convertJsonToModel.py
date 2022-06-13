from js import document
import json

'''
primeiro procurar por listas.

para cada lista cria uma classe para ela em cima


modificar from json com 

List<Certificates> _certificates = List<Certificates>.from(
        certificatesJsonArray
            .map((json) => Certificates.fromJson(json))
            .toList());

e 

certificates: _certificates,
'''

def convertJson(event):
    textAreaResult = document.getElementById('textAreaResult')
    selectModelType = document.getElementById("selectModelType")
    selectedOption = selectModelType.value

    result = ""

    if (selectedOption == "flutter"):
        result = convertToFlutter()
    elif (selectedOption == "kotlin"):
        result = convertToKotlin()

    textAreaResult.value = result


def convertToFlutter():

    className = document.getElementById("inputClassName").value
    jsonStr = document.getElementById('insertJsonArea').value
    jsonStr = jsonStr.replace("\n", "")
    jsonStr = jsonStr.replace("\t", "")
    data = json.loads(jsonStr)

    result = "class " + className + " {\n\t"
    
    for item in data:
        result += "final " + getItemTypeDart(data[item]) +" " + item + ";\n\t"

    result += "\n\tconst " + className + "({"
    
    for item in data:
        result += "\n\t\trequired this." + item + ","

    result += "\n\t});\n\n\t"
    result += "factory " + className + ".fromJson(Map<String, dynamic> json) {\n\t\t"
    result += "return " + className + "("
    
    for item in data:
        result += "\n\t\t\t" + item + ": json['" + item + "'],"
    
    result += "\n\t\t);\n\t"
    result += "}\n\n\t"
    result += "Map<String, dynamic> toJson() => {"
    
    for item in data:
        result += "\n\t\t'" + item + "': " + item + ","

    result += "\n\t};\n"
    result += "}"

    return result


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
        result += "\n\tvar " + item + ": " + getItemTypeKotlin(data[item]) + "? = null"

    result += "\n\n\tconstructor(){\n\t"
    result += "}\n\n\t"
    result += "constructor(\t\t"

    for item in data:
        result += "\n\t\t" + item + ": " + getItemTypeKotlin(data[item]) + ","

    result += "\n\t){\t\t"

    for item in data:
        result += "\n\t\tthis." + item + " = " + item

    result += "\n\t}\n\n\t"
    result += "companion object {\n\t\t"
    result += "fun fromJson(jsonObject: JSONObject) : " + className + " {\n\t\t\t"
    result += "val " + str("_" + className).lower() + " = " + className + "()\n\n\t\t\t"

    for item in data:
        result += "" + str("_" + className).lower() + "." + item + " = if (!jsonObject.isNull(\"" + item + "\")) jsonObject.get" + getItemTypeKotlin(data[item]).capitalize() + "(\"" + item + "\") else null\n\t\t\t"
    
    result += "\n\t\t\treturn " + str("_" + className).lower() + "\n\t\t"
    result += "}\n\t"
    result += "}\n\n"
    result += "}"
    
    return result


def getItemTypeDart(item):

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


def getItemTypeKotlin(item):

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