from utils import *
import dbReader
import dotNetFrameWork5,dotNetFrameWork6
import js, json

# ALL THE CODE DONE HERE WAS DONE ASSUMING .NET FRAMEWORK 6.0 IS SELECTED

EXTENSION = ".cs"

def download_api(event):

    # Get data in data base
    api_name = js.getApiName()
    api_type = js.getApiType()
    db_data = js.getSelectedDbData()
    db_name = dbReader.get_name(db_data)
    tables = dbReader.get_tables(db_data)
    stored_procedures = dbReader.get_stored_procedures(db_data, tables)
    
    # Generate API
    models = get_models(api_name, api_type, tables)
    controllers = get_controllers(api_name, api_type, db_name, tables)
    custom_models = get_custom_models(api_name, api_type, stored_procedures)
    custom_controllers = get_custom_controllers(api_name, api_type, db_name, stored_procedures)
    context = get_context(api_name, api_type, db_name, tables, stored_procedures)

    # Download API Files
    models_json = json.dumps(models)
    controllers_json = json.dumps(controllers)
    context_json = json.dumps(context)
    custom_models_json = json.dumps(custom_models)
    custom_controllers_json = json.dumps(custom_controllers)
    db_data = json.dumps({"filename": "storedProcedures.json", "code": str(stored_procedures)})
    js.downloadAPI(str(models_json), str(controllers_json), str(context_json), str(custom_models_json), str(custom_controllers_json), str(db_data), api_name)
    

# Create all Models in each table
def get_models(api_name, api_type, tables):
    models = []

    for table in tables:
        code = get_model_code(api_name, api_type, table["name"], table["columns"])
        filename = table["name"] + EXTENSION
        file = {"filename": filename, "code": str(code)}
        models.append(file)

    return models


# Create all controllers in each table 
def get_controllers(api_name, api_type, db_name, tables):
    controllers = []

    for table in tables:
        code = get_controller_code(api_name, api_type, db_name, table["name"], table["columns"])
        filename = table["name"] + "Controller" + EXTENSION
        file = {"filename": filename, "code": str(code)}
        controllers.append(file)

    return controllers


# Create all Models in each stored procedure 
def get_custom_models(api_name, api_type, stored_procedures):
    custom_models = []

    for sp in stored_procedures:
        code = get_model_code(api_name, api_type, sp["name"], sp["columns"])
        filename = sp["name"] + EXTENSION
        file = {"filename": filename, "code": str(code)}
        custom_models.append(file)

    return custom_models


# Create all controllers in each stored procedure 
def get_custom_controllers(api_name, api_type, db_name, stored_procedures):
    custom_controllers = []

    for sp in stored_procedures:
        code = get_controller_code(api_name, api_type, db_name, sp["name"], sp["columns"])
        filename = sp["name"] + "Controller" + EXTENSION
        file = {"filename": filename, "code": str(code)}
        custom_controllers.append(file)

    return custom_controllers


# Create context file based on all tables and stored procedure 
def get_context(api_name, api_type, db_name, tables, stored_procedures):

    code = get_context_code(api_name, api_type, db_name, tables, stored_procedures)
    filename = "DbContext" + EXTENSION # db_name + 
    context = {"filename": filename, "code": str(code)}

    return context


# Get model code depending on the selected api type
def get_model_code(api_name, api_type, model_name, columns):
    model = {
        "dot-net-framework-5": dotNetFrameWork5.get_model(api_name, model_name, columns),
        "dot-net-framework-6": dotNetFrameWork6.get_model(api_name, model_name, columns)
    }
    return model[api_type]


# Get controller code depending on the selected api type
def get_controller_code(api_name, api_type, db_name, model_name, columns):
    model = {
        "dot-net-framework-5": dotNetFrameWork5.get_controller(api_name, db_name, model_name, columns),
        "dot-net-framework-6": dotNetFrameWork6.get_controller(api_name, db_name, model_name, columns),
    }
    return model[api_type]


# Get context code depending on the selected api type
def get_context_code(api_name, api_type, db_name, tables, stored_procedures):
    model = {
        "dot-net-framework-5": dotNetFrameWork5.get_context(api_name, db_name, tables, stored_procedures),
        "dot-net-framework-6": dotNetFrameWork6.get_context(api_name, db_name, tables, stored_procedures)
    }

    print("a versao é: " + str(api_type))

    return model[api_type]