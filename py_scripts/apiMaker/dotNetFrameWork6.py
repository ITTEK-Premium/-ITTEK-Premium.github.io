####################################################
## Py-Script Documentation -> https://github.com/pyscript/pyscript/blob/main/docs/tutorials/getting-started.md
## .NET FrameWork 6.0 Documentation -> https://docs.microsoft.com/en-us/dotnet/core/whats-new/dotnet-6

# Abstract: Library with all functions to build an API with .NET FrameWork 6.0.6
# Author: André Cerqueira
# Start Date: 01/07/2022
# Last Update Date: 12/07/2022
# Current Version: 1.1

####################################################


####################################################
## 1. Generate Script Code Functions
####################################################  


### Dot Net FrameWork 6.0.6 Model generated from a table from a database script ###
## Parameters
# 1. @api_name = API name
# 2. @model_name = Model name
# 3. @columns = All columns in the (api_name) table
def get_model(api_name, model_name, columns):

    # Declare Variables
    text = ""
    isKeyless = False

    # Write Imports
    text += "using System.ComponentModel.DataAnnotations;\n"
    text += "using Newtonsoft.Json;\n"
    text += "\n"
    text += "namespace " + api_name + ".Models\n"
    text += "{\n"
    
    # Write Class

    # Check need for Keyless, basically check if model has Get, Add or Update in name
    isKeyless = ("get" in model_name.lower() or "add" in model_name.lower() or "update" in model_name.lower())
    if (isKeyless):
        text += "\t[Keyless]\n"

    text += "\tpublic class " + model_name + "\n"
    text += "\t{\n"
    if (not isKeyless):
        text += "\t\t[Key]\n"

    # Write Every Variable and Variable Type
    for column in columns:

        var_type = get_var_type(column["type"])

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

        text += "\t\t[JsonProperty(PropertyName = \"" + name_without_first + "\")]\n"
        text += "\t\tpublic "+var_type+" "+column["name"]+" { get; set; }\n"

    # Close Code
    text += "\t}\n"
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
    text += "using System;\n"
    text += "using System.Collections.Generic;\n"
    text += "using System.Linq;\n"
    text += "using System.Threading.Tasks;\n"
    text += "using Microsoft.AspNetCore.Http;\n"
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
# 1. Read Properly
# 2. Analyse witch method use
# 3. Build Individual Controller
# 4. Build Multi Model Controller
def get_stored_procedure_controller(api_name, db_name, model_name, columns, stored_procedures):
    text = ""

    # Get Store Procedure name
    print("name --> " + model_name)

    text += "using System;\n"
    text += "using System.Collections.Generic;\n"
    text += "using System.Linq;\n"
    text += "using System.Threading.Tasks;\n"
    text += "using Microsoft.AspNetCore.Http;\n"
    text += "using Microsoft.AspNetCore.Mvc;\n"
    text += "using Microsoft.EntityFrameworkCore;\n"
    text += "using " + api_name + ".Data;\n"
    text += "using " + api_name + ".Models;\n"
    text += "\n"
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

    # Find for other stored procedures that can be here

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
def get_app_settings(db_name):
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
    text += "\t\"" + db_name + "\": \"[MISSING]\"\n" # TODO INSERT DB CREDENTIALS
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



####################################################
## 4. Utils
####################################################         


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
