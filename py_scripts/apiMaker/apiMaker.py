from utils import *
from dbReader import get_db_json
import dotNetFrameWork6
import js, json


def create_api(event):
        
    # db_data = js.getSelectedDbData()

    # result = get_db_json(db_data)
    # print(result)

    pass


def download_api(event):

    db_data = js.getSelectedDbData()
    tables = get_db_json(db_data)
    extension = ".cs"
    models = []
    controllers = []
    context = None

    # for each table create a model
    for table in tables:

        # Create Model
        code = dotNetFrameWork6.get_model(table["name"], table["columns"])
        filename = table["name"] + extension
        file = {"filename": filename, "code": str(code)}
        models.append(file)

        # Create Controller
        code = dotNetFrameWork6.get_controller(table["name"], table["columns"])
        filename = table["name"] + "Controller" + extension
        file = {"filename": filename, "code": str(code)}
        controllers.append(file)


    models_json = json.dumps(models)
    controllers_json = json.dumps(controllers)
    js.downloadAPI(str(models_json), str(controllers_json), "api")


