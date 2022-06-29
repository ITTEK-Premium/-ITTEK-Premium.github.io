import json, os

def get_model(name, columns):
    text = ""

    text += "using System;\n"
    text += "using System.ComponentModel.DataAnnotations;\n"
    text += "using System.ComponentModel.DataAnnotations.Schema;\n"
    text += "\n"
    text += "namespace ITTEKPremium_API.Models\n"
    text += "{\n"
    text += "\t\tpublic class " + name + "\n"
    text += "\t\t{\n"
    text += "\t\t\t\t[Key]\n"

    for column in columns:

        var_type = get_var_type(column["type"])

        if (column["length"] != None and var_type == "string"):
            text += "\t\t\t\t[StringLength("+str(column["length"])+", ErrorMessage = \"Max Characters Limit Reached\")]\n"

        text += "\t\t\t\tpublic "+var_type+" "+column["name"]+" { get; set; }\n"

    text += "\t\t}\n"
    text += "}"

    return text


def get_controller(name, columns):
    text = ""

    text += "using ITTEKPremium_API.Context;\n"
    text += "using ITTEKPremium_API.Models;\n"
    text += "using Microsoft.AspNetCore.Mvc;\n"
    text += "using Microsoft.EntityFrameworkCore;\n"
    text += "using System;\n"
    text += "using System.Collections.Generic;\n"
    text += "using System.Linq;\n"
    text += "using System.Threading.Tasks;\n"
    text += "\n"
    text += "namespace ITTEKPremium_API.Controllers\n"
    text += "{\n"
    text += "\t\t[Route(\"api/\")]\n"
    text += "\t\t[ApiController]\n"
    text += "\t\tpublic class " + name + "Controller : Controller\n"
    text += "\t\t{\n"
    text += "\n"
    text += "\t\t\t\t//GET ALL\n"
    text += "\t\t\t\t[HttpGet]\n"
    text += "\t\t\t\t[Route(\"[controller]\")]\n"
    text += "\t\t\t\tpublic async Task<ActionResult<List<" + name + ">>> Get([FromServices] ITTEKTesteDbContext context)\n"
    text += "\t\t\t\t{\n"
    text += "\t\t\t\t\t\tvar all" + name + " = await context." + name + ".FromSqlRaw(\"SELECT * FROM " + name + ";\").ToListAsync();\n"
    text += "\t\t\t\t\t\treturn all" + name + ".ToList();\n"
    text += "\t\t\t\t}\n"
    text += "\n"
    text += "\n"
    text += "\t\t\t\t//GET BY ID\n"
    text += "\t\t\t\t[HttpGet]\n"
    text += "\t\t\t\t[Route(\"[controller]/{id:int}\")]\n"
    text += "\t\t\t\tpublic async Task<ActionResult<List<" + name + ">>> GetById([FromServices] ITTEKTesteDbContext context, int id)\n"
    text += "\t\t\t\t{\n"
    text += "\t\t\t\t\t\tvar " + name + "Id = await context." + name + ".FromSqlRaw(\"SELECT * FROM " + name + " WHERE ID=\" + id).ToListAsync();\n"
    text += "\t\t\t\t\t\treturn " + name + "Id;\n"
    text += "\t\t\t\t}\n"
    text += "\n"
    text += "\n"
    text += "\t\t\t\t//POST\n"
    text += "\t\t\t\t[HttpPost]\n"
    text += "\t\t\t\t[Route(\"[controller]\")]\n"
    text += "\t\t\t\tpublic async Task<ActionResult<" + name + ">> Post([FromServices] ITTEKTesteDbContext context, [FromBody] " + name + " model)\n"
    text += "\t\t\t\t{\n"
    text += "\t\t\t\t\t\tif (ModelState.IsValid)\n"
    text += "\t\t\t\t\t\t{\n"
    text += "\t\t\t\t\t\t\t\tcontext." + name + ".Add(model);\n"
    text += "\t\t\t\t\t\t\t\tawait context.SaveChangesAsync();\n"
    text += "\t\t\t\t\t\t\t\treturn model;\n"
    text += "\t\t\t\t\t\t}\n"
    text += "\t\t\t\t\t\telse\n"
    text += "\t\t\t\t\t\t{\n"
    text += "\t\t\t\t\t\t\t\treturn BadRequest(ModelState);\n"
    text += "\t\t\t\t\t\t}\n"
    text += "\t\t\t\t}\n"
    text += "\n"
    text += "\n"
    text += "\t\t\t\t//PUT\n"
    text += "\t\t\t\t[HttpPut(\"[controller]/{id}\")]\n"
    text += "\t\t\t\tpublic async Task<ActionResult<" + name + ">> Put([FromServices] ITTEKTesteDbContext context, [FromBody] " + name + " model, int id)\n"
    text += "\t\t\t\t{\n"
    text += "\t\t\t\t\t\ttry\n"
    text += "\t\t\t\t\t\t{\n"
    text += "\t\t\t\t\t\t\t\tif (ModelState.IsValid)\n"
    text += "\t\t\t\t\t\t\t\t{\n"
    text += "\t\t\t\t\t\t\t\t\t\tvar entity = context." + name + ".FirstOrDefault(e => e.id == id);\n"
    text += "\t\t\t\t\t\t\t\t\t\tif (entity == null)\n"
    text += "\t\t\t\t\t\t\t\t\t\t{\n"
    text += "\t\t\t\t\t\t\t\t\t\t\t\treturn BadRequest(ModelState);\n"
    text += "\t\t\t\t\t\t\t\t\t\t}\n"
    text += "\t\t\t\t\t\t\t\t\t\telse\n"
    text += "\t\t\t\t\t\t\t\t\t\t{\n"
    for column in columns:
        text += "\t\t\t\t\t\t\t\t\t\t\t\tentity."+column["name"]+" = model."+column["name"]+";\n"
    text += "\n"
    text += "\t\t\t\t\t\t\t\t\t\t\t\tawait context.SaveChangesAsync();\n"
    text += "\t\t\t\t\t\t\t\t\t\t\t\treturn model;\n"
    text += "\t\t\t\t\t\t\t\t\t\t}\n"
    text += "\t\t\t\t\t\t\t\t}\n"
    text += "\t\t\t\t\t\t\t\telse\n"
    text += "\t\t\t\t\t\t\t\t{\n"
    text += "\t\t\t\t\t\t\t\t\t\treturn BadRequest(ModelState);\n"
    text += "\t\t\t\t\t\t\t\t}\n"
    text += "\t\t\t\t\t\t}\n"
    text += "\t\t\t\t\t\tcatch (Exception ex)\n"
    text += "\t\t\t\t\t\t{\n"
    text += "\t\t\t\t\t\t\t\treturn BadRequest(ModelState);\n"
    text += "\t\t\t\t\t\t}\n"
    text += "\t\t\t\t}\n"
    text += "\n"
    text += "\n"
    text += "\t\t\t\t//DELETE\n"
    text += "\t\t\t\t[HttpDelete(\"[controller]/{id}\")]\n"
    text += "\t\t\t\tpublic void Delete(int id)\n"
    text += "\t\t\t\t{\n"
    text += "\t\t\t\t}\n"
    text += "\t\t}\n"
    text += "}"
    return text


def get_context(name, columns):
    return "available soon"
    

def get_var_type(db_type):

    # Open dictionary
    dictionary = get_sql_server_to_cs_dictionary()
    result = db_type

    # Find the correct keyword in the dictionary
    try:
        result = dictionary[db_type]
    except:
        pass

    return result


# Dictionary that covert variable types in sql server to csharp
def get_sql_server_to_cs_dictionary():
    dictionary = {
        "varchar":"string",
        "decimal":"decimal",
        "int":"int",
        "bit":"bool",
        "datetime":"DateTime",
        "date":"DateTime",
        "time":"TimeSpan"
        }
    return dictionary