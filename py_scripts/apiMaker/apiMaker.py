####################################################
## Py-Script Documentation -> https://github.com/pyscript/pyscript/blob/main/docs/tutorials/getting-started.md

# Abstract: Library with the purpose of downloading any type of API. Currently available only .NET Framework 5.0 & 6.0
# Author: André Cerqueira
# Start Date: 25/06/2022
# Last Update Date: 13/07/2022
# Current Version: 2.1

####################################################


####################################################
## 1. Imports
####################################################  


from utils import *
import dbReader
import dotNetFrameWork6
import js, json
EXTENSION = ".cs" # FOR NOW ALL THE CODE DONE HERE WAS DONE ASSUMING .NET FRAMEWORK 6.0 IS SELECTED



####################################################
## 2. Download API
####################################################  



### Download API based on a selected API and Database ###
## Parameters
# 1. @event = event of download button clicked
def download_api(event):

    # Get data in data base
    api_name = js.getApiName()
    api_type = js.getApiType()
    db_data = js.getSelectedDbData()
    connection_string = js.getConnectionString()
    db_name = dbReader.get_name(db_data)
    tables = dbReader.get_tables(db_data)
    stored_procedures = dbReader.get_stored_procedures(db_data, tables)
    
    # Generate API
    models = get_models(api_name, api_type, tables)
    controllers = get_controllers(api_name, api_type, db_name, tables)
    custom_models = get_custom_models(db_data, tables, api_name, api_type, stored_procedures)
    custom_controllers = get_custom_controllers(db_data, tables, api_name, api_type, db_name, stored_procedures)
    context = get_context(api_name, api_type, db_name, tables, stored_procedures)

    # Download API Files
    models_json = json.dumps(models)
    controllers_json = json.dumps(controllers)
    context_json = json.dumps(context)
    custom_models_json = json.dumps(custom_models)
    custom_controllers_json = json.dumps(custom_controllers)
    db_data = json.dumps({"filename": "storedProcedures.json", "code": str(stored_procedures)})
    
    # [Temporary Code] if version 6 build with other files
    if (api_type == "dot-net-framework-6"):
        launch_settings = get_launch_settings_code(api_name)
        app_settings = get_app_settings_code(db_name, connection_string)
        app_settings_dev = get_app_settings_dev_code()
        program = get_program_code(api_name, db_name)
        project_file = get_project_file()
        middleware = get_middleware_code()
        readme = get_readme_code()
        launch_settings_json = json.dumps({"filename": "launchSettings.json", "code": str(launch_settings)})
        app_settings_json = json.dumps({"filename": "appsettings.json", "code": str(app_settings)})
        app_settings_dev_json = json.dumps({"filename": "appsettings.Development.json", "code": str(app_settings_dev)})
        program_json = json.dumps({"filename": "Program.cs", "code": str(program)})
        project_file_json = json.dumps({"filename": api_name+".csproj", "code": str(project_file)})
        middleware_json = json.dumps({"filename": "ApiKeyMiddleware.cs", "code": str(middleware)})
        readme_json = json.dumps({"filename": "readme.md", "code": str(readme)})

        js.downloadAPI6(str(models_json), str(controllers_json), str(context_json), str(custom_models_json), str(custom_controllers_json), str(launch_settings_json), str(app_settings_json), str(app_settings_dev_json), str(program_json), str(project_file_json), str(middleware_json), str(readme_json), api_name)
    
    else:
        
        js.downloadAPI(str(models_json), str(controllers_json), str(context_json), str(custom_models_json), str(custom_controllers_json), str(db_data), api_name)



####################################################
## 3. Generate API Files Functions
####################################################  



### Get all models files for each table in database ###
## Parameters
# 1. @api_name = API name
# 2. @api_type = API type
# 3. @tables = All tables in database
def get_models(api_name, api_type, tables):
    models = []

    for table in tables:
        code = get_model_code(api_name, api_type, table["name"], table["columns"])
        filename = table["name"] + EXTENSION
        file = {"filename": filename, "code": str(code)}
        models.append(file)

    return models


### Get all controllers files for each table in database ###
## Parameters
# 1. @api_name = API name
# 2. @api_type = API type
# 3. @db_name = Database name
# 4. @tables = All tables in database
def get_controllers(api_name, api_type, db_name, tables):
    controllers = []

    for table in tables:
        code = get_controller_code(api_name, api_type, db_name, table["name"], table["columns"])
        filename = table["name"] + "Controller" + EXTENSION
        file = {"filename": filename, "code": str(code)}
        controllers.append(file)

    return controllers


### Get all Models files for each stored procedure in database ###
## Parameters
# 1. @api_name = API name
# 2. @api_type = API type
# 3. @stored_procedures = All stored procedures in database
def get_custom_models(db_data, tables, api_name, api_type, stored_procedures):
    custom_models = []

    for sp in stored_procedures:
        sub_models = dbReader.get_queries_in_stored_procedure(db_data, tables, sp["name"])
        code = get_custom_model_code(api_name, api_type, sp["name"], sub_models)
        filename = sp["name"] + EXTENSION
        file = {"filename": filename, "code": str(code)}
        custom_models.append(file)

    return custom_models


### Get all Controllers files for each stored procedure in database ###
## Parameters
# 1. @api_name = API name
# 2. @api_type = API type
# 3. @db_name = Database name
# 4. @stored_procedures = All stored procedures in database
def get_custom_controllers(db_data, tables, api_name, api_type, db_name, stored_procedures):
    custom_controllers = []

    for sp in stored_procedures:
        sub_models = dbReader.get_queries_in_stored_procedure(db_data, tables, sp["name"])
        code = get_custom_controller_code(api_name, api_type, db_name, sp["name"], sp["columns"], sp["headers"], sub_models)
        filename = sp["name"] + "Controller" + EXTENSION
        file = {"filename": filename, "code": str(code)}
        custom_controllers.append(file)

    return custom_controllers


### Get Context file based on all tables and stored procedure  ###
## Parameters
# 1. @api_name = API name
# 2. @api_type = API type
# 3. @db_name = Database name
# 4. @tables = All tables in database
# 5. @stored_procedures = All stored procedures in database
def get_context(api_name, api_type, db_name, tables, stored_procedures):

    code = get_context_code(api_name, api_type, db_name, tables, stored_procedures)
    filename = "DbContext" + EXTENSION # db_name + 
    context = {"filename": filename, "code": str(code)}

    return context



####################################################
## 4. Generate API Scripts Functions
####################################################  



### Get model code based on the selected api type ###
## Parameters
# 1. @api_name = API name
# 2. @api_type = API type
# 3. @model_name = Database name
# 4. @columns = All Columns in the (api_name) table
def get_model_code(api_name, api_type, model_name, columns):

    models = []
    models.append({"name":model_name, "columns":columns})

    model = {
        # "dot-net-framework-5": dotNetFrameWork5.get_model(api_name, model_name, models),
        "dot-net-framework-6": dotNetFrameWork6.get_model(api_name, model_name, models, False)
    }
    return model[api_type]


### Get controller code based on the selected api type ###
## Parameters
# 1. @api_name = API name
# 2. @api_type = API type
# 3. @db_name = Database name
# 4. @model_name = Database name
# 5. @columns = All Columns in the (api_name) table
def get_controller_code(api_name, api_type, db_name, model_name, columns):
    model = {
        # "dot-net-framework-5": dotNetFrameWork5.get_controller(api_name, db_name, model_name, columns),
        "dot-net-framework-6": dotNetFrameWork6.get_controller(api_name, db_name, model_name, columns)
    }
    return model[api_type]


### Get custom model code based on the selected api type ### TODO TODO TODO TODO
## Parameters
# 1. @api_name = API name
# 2. @api_type = API type
# 3. @model_name = Database name
# 4. @columns = All Columns in the (api_name) table
# OLD - def get_custom_model_code(api_name, api_type, model_name, columns):
def get_custom_model_code(api_name, api_type, model_name, models):
    model = {
        # "dot-net-framework-5": dotNetFrameWork5.get_model(api_name, model_name, models),
        "dot-net-framework-6": dotNetFrameWork6.get_model(api_name, model_name, models, True)
    }
    return model[api_type]


### Get custom controller code based on the selected api type ### TODO TODO TODO TODO
## Parameters
# 1. @api_name = API name
# 2. @api_type = API type
# 3. @db_name = Database name
# 4. @model_name = Database name
# 5. @columns = All Columns in the (api_name) table
def get_custom_controller_code(api_name, api_type, db_name, model_name, columns, headers, models):
    model = {
        # "dot-net-framework-5": dotNetFrameWork5.get_controller(api_name, db_name, model_name, columns),
        "dot-net-framework-6": dotNetFrameWork6.get_stored_procedure_controller(api_name, db_name, model_name, columns, headers, models)
    }
    return model[api_type]


### Get context code based on the selected api type ###
## Parameters
# 1. @api_name = API name
# 2. @api_type = API type
# 3. @db_name = Database name
# 4. @tables = All tables in database
# 5. @stored_procedures = All stored procedures in database
def get_context_code(api_name, api_type, db_name, tables, stored_procedures):
    model = {
        # "dot-net-framework-5": dotNetFrameWork5.get_context(api_name, db_name, tables, stored_procedures),
        "dot-net-framework-6": dotNetFrameWork6.get_context(api_name, db_name, tables, stored_procedures)
    }
    return model[api_type]



####################################################
## 5. Generate Other API Files Functions
####################################################  



### [TEMPORARY] Get other files for version 6.0.6 of dotnet

def get_launch_settings_code(api_name):
    return dotNetFrameWork6.get_launch_settings(api_name)

def get_app_settings_code(db_name, connection_string):
    return dotNetFrameWork6.get_app_settings(db_name, connection_string)

def get_app_settings_dev_code():
    return dotNetFrameWork6.get_app_settings_dev()

def get_program_code(api_name, db_name):
    return dotNetFrameWork6.get_program(api_name, db_name)

def get_project_file():
    return dotNetFrameWork6.get_project_file()

def get_middleware_code():
    return dotNetFrameWork6.get_middleware()

def get_readme_code():
    return dotNetFrameWork6.get_readme()
