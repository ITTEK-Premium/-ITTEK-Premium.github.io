from utils import *
import dbReader
import dotNetFrameWork6
import js, json


def download_api(event):

    api_name = js.getApiName()
    db_data = js.getSelectedDbData()
    db_name = dbReader.get_db_name(db_data)
    tables = dbReader.get_db_tables(db_data)
    extension = ".cs"
    models = []
    controllers = []
    context = None

    # for each table create a model
    for table in tables:

        # Create Model
        code = dotNetFrameWork6.get_model(api_name, table["name"], table["columns"])
        filename = table["name"] + extension
        file = {"filename": filename, "code": str(code)}
        models.append(file)

        # Create Controller
        code = dotNetFrameWork6.get_controller(api_name, db_name, table["name"], table["columns"])
        filename = table["name"] + "Controller" + extension
        file = {"filename": filename, "code": str(code)}
        controllers.append(file)

    # Create Context
    code = dotNetFrameWork6.get_context(api_name, db_name, tables)
    filename = db_name + "DbContext" + extension
    context = {"filename": filename, "code": str(code)}

    # Download API Files
    models_json = json.dumps(models)
    controllers_json = json.dumps(controllers)
    context_json = json.dumps(context)
    js.downloadAPI(str(models_json), str(controllers_json), str(context_json), api_name)
    
