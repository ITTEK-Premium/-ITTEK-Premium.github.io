from js import document
from utils import *
from tabManager import get_tabs

# This script contains functions to generate flutter (dart) code

def get_flutter_code(selected_tab):

    class_name = get_class_name()
    data = get_json_in_element("insertJsonArea")
    tabs = get_tabs(data)
    full_code = ""

    # Generate List Code
    try:
        for tab in tabs:
            try:
                full_code += generate_flutter_model_code(tab["name"], tab["body"])
            except:
                full_code += generate_flutter_model_code(tab["name"], tab["body"])

        # Generate Base Code
        if (selected_tab == class_name):
            full_code = generate_flutter_model_code(class_name, data)
        elif (selected_tab == "all"):
            full_code += generate_flutter_all_model_code(class_name, data)
        elif (selected_tab == "service"):
            full_code = generate_flutter_get_service(class_name)
        else:
            # Find Class inside json
            for tab in tabs:
                if (tab["name"] == selected_tab):
                    full_code = generate_flutter_model_code(tab["name"], tab["body"])
    except:
        for item in data[0]:
            if (get_item_type(data[0][item]) == "list"):
                fullCode += generate_flutter_model_code(item, data[0][item][0])

        # Generate Base Code
        if (selected_tab == class_name):
            fullCode = generate_flutter_model_code(class_name, data[0])
        elif (selected_tab == "all"):
            fullCode += generate_flutter_all_model_code(class_name, data[0])
        else:
            fullCode = generate_flutter_model_code(selected_tab, data[0][selected_tab][0])

    return full_code


def generate_flutter_model_code(class_name, data):

    model_code = "class " + str(class_name).capitalize() + " {\n\t"
    
    for item in data:
        item_type = get_item_type(data[item])
        if (item_type == "list"):
            item_type = "List<" + str(item).capitalize() + ">"
        elif (item_type == "dict"):
            item_type = str(item).capitalize()
        model_code += "final " + item_type +" " + item + ";\n\t"

    model_code += "\n\tconst " + str(class_name).capitalize() + "({"
    
    for item in data:
        model_code += "\n\t\trequired this." + item + ","

    model_code += "\n\t});\n\n\t"
    model_code += "factory " + str(class_name).capitalize() + ".fromJson(Map<String, dynamic> json) {\n\t\t"
    model_code += "return " + str(class_name).capitalize() + "("
    
    for item in data:
        item_type = get_item_type(data[item])
        if (item_type == "list" or item_type == "dict"):
            model_code += "\n\t\t\t" + item + ": _" + item + ","
        else:
            model_code += "\n\t\t\t" + item + ": json['" + item + "'],"
    
    model_code += "\n\t\t);\n\t"
    model_code += "}\n\n\t"
    model_code += "Map<String, dynamic> toJson() => {"
    
    for item in data:
        model_code += "\n\t\t'" + item + "': " + item + ","

    model_code += "\n\t};\n"
    model_code += "}\n\n"

    return model_code


def generate_flutter_all_model_code(class_name, data):

    model_code = "class " + str(class_name).capitalize() + " {\n\t"
    
    for item in data:
        item_type = get_item_type(data[item])
        if (item_type == "list"):
            item_type = "List<" + str(item).capitalize() + ">"
        elif (item_type == "dict"):
            item_type = str(item).capitalize()
        model_code += "final " + item_type +" " + item + ";\n\t"

    model_code += "\n\tconst " + str(class_name).capitalize() + "({"
    
    for item in data:
        model_code += "\n\t\trequired this." + item + ","

    model_code += "\n\t});\n\n\t"
    model_code += "factory " + str(class_name).capitalize() + ".fromJson(Map<String, dynamic> json) {\n\t\t"

    
    for item in data:
        item_type = get_item_type(data[item])
        if (item_type == "list" or item_type == "dict"):
            model_code += "var " + item + "JsonArray = json['" + item + "'] as List;\n\n\t\t"

    for item in data:
        item_type = get_item_type(data[item])
        if (item_type == "list" or item_type == "dict"):
            model_code += "List<" + item + "> _" + item + " = List<" + item + ">.from(\n\t\t\t"
            model_code += "" + item + "JsonArray\n\t\t\t\t"
            model_code += ".map((json) => " + item + ".fromJson(json))\n\t\t\t\t"
            model_code += ".toList());\n\n\t\t"

    model_code += "return " + str(class_name).capitalize() + "("
    
    for item in data:
        item_type = get_item_type(data[item])
        if (item_type == "list" or item_type == "dict"):
            model_code += "\n\t\t\t" + item + ": _" + item + ","
        else:
            model_code += "\n\t\t\t" + item + ": json['" + item + "'],"
    
    model_code += "\n\t\t);\n\t"
    model_code += "}\n\n\t"
    model_code += "Map<String, dynamic> toJson() => {"
    
    for item in data:
        model_code += "\n\t\t'" + item + "': " + item + ","

    model_code += "\n\t};\n"
    model_code += "}\n\n"

    return model_code


def generate_flutter_get_service(class_name):

    service_code = ""
    service_code += "// Here we want to receive a GET of API\n"
    service_code += "// We take the body formatted in JSON and transform to a List of " + class_name + "\n"
    service_code += "import 'dart:convert';\n"
    service_code += "import 'package:http/http.dart' as http;\n"
    service_code += "import '../../models/*';\n"
    service_code += "import '../../constants/app_constants.dart';\n"
    service_code += "\n"
    service_code += "Future<List<" + class_name + ">> fetch" + class_name + "() async {\n"
    service_code += "	print('RESPONSE BODY');\n"
    service_code += "\n"
    service_code += "	// Internal LINK = http://10.0.10.139:5000/api/" + class_name + "\n"
    service_code += "	final response =\n"
    service_code += "	await http.get(Uri.parse('${internal_link}" + class_name + "'));\n"
    service_code += "	print(response.statusCode);\n"
    service_code += "\n"
    service_code += "	if (response.statusCode >= 200 && response.statusCode < 300) {\n"
    service_code += "		// If the server did return a 200 OK response,\n"
    service_code += "		// then parse the JSON.\n"
    service_code += "		print('positive response');\n"
    service_code += "\n"
    service_code += "		List<dynamic> body = jsonDecode(response.body);\n"
    service_code += "		List<" + class_name + "> _" + class_name + " = body\n"
    service_code += "				.map(\n"
    service_code += "					(dynamic item) => " + class_name + ".fromJson(item),\n"
    service_code += "		)\n"
    service_code += "				.toList();\n"
    service_code += "\n"
    service_code += "		print(body);\n"
    service_code += "\n"
    service_code += "		return _" + class_name + ";\n"
    service_code += "	} else {\n"
    service_code += "		// If the server did not return a 200 OK response,\n"
    service_code += "		// then throw an exception.\n"
    service_code += "		print('Failed to load " + class_name + "');\n"
    service_code += "		throw Exception('Failed to load " + class_name + "');\n"
    service_code += "	}\n"
    service_code += "}\n"
    service_code += "\n"
    service_code += "post" + class_name + "(String description, ) async {\n"
    service_code += "	//String body = json.encode({\"active\": true});\n"
    service_code += "	var _" + class_name + " = " + class_name + "(\n"
    service_code += "		description: description,);\n"
    service_code += "	String body = json.encode(_" + class_name + ".toJson());\n"
    service_code += "\n"
    service_code += "	var response = await http.post(\n"
    service_code += "			Uri.parse(\"http://10.0.10.139:5000/api/" + class_name + "\"),\n"
    service_code += "			body: body,\n"
    service_code += "			headers: {\n"
    service_code += "				\"Accept\": \"application/json\",\n"
    service_code += "				\"content-type\": \"application/json\",\n"
    service_code += "			});\n"
    service_code += "\n"
    service_code += "	print(response.body);\n"
    service_code += "}"

    return service_code