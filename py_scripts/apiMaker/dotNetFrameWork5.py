
def get_model(api_name, model_name, columns):
    text = ""

    text += "using System;\n"
    text += "using System.ComponentModel.DataAnnotations;\n"
    text += "using System.ComponentModel.DataAnnotations.Schema;\n"
    text += "\n"
    text += "namespace " + api_name + ".Models\n"
    text += "{\n"
    text += "\tpublic class " + model_name + "\n"
    text += "\t{\n"
    text += "\t\t[Key]\n"

    for column in columns:

        var_type = get_var_type(column["type"])

        if (column["length"] != None and var_type == "string"):
            text += "\t\t[StringLength("+str(column["length"])+", ErrorMessage = \"Max Characters Limit Reached\")]\n"

        text += "\t\tpublic "+var_type+" "+column["name"]+" { get; set; }\n"

    text += "\t}\n"
    text += "}"

    return text


def get_controller(api_name, db_name, model_name, columns):
    text = ""

    text += "using " + api_name + ".Context;\n"
    text += "using " + api_name + ".Models;\n"
    text += "using Microsoft.AspNetCore.Mvc;\n"
    text += "using Microsoft.EntityFrameworkCore;\n"
    text += "using System;\n"
    text += "using System.Collections.Generic;\n"
    text += "using System.Linq;\n"
    text += "using System.Threading.Tasks;\n"
    text += "\n"
    text += "namespace " + api_name + ".Controllers\n"
    text += "{\n"
    text += "\t[Route(\"api/\")]\n"
    text += "\t[ApiController]\n"
    text += "\tpublic class " + model_name + "Controller : Controller\n"
    text += "\t{\n"
    text += "\n"
    text += "\t\t//GET ALL\n"
    text += "\t\t[HttpGet]\n"
    text += "\t\t[Route(\"[controller]\")]\n"
    text += "\t\tpublic async Task<ActionResult<List<" + model_name + ">>> Get([FromServices] " + db_name + "DbContext context)\n"
    text += "\t\t{\n"
    text += "\t\t\tvar all" + model_name + " = await context." + model_name + ".FromSqlRaw(\"SELECT * FROM " + model_name + ";\").ToListAsync();\n"
    text += "\t\t\treturn all" + model_name + ".ToList();\n"
    text += "\t\t}\n"
    text += "\n"
    text += "\n"
    text += "\t\t//GET BY ID\n"
    text += "\t\t[HttpGet]\n"
    text += "\t\t[Route(\"[controller]/{id:int}\")]\n"
    text += "\t\tpublic async Task<ActionResult<List<" + model_name + ">>> GetById([FromServices] " + db_name + "DbContext context, int id)\n"
    text += "\t\t{\n"
    text += "\t\t\tvar " + model_name + "Id = await context." + model_name + ".FromSqlRaw(\"SELECT * FROM " + model_name + " WHERE ID=\" + id).ToListAsync();\n"
    text += "\t\t\treturn " + model_name + "Id;\n"
    text += "\t\t}\n"
    text += "\n"
    text += "\n"
    text += "\t\t//POST\n"
    text += "\t\t[HttpPost]\n"
    text += "\t\t[Route(\"[controller]\")]\n"
    text += "\t\tpublic async Task<ActionResult<" + model_name + ">> Post([FromServices] " + db_name + "DbContext context, [FromBody] " + model_name + " model)\n"
    text += "\t\t{\n"
    text += "\t\t\tif (ModelState.IsValid)\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\tcontext." + model_name + ".Add(model);\n"
    text += "\t\t\t\tawait context.SaveChangesAsync();\n"
    text += "\t\t\t\treturn model;\n"
    text += "\t\t\t}\n"
    text += "\t\t\telse\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\treturn BadRequest(ModelState);\n"
    text += "\t\t\t}\n"
    text += "\t\t}\n"
    text += "\n"
    text += "\n"
    text += "\t\t//PUT\n"
    text += "\t\t[HttpPut(\"[controller]/{id}\")]\n"
    text += "\t\tpublic async Task<ActionResult<" + model_name + ">> Put([FromServices] " + db_name + "DbContext context, [FromBody] " + model_name + " model, int id)\n"
    text += "\t\t{\n"
    text += "\t\t\ttry\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\tif (ModelState.IsValid)\n"
    text += "\t\t\t\t{\n"
    text += "\t\t\t\t\tvar entity = context." + model_name + ".FirstOrDefault(e => e.id == id);\n"
    text += "\t\t\t\t\tif (entity == null)\n"
    text += "\t\t\t\t\t{\n"
    text += "\t\t\t\t\t\treturn BadRequest(ModelState);\n"
    text += "\t\t\t\t\t}\n"
    text += "\t\t\t\t\telse\n"
    text += "\t\t\t\t\t{\n"
    for column in columns:
        text += "\t\t\t\t\t\tentity."+column["name"]+" = model."+column["name"]+";\n"
    text += "\n"
    text += "\t\t\t\t\t\tawait context.SaveChangesAsync();\n"
    text += "\t\t\t\t\t\treturn model;\n"
    text += "\t\t\t\t\t}\n"
    text += "\t\t\t\t}\n"
    text += "\t\t\t\telse\n"
    text += "\t\t\t\t{\n"
    text += "\t\t\t\t\treturn BadRequest(ModelState);\n"
    text += "\t\t\t\t}\n"
    text += "\t\t\t}\n"
    text += "\t\t\tcatch (Exception ex)\n"
    text += "\t\t\t{\n"
    text += "\t\t\t\treturn BadRequest(ModelState);\n"
    text += "\t\t\t}\n"
    text += "\t\t}\n"
    text += "\n"
    text += "\n"
    text += "\t\t//DELETE\n"
    text += "\t\t[HttpDelete(\"[controller]/{id}\")]\n"
    text += "\t\tpublic void Delete(int id)\n"
    text += "\t\t{\n"
    text += "\t\t}\n"
    text += "\t}\n"
    text += "}"
    return text


def get_context(api_name, db_name, tables, stored_procedures):
    text = ""

    text += "using " + api_name + ".Models;\n"
    text += "using Microsoft.EntityFrameworkCore;\n"
    text += "\n"
    text += "namespace " + api_name + ".Context\n"
    text += "{\n"
    text += "\tpublic class "+db_name+"DbContext : DbContext\n"
    text += "\t{\n"
    text += "\t\tpublic "+db_name+"DbContext(DbContextOptions<"+db_name+"DbContext> options)\n"
    text += "\t\t: base(options)\n"
    text += "\t\t{\n"
    text += "\t\t}\n"
    text += "\n"

    for table in tables:
        text += "\t\tpublic DbSet<"+table["name"]+"> "+table["name"]+" { get; set; }\n"
    
    if (len(stored_procedures) > 0):
        text += "\n\t\t// ---------------------------- Stored Procedures ---------------------------- \n\n"
        for sp in stored_procedures:
            text += "\t\tpublic DbSet<"+sp["name"]+"> "+sp["name"]+" { get; set; }\n"

    text += "\n"
    text += "\t\t}\n"
    text += "}"
    return text
    

def get_var_type(db_type):

    # Open dictionary
    dictionary = get_sql_server_to_cs_dictionary()
    result = db_type

    # Find the correct keyword in the dictionary
    try:
        result = dictionary[db_type.upper()]
    except:
        if (result == db_type and "VARCHAR" in db_type):
            result = "string"

    return result


# Dictionary that covert variable types in sql server to csharp
def get_sql_server_to_cs_dictionary():
    return {
        "VARCHAR":"string",
        "DECIMAL":"decimal",
        "INT":"int",
        "BIT":"bool",
        "DATETIME":"DateTime",
        "DATE":"DateTime",
        "TIME":"TimeSpan"
        }