
def get_model(api_name, model_name, columns):
    text = ""
    isKeyless = False

    text += "using System.ComponentModel.DataAnnotations;\n"
    text += "using Newtonsoft.Json;\n"
    text += "\n"
    text += "namespace " + api_name + ".Models\n"
    text += "{\n"
    
    # Check need for Keyless, basically check if model has Get, Add or Update in name
    isKeyless = ("get" in model_name.lower() or "add" in model_name.lower() or "update" in model_name.lower())
    if (isKeyless):
        text += "\t\t[Keyless]\n"

    text += "\tpublic class " + model_name + "\n"
    text += "\t{\n"
    if (not isKeyless):
        text += "\t\t[Key]\n"

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

        text += "\t\t[JsonProperty(PropertyName = \"" + column["name"] + "\")]\n"
        text += "\t\tpublic "+var_type+" "+name_without_first+" { get; set; }\n"

    text += "\t}\n"
    text += "}"

    return text


def get_controller(api_name, db_name, model_name, columns):
    text = ""

    text += "using System;\n"
    text += "using System.Collections.Generic;\n"
    text += "using System.Linq;\n"
    text += "using System.Threading.Tasks;\n"
    text += "using Microsoft.AspNetCore.Http;\n"
    text += "using Microsoft.AspNetCore.Mvc;\n"
    text += "using Microsoft.EntityFrameworkCore;\n"
    text += "using " + api_name + ".Context;\n"
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

    # Get first element in columns
    first_column_name = columns[0]["name"]

    text += "\t\t\treturn CreatedAtAction(\"Get\", new { id = _" + model_name.lower() + "."+first_column_name+" }, _" + model_name.lower() + ");\n" 
    text += "\t\t}\n"
    text += "\n"
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
        text += "\t\tpublic DbSet<"+table["name"]+"> "+table["name"]+" { get; set; } = null!;\n"
    
    if (len(stored_procedures) > 0):
        text += "\n\t\t// ---------------------------- Stored Procedures ---------------------------- \n\n"
        for sp in stored_procedures:
            text += "\t\tpublic DbSet<"+sp["name"]+"> "+sp["name"]+" { get; set; } = null!;\n"

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
            result = "string?"

    return result


# Dictionary that covert variable types in sql server to csharp
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