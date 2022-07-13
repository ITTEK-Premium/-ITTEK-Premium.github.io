####################################################
## Py-Script Documentation -> https://github.com/pyscript/pyscript/blob/main/docs/tutorials/getting-started.md
## .NET FrameWork 6.0 Documentation -> https://docs.microsoft.com/en-us/dotnet/core/whats-new/dotnet-6

# Abstract: Library with all functions to build an API with .NET FrameWork 6.0.6
# Author: André Cerqueira
# Start Date: 01/07/2022
# Last Update Date: 13/07/2022
# Current Version: 1.2

####################################################


####################################################
## 1. Generate Script Code Functions
####################################################  


### Dot Net FrameWork 6.0.6 Model generated from a table from a database script ###
## Parameters
# 1. @api_name = API name
# 2. @model_name = Model name
# 3. #TODO @columns = All columns in the (api_name) table
def get_model(api_name, main_model_name, sub_models, isStoredProcedure):

    # Declare Variables
    text = ""
    isKeyless = False

    # Write Imports
    text += "using System.ComponentModel.DataAnnotations;\n"
    
    if (isStoredProcedure):
        text += "using Microsoft.EntityFrameworkCore;\n"

    text += "using Newtonsoft.Json;\n"
    text += "\n"
    if (isStoredProcedure):
        text += "namespace " + api_name + ".Models.StoredProcedures\n"
    else:
        text += "namespace " + api_name + ".Models\n"
    text += "{\n"

    # Write Class for each model in this model script
    for model in sub_models:

        # Check need for Keyless, basically check if model has Get, Add or Update in name
        isKeyless = ("get" in model["name"].lower() or "add" in model["name"].lower() or "update" in model["name"].lower())
        if (isKeyless):
            text += "\t[Keyless]\n"

        text += "\tpublic class " + model["name"] + "\n"
        text += "\t{\n"
        if (not isKeyless):
            text += "\t\t[Key]\n"

        # Write Every Variable and Variable Type
        for column in model["columns"]:
            
            var_type = get_var_type(column["type"])

            # get_name_without_first()
            text += "\t\t[JsonProperty(PropertyName = \"" + column["name"] + "\")]\n" 
            text += "\t\tpublic "+var_type+" "+column["name"]+" { get; set; }\n\n"

        # Close Model
        text += "\t}\n\n"
    
    # Create Main Model to concatenate every model if necessary
    if (len(sub_models) > 1):
        # Check need for Keyless, basically check if model has Get, Add or Update in name
        isKeyless = ("get" in main_model_name.lower() or "add" in main_model_name.lower() or "update" in main_model_name.lower())
        if (isKeyless):
            text += "\t[Keyless]\n"

        text += "\tpublic class " + main_model_name + "\n"
        text += "\t{\n"
        if (not isKeyless):
            text += "\t\t[Key]\n"

        # Write Every Variable and Variable Type
        for model in sub_models:
            
            var_name = model["name"][0].lower() + model["name"][1:]
            text += "\t\t[JsonProperty(PropertyName = \"" + var_name + "\")]\n" 
            text += "\t\tpublic List<"+model["name"]+">? "+ var_name +" { get; set; }\n\n"

        # Close Model
        text += "\t}\n\n"

    # Close Code
    text += "}"

    return text


### Dot Net FrameWork 6.0.6 Controller generated from a table from a database script ###
## Parameters
# 1. @api_name = API name
# 2. @db_name = DataBase name
# 3. @model_name = Model name
# 4. @columns = All Columns in the (api_name) table
def get_controller(api_name, db_name, model_name, columns):

    # Declare Variables
    text = ""
    first_column_name = columns[0]["name"]

    # Write Imports
    text += "using Microsoft.AspNetCore.Mvc;\n"
    text += "using Microsoft.EntityFrameworkCore;\n"
    text += "using " + api_name + ".Data;\n"
    text += "using " + api_name + ".Models;\n"
    text += "\n"
    
    # Write Namespace, Class Start and Constructors
    text += "namespace " + api_name + ".Controllers\n"
    text += "{\n"
    text += "\t[Route(\"api/[controller]\")]\n"
    text += "\t[ApiController]\n"
    text += "\tpublic class " + model_name + "Controller : ControllerBase\n"
    text += "\t{\n"
    text += "\t\tprivate readonly " + db_name + "DbContext _context;\n"
    text += "\n"
    text += "\t\tpublic " + model_name + "Controller(" + db_name + "DbContext context)\n"
    text += "\t\t{\n"
    text += "\t\t\t_context = context;\n"
    text += "\t\t}\n"
    text += "\n"

    # Write Methods
    text += get_get_all_method(model_name)
    text += get_get_by_id_method(model_name)
    text += get_put_method(model_name)
    text += get_post_method(model_name, db_name, first_column_name)
    text += get_delete_method(model_name)

    # Write Class End and Close Code
    text += "\t\t\t_context." + model_name + ".Remove(_" + model_name.lower() + ");\n"
    text += "\t\t\tawait _context.SaveChangesAsync();\n"
    text += "\n"
    text += "\t\t\treturn NoContent();\n"
    text += "\t\t}\n"
    text += "\n"
    text += "\t\tprivate bool " + model_name + "Exists(int id)\n"
    text += "\t\t{\n"
    text += "\t\t\treturn (_context." + model_name + "?.Any(e => e."+first_column_name+" == id)).GetValueOrDefault();\n"
    text += "\t\t}\n"
    text += "\t}\n"
    text += "}\n"

    return text


### Controller of dot Net FrameWork 6.0.6 ###
## Parameters
# 1. @api_name = API name
# 2. @db_name = DataBase name
# 3. @model_name = Model name
# 4. @columns = All Columns in the (api_name) table
# 5. @stored_procedures = All Stored Procedures in the Database Script
## TODO 
# 1. Read Properly -DONE
# 2. Analyse witch method use -DONE
# 3. Build Individual Controller -DONE
# 4. Get with parameters -DONE
# 5. Build Multi Model Controller
def get_stored_procedure_controller(api_name, db_name, model_name, columns, headers, sub_models):
    text = ""

    text += "using Microsoft.AspNetCore.Mvc;\n"
    text += "using Microsoft.EntityFrameworkCore;\n"
    text += "using " + api_name + ".Data;\n"
    text += "using " + api_name + ".Models.StoredProcedures;\n"
    text += "using System.Data;\n"
    text += "\n"
    text += "namespace " + api_name + ".Controllers.StoredProcedures\n"
    text += "{\n"

    # Set Default Route
    if (headers == None):
        text += "\t[Route(\"api/[controller]\")]\n"
    # Set Route with all headers
    else:
        text += "\t[Route(\"api/[controller]/"
        for index, header in enumerate(headers):
            text += "{"+header["name"]+"}"
            if (index < len(headers)-1):
                text += "/"
        text += "\")]\n"

    text += "\t[ApiController]\n"
    text += "\tpublic class " + model_name + "Controller : ControllerBase\n"
    text += "\t{\n"
    text += "\t\tprivate readonly " + db_name + "DbContext _context;\n"
    text += "\n"
    text += "\t\tpublic " + model_name + "Controller(" + db_name + "DbContext context)\n"
    text += "\t\t{\n"
    text += "\t\t\t_context = context;\n"
    text += "\t\t}\n"
    text += "\n"

    # Check Sub Model Quantity in Store Procedure To change the code
    if (len(sub_models) > 1):

        # Create Method
        text += "\t\t// GET: api/"+model_name+"\n"
        text += "\t\t[HttpGet]\n"
        text += "\t\tpublic async Task<GetProductionScreen?> Get(\n"
        
        # Set all parameters
        if (headers != None):
            for index, header in enumerate(headers):
                type_converted = get_var_type(header["type"])
                text += type_converted +" "+header["name"]
                if (index < len(headers)-1):
                    text += ", "
        text += ")\n"
        
        text += "\t\t{\n"
        text += "\t\t\tif (_context.GetProductionScreen == null)\n"
        text += "\t\t\t{\n"
        text += "\t\t\t\treturn null;\n"
        text += "\t\t\t}\n"
        text += "\n"
        
        # Create Connection
        text += "\t\t\tvar connection = _context.Database.GetDbConnection();\n"
        text += "\t\t\tawait connection.OpenAsync();\n"
        text += "\n"

        text += "\t\t\tvar command = connection.CreateCommand();\n"

        # Create Command
        text += "\t\t\tcommand.CommandText = $\"EXEC "+model_name
        if (headers != None):
            for index, header in enumerate(headers):
                text += " @"+header["name"]+" = {"+header["name"]+"}"
                if index < len(headers)-1:
                    text += ","
        text += ";\";\n"

        text += "\t\t\tcommand.CommandType = CommandType.Text;\n"
        text += "\n"
        text += "\t\t\tvar reader = await command.ExecuteReaderAsync();\n"

        # Loop for each sub model
        for sub_model in sub_models:
            var_name = sub_model["name"][0].lower() + sub_model["name"][1:]
            text += "\t\t\tvar "+var_name+" = new List<"+sub_model["name"]+">();\n"
        text += "\n"

        # Loop for each sub model
        
        for index, sub_model in enumerate(sub_models):
            var_name = sub_model["name"][0].lower() + sub_model["name"][1:]
            text += "\t\t\twhile (await reader.ReadAsync())\n"
            text += "\t\t\t{\n"
            text += "\t\t\t\t"+var_name+".Add(new "+sub_model["name"]+"(\n"
            for column in sub_model["columns"]:
                text += "\t\t\t\t\treader.GetString(\""+column["name"]+"\"),\n" # TODO TYPE GetInt32
            text += "\t\t\t\t));\n"
            text += "\t\t\t}\n"
            text += "\n"

            if (index < len(sub_models)-1):
                text += "\t\t\tawait reader.NextResultAsync();\n"
            else:
                text += "\t\t\tawait reader.CloseAsync();\n"
            text += "\n"

        # Create result with sub model loop
        text += "\t\t\tvar query = new GetProductionScreen("
        for index, sub_model in enumerate(sub_models):
            var_name = sub_model["name"][0].lower() + sub_model["name"][1:]
            text += var_name
            if (index < len(sub_models)-1):
                text += ", "
                
        text += ");\n"
        text += "\t\t\treturn query;\n"
        text += "\t\t}\n"

    else:

        # Get Stored Procedure Type (SELECT, INSERT, UPDATE, DELETE) # TODO DELETE
        method_code = ""
        if ("get" in model_name.lower()):
            method_code = get_get_stored_procedure_method(model_name, headers)
        elif ("add" in model_name.lower()):
            method_code = get_post_stored_procedure_method(model_name, columns)
        elif ("update" in model_name.lower()):
            method_code = get_put_stored_procedure_method(model_name, columns)

        text += method_code

    # End
    text += "\t}\n"
    text += "}\n"
    return text


### Dot Net FrameWork 6.0.6 Context generated from all tables in a database script ###
## Parameters
# 1. @api_name = API name
# 2. @db_name = DataBase name
# 3. @tables =  All tables in the Database Script
# 4. @stored_procedures = All Columns in the Database Script
def get_context(api_name, db_name, tables, stored_procedures):

    # Declare Variables
    text = ""

    # Write Imports
    text += "using " + api_name + ".Models;\n"
    text += "using " + api_name + ".Models.StoredProcedures;\n"
    text += "using Microsoft.EntityFrameworkCore;\n"
    text += "\n"
    
    # Write Namespace, Class Start and Constructor
    text += "namespace " + api_name + ".Data\n"
    text += "{\n"
    text += "\tpublic class "+db_name+"DbContext : DbContext\n"
    text += "\t{\n"
    text += "\t\tpublic "+db_name+"DbContext(DbContextOptions<"+db_name+"DbContext> options)\n"
    text += "\t\t: base(options)\n"
    text += "\t\t{\n"
    text += "\t\t}\n"
    text += "\n"

    # Write for all tables in sql script
    for table in tables:
        text += "\t\tpublic DbSet<"+table["name"]+"> "+table["name"]+" { get; set; } = null!;\n"
    
    # Write for all Stored Procedures in sql script
    if (len(stored_procedures) > 0):
        text += "\n\t\t// ---------------------------- Stored Procedures ---------------------------- \n\n"
        for sp in stored_procedures:
            text += "\t\tpublic DbSet<"+sp["name"]+"> "+sp["name"]+" { get; set; } = null!;\n"

    # Close code
    text += "\n"
    text += "\t\t}\n"
    text += "}"

    return text
    


####################################################
## 2. Generate Method Code Functions
####################################################         



### Dot Net FrameWork 6.0.6 Get All Method generated for default controller ###
## Parameters
# 1. @model_name = Model name
def get_get_all_method(model_name):
    text = ""
    text += "\t\t// GET: api/" + model_name + "\n"
    text += "\t\t[HttpGet]\n"
    text += "\t\tpublic async Task<ActionResult<IEnumerable<" + model_name + ">>> Get()\n"
    text += "\t\t{\n"
    text += "\t\t\tif (_context." + model_name + " == null)\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\treturn NotFound();\n"
    text += "\t\t\t}\n"
    text += "\t\t\treturn await _context." + model_name + ".ToListAsync();\n"
    text += "\t\t}\n"
    text += "\n"
    return text


### Dot Net FrameWork 6.0.6 Get By Id Method generated for default controller ###
## Parameters
# 1. @model_name = Model name
def get_get_by_id_method(model_name):
    text = ""
    text += "\t\t// GET: api/" + model_name + "/5\n"
    text += "\t\t[HttpGet(\"{id}\")]\n"
    text += "\t\tpublic async Task<ActionResult<" + model_name + ">> Get(int id)\n"
    text += "\t\t{\n"
    text += "\t\t\tif (_context." + model_name + " == null)\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\treturn NotFound();\n"
    text += "\t\t\t}\n"
    text += "\t\t\tvar _" + model_name.lower() + " = await _context." + model_name + ".FindAsync(id);\n"
    text += "\n"
    text += "\t\t\tif (_" + model_name.lower() + " == null)\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\treturn NotFound();\n"
    text += "\t\t\t}\n"
    text += "\n"
    text += "\t\t\treturn _" + model_name.lower() + ";\n"
    text += "\t\t}\n"
    text += "\n"
    return text


### Dot Net FrameWork 6.0.6 Post Method generated for default controller ###
## Parameters
# 1. @model_name = Model name
# 2. @db_name = DataBase name
# 3. @first_column_name = The id / primary key of the model
def get_post_method(model_name, db_name, first_column_name):
    text = ""
    text += "\t\t// POST: api/" + model_name + "\n"
    text += "\t\t// To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754\n"
    text += "\t\t[HttpPost]\n"
    text += "\t\tpublic async Task<ActionResult<" + model_name + ">> Post(" + model_name + " _" + model_name.lower() + ")\n"
    text += "\t\t{\n"
    text += "\t\t\tif (_context." + model_name + " == null)\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\treturn Problem(\"Entity set '" + db_name + "DbContext." + model_name + "'\tis null.\");\n"
    text += "\t\t\t}\n"
    text += "\t\t\t_context." + model_name + ".Add(_" + model_name.lower() + ");\n"
    text += "\t\t\tawait _context.SaveChangesAsync();\n"
    text += "\n"

    text += "\t\t\treturn CreatedAtAction(\"Get\", new { id = _" + model_name.lower() + "."+first_column_name+" }, _" + model_name.lower() + ");\n" 
    text += "\t\t}\n"
    text += "\n"
    return text


### Dot Net FrameWork 6.0.6 Put Method generated for default controller ###
## Parameters
# 1. @model_name = Model name
def get_put_method(model_name):
    text = ""
    text += "\t\t// PUT: api/" + model_name + "/5\n"
    text += "\t\t// To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754\n"
    text += "\t\t[HttpPut(\"{id}\")]\n"
    text += "\t\tpublic async Task<IActionResult> Put(int id, " + model_name + " _" + model_name.lower() + ")\n"
    text += "\t\t{\n"
    text += "\t\t\t_context.Entry(_" + model_name.lower() + ").State = EntityState.Modified;\n"
    text += "\n"
    text += "\t\t\ttry\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\tawait _context.SaveChangesAsync();\n"
    text += "\t\t\t}\n"
    text += "\t\t\tcatch (DbUpdateConcurrencyException)\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\tif (!" + model_name + "Exists(id))\n"
    text += "\t\t\t\t{\n"
    text += "\t\t\t\t\treturn NotFound();\n"
    text += "\t\t\t\t}\n"
    text += "\t\t\t\telse\n"
    text += "\t\t\t\t{\n"
    text += "\t\t\t\t\tthrow;\n"
    text += "\t\t\t\t}\n"
    text += "\t\t\t}\n"
    text += "\n"
    text += "\t\t\treturn NoContent();\n"
    text += "\t\t}\n"
    text += "\n"
    return text


### Dot Net FrameWork 6.0.6 Delete Method generated for default controller ###
## Parameters
# 1. @model_name = Model name
def get_delete_method(model_name):
    text = ""
    text += "\t\t// DELETE: api/" + model_name + "/5\n"
    text += "\t\t[HttpDelete(\"{id}\")]\n"
    text += "\t\tpublic async Task<IActionResult> Delete(int id)\n"
    text += "\t\t{\n"
    text += "\t\t\tif (_context." + model_name + " == null)\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\treturn NotFound();\n"
    text += "\t\t\t}\n"
    text += "\t\t\tvar _" + model_name.lower() + " = await _context." + model_name + ".FindAsync(id);\n"
    text += "\t\t\tif (_" + model_name.lower() + " == null)\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\treturn NotFound();\n"
    text += "\t\t\t}\n"
    text += "\n"
    return text


### Dot Net FrameWork 6.0.6 Get Store Procedure Method generated for default controller ###
## Parameters
# 1. @model_name = Model name
def get_get_stored_procedure_method(model_name, headers):
    text = ""
    text += "\t\t// GET: api/" + model_name + "\n"
    text += "\t\t[HttpGet]\n"
    text += "\t\tpublic async Task<ActionResult<IEnumerable<" + model_name + ">>> Get("

    # Set all parameters
    if (headers != None):
        for index, header in enumerate(headers):
            type_converted = get_var_type(header["type"])
            text += type_converted +" "+header["name"]
            if (index < len(headers)-1):
                text += ", "

    text += ")\n"
    text += "\t\t{\n"
    text += "\t\t\tif (_context." + model_name + " == null)\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\treturn NotFound();\n"
    text += "\t\t\t}\n"
    text += "\t\t\tvar query = await _context." + model_name + ".FromSqlInterpolated($\"EXEC "+model_name

    #example: text += "\t\t\tFormattableString cmd = $\"EXEC "+model_name+" @UserId = {"+var_name+".user_id}, @StopTypeId = {"+var_name+".stop_type_id}\";\n"
    if (headers != None):
        for index, header in enumerate(headers):
            text += " @"+header["name"]+" = {"+header["name"]+"}"
            if index < len(headers)-1:
                text += ","

    text += ";\").ToListAsync();\n"

    text += "\t\t\treturn query;\n"
    text += "\t\t}\n"
    text += "\n"
    return text


### Dot Net FrameWork 6.0.6 Post Store Procedure Method generated for default controller ###
## Parameters
# 1. @model_name = Model name
def get_post_stored_procedure_method(model_name, columns):
    text = ""
    var_name = "_"+model_name.lower()
    text += "\t\t[HttpPost]\n"
    text += "\t\tpublic async Task<ActionResult<Stop>> Post("+model_name+" "+var_name+")\n"
    text += "\t\t{\n"
    text += "\t\t\tFormattableString cmd = $\"EXEC "+model_name

    #example: text += "\t\t\tFormattableString cmd = $\"EXEC "+model_name+" @UserId = {"+var_name+".user_id}, @StopTypeId = {"+var_name+".stop_type_id}\";\n"
    for index, column in enumerate(columns):
        text += " @"+column["name"]+" = {"+var_name+"."+column["name"]+"}"
        if index < len(columns)-1:
            text += ","
    text += "\";\n"

    text += "\t\t\t_context.Database.ExecuteSqlInterpolated(cmd);\n"
    text += "\n"
    text += "\t\t\treturn NoContent();\n"
    text += "\t\t}\n"
    return text


### Dot Net FrameWork 6.0.6 Put Store Procedure Method generated for default controller ###
## Parameters
# 1. @model_name = Model name
def get_put_stored_procedure_method(model_name, columns):
    text = ""
    var_name = "_"+model_name.lower()
    text += "\t\t[HttpPut]\n"
    text += "\t\tpublic async Task<ActionResult<Stop>> Put("+model_name+" "+var_name+")\n"
    text += "\t\t{\n"
    text += "\t\t\tFormattableString cmd = $\"EXEC "+model_name

    #example: text += "\t\t\tFormattableString cmd = $\"EXEC "+model_name+" @UserId = {"+var_name+".user_id}, @StopTypeId = {"+var_name+".stop_type_id}\";\n"
    for index, column in enumerate(columns):
        text += " @"+column["name"]+" = {"+var_name+"."+column["name"]+"}"
        if index < len(columns)-1:
            text += ","
    text += "\";\n"

    text += "\t\t\t_context.Database.ExecuteSqlInterpolated(cmd);\n"
    text += "\n"
    text += "\t\t\treturn NoContent();\n"
    text += "\t\t}\n"
    return text


####################################################
## 3. Generate Other Files
####################################################         



### Dot Net FrameWork 6.0.6 Launch Settings code generated based on the api name ###
## Parameters
# 1. @api_name = API name
def get_launch_settings(api_name):
    text = ""
    text += "{\n"
    text += "\t\"$schema\": \"https://json.schemastore.org/launchsettings.json\",\n"
    text += "\t\"iisSettings\": {\n"
    text += "\t\"windowsAuthentication\": false,\n"
    text += "\t\"anonymousAuthentication\": true,\n"
    text += "\t\"iisExpress\": {\n"
    text += "\t\t\"applicationUrl\": \"http://0.0.0.0:42263\",\n"
    text += "\t\t\"sslPort\": 44311\n"
    text += "\t}\n"
    text += "\t},\n"
    text += "\t\"profiles\": {\n"
    text += "\t\""+api_name+"\": {\n"
    text += "\t\t\"commandName\": \"Project\",\n"
    text += "\t\t\"dotnetRunMessages\": true,\n"
    text += "\t\t\"launchBrowser\": true,\n"
    text += "\t\t\"launchUrl\": \"swagger\",\n"
    text += "\t\t\"applicationUrl\": \"https://0.0.0.0:7005;http://0.0.0.0:5052\",\n"
    text += "\t\t\"environmentVariables\": {\n"
    text += "\t\t\"ASPNETCORE_ENVIRONMENT\": \"Development\"\n"
    text += "\t\t}\n"
    text += "\t},\n"
    text += "\t\"IIS Express\": {\n"
    text += "\t\t\"commandName\": \"IISExpress\",\n"
    text += "\t\t\"launchBrowser\": true,\n"
    text += "\t\t\"launchUrl\": \"swagger\",\n"
    text += "\t\t\"environmentVariables\": {\n"
    text += "\t\t\"ASPNETCORE_ENVIRONMENT\": \"Development\"\n"
    text += "\t\t}\n"
    text += "\t}\n"
    text += "\t}\n"
    text += "}\n"
    return text


### Dot Net FrameWork 6.0.6 App Settings code generated based on the database name ###
## Parameters
# 1. @db_name = DataBase name
def get_app_settings(db_name, connection_string):
    text = ""
    text += "{\n"
    text += "\t\"Logging\": {\n"
    text += "\t\"LogLevel\": {\n"
    text += "\t\t\"Default\": \"Information\",\n"
    text += "\t\t\"Microsoft.AspNetCore\": \"Warning\"\n"
    text += "\t}\n"
    text += "\t},\n"
    text += "\t\"AllowedHosts\": \"*\",\n"
    text += "\t\"ConnectionStrings\": {\n"
    text += "\t\"" + db_name + "\": \""+connection_string+"\"\n" # TODO INSERT DB CREDENTIALS
    text += "\t},\n"
    text += "\t\"ReApiKey\": \"pgH7QzFHJx4w46fI~5Uzi4RvtTwlEXp\"\n"
    text += "\t\n"
    text += "}\n"
    return text


### Dot Net FrameWork 6.0.6 App Settings Development default code generated ###
def get_app_settings_dev():
    text = ""
    text += "{\n"
    text += "\t\"Logging\": {\n"
    text += "\t\"LogLevel\": {\n"
    text += "\t\t\"Default\": \"Information\",\n"
    text += "\t\t\"Microsoft.AspNetCore\": \"Warning\"\n"
    text += "\t}\n"
    text += "\t}\n"
    text += "}\n"
    return text


### Dot Net FrameWork 6.0.6 Program code generated based on the api name and database name ###
## Parameters
# 1. @api_name = API name
# 2. @db_name = DataBase name
def get_program(api_name, db_name):
    text = ""
    text += "using Microsoft.EntityFrameworkCore;\n"
    text += "using "+api_name+".Data;\n"
    text += "\n"
    text += "var builder = WebApplication.CreateBuilder(args);\n"
    text += "\n"
    text += "// Add services to the container.\n"
    text += "\n"
    text += "builder.Services.AddControllers().AddNewtonsoftJson();\n"
    text += "// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle\n"
    text += "builder.Services.AddEndpointsApiExplorer();\n"
    text += "builder.Services.AddSwaggerGen();\n"
    text += "\n"
    text += "builder.Services.AddDbContext<"+db_name+"DbContext>(options =>\n"
    text += " options.UseSqlServer(builder.Configuration.GetConnectionString(\""+db_name+"\")));\n"
    text += "\n"
    text += "var app = builder.Build();\n"
    text += "\n"
    text += "\n"
    text += "// Configure the HTTP request pipeline.\n"
    text += "if (app.Environment.IsDevelopment())\n"
    text += "{\n"
    text += "\tapp.UseSwagger();\n"
    text += "\tapp.UseSwaggerUI();\n"
    text += "}\n"
    text += "\n"
    text += "//app.UseHttpsRedirection();\n"
    text += "\n"
    text += "//app.UseAuthorization();\n"
    text += "\n"
    text += "app.UseMiddleware<ApiKeyMiddleware>();\n"
    text += "\n"
    text += "app.MapControllers();\n"
    text += "\n"
    text += "app.Run();\n"
    return text


### Dot Net FrameWork 6.0.6 Project File default code generated ###
def get_project_file():
    text = ""
    text += "<Project Sdk=\"Microsoft.NET.Sdk.Web\">\n"
    text += "\n"
    text += "\t<PropertyGroup>\n"
    text += "\t<TargetFramework>net6.0</TargetFramework>\n"
    text += "\t<Nullable>enable</Nullable>\n"
    text += "\t<ImplicitUsings>enable</ImplicitUsings>\n"
    text += "\t</PropertyGroup>\n"
    text += "\n"
    text += "\t<ItemGroup>\n"
    text += "\t<PackageReference Include=\"DotNetEnv\" Version=\"2.3.0\" />\n"
    text += "\t<PackageReference Include=\"Microsoft.AspNetCore.Mvc.NewtonsoftJson\" Version=\"6.0.6\" />\n"
    text += "\t<PackageReference Include=\"Microsoft.AspNetCore.Mvc.Versioning\" Version=\"5.0.0\" />\n"
    text += "\t<PackageReference Include=\"Microsoft.EntityFrameworkCore\" Version=\"6.0.6\" />\n"
    text += "\t<PackageReference Include=\"Microsoft.EntityFrameworkCore.Design\" Version=\"6.0.6\">\n"
    text += "\t\t<IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>\n"
    text += "\t\t<PrivateAssets>all</PrivateAssets>\n"
    text += "\t</PackageReference>\n"
    text += "\t<PackageReference Include=\"Microsoft.EntityFrameworkCore.InMemory\" Version=\"6.0.6\" />\n"
    text += "\t<PackageReference Include=\"Microsoft.EntityFrameworkCore.SqlServer\" Version=\"6.0.6\" />\n"
    text += "\t<PackageReference Include=\"Microsoft.EntityFrameworkCore.Tools\" Version=\"6.0.6\">\n"
    text += "\t\t<IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>\n"
    text += "\t\t<PrivateAssets>all</PrivateAssets>\n"
    text += "\t</PackageReference>\n"
    text += "\t<PackageReference Include=\"Microsoft.VisualStudio.Web.CodeGeneration.Design\" Version=\"6.0.6\" />\n"
    text += "\t<PackageReference Include=\"Swashbuckle.AspNetCore\" Version=\"6.2.3\" />\n"
    text += "\t</ItemGroup>\n"
    text += "\n"
    text += "</Project>\n"
    return text


### Dot Net FrameWork 6.0.6 Middleware File default code generated ###
def get_middleware():
    text = ""
    text += "public class ApiKeyMiddleware {\n"
    text += "\tprivate readonly RequestDelegate _next;\n"
    text += "\tprivate\n"
    text += "\tconst string APIKEY = \"ReApiKey\";\n"
    text += "\tpublic ApiKeyMiddleware(RequestDelegate next) {\n"
    text += "\t\t_next = next;\n"
    text += "\t}\n"
    text += "\tpublic async Task InvokeAsync(HttpContext context) {\n"
    text += "\t\tif (!context.Request.Headers.TryGetValue(APIKEY, out\n"
    text += "\t\t\t\tvar extractedApiKey)) {\n"
    text += "\t\t\tcontext.Response.StatusCode = 401;\n"
    text += "\t\t\tawait context.Response.WriteAsync(\"Api Key was not provided \");\n"
    text += "\t\t\treturn;\n"
    text += "\t\t}\n"
    text += "\n"
    text += "\t\t// Get API key value\n"
    text += "\t\tvar appSettings = context.RequestServices.GetRequiredService < IConfiguration > ();\n"
    text += "\t\tvar apiKey = appSettings.GetValue < string > (APIKEY);\n"
    text += "\n"
    text += "\t\tif (!apiKey.Equals(extractedApiKey)) {\n"
    text += "\t\t\tcontext.Response.StatusCode = 401;\n"
    text += "\t\t\tawait context.Response.WriteAsync(\"Unauthorized client\");\n"
    text += "\t\t\treturn;\n"
    text += "\t\t}\n"
    text += "\t\t\n"
    text += "\t\tawait _next(context);\n"
    text += "\t}\n"
    text += "}\n"
    return text


### Dot Net FrameWork 6.0.6 Readme File default code generated ###
def get_readme():
    text = ""
    text += "# Packages\n\n"
    text += "1. dotnet add package Microsoft.EntityFrameworkCore --version 6.0.7\n"
    text += "2. dotnet add package Microsoft.EntityFrameworkCore.Design\n"
    text += "3. dotnet add package Microsoft.EntityFrameworkCore.SqlServer\n"
    return text



####################################################
## 4. Utils
####################################################         


### Convert a varible name to a more smaller version ###
## TODO Everything
def get_name_without_first():
    ''' # TODO name_without_first
    names = column["name"].split("_")
    name_without_first = ""
    for index, name in enumerate(names):
        if index != 0:
            name_without_first += name
            if (index < len(names)-1):
                name_without_first += "_"

    if ("id" in name_without_first or name_without_first == ""):
        name_without_first = column["name"]

    # Check starting with number
    if (name_without_first[0].isnumeric()):
        name_without_first = column["name"]
    '''
    pass


### Convert from a selected Db Type a Variable Type to Csharp Variable Type ###
## Parameters
# 1. @db_name = DataBase name
def get_var_type(db_type):

    # Open dictionary
    dictionary = get_sql_server_to_cs_dictionary()
    result = db_type

    # Find the correct keyword in the dictionary
    try:
        result = dictionary[db_type.upper()]
    except:
        if (result == db_type and "VARCHAR" in db_type):
            result = "string?"

    return result


### Dictionary that covert variable types in sql server to csharp ###
def get_sql_server_to_cs_dictionary():
    return {
        "VARCHAR":"string?",
        "DECIMAL":"decimal",
        "INT":"int",
        "BIT":"bool",
        "DATETIME":"DateTime",
        "DATE":"DateTime",
        "TIME":"TimeSpan"
        }
