
def get_db_json(db_data):

    # Result data
    tables = []

    # Get all lines in the database script
    lines = db_data.splitlines()

    # Read database script
    current_table = None
    current_table_index = 0
    for line in lines:

        # Search for a table
        if (current_table == None):
            if ("CREATE TABLE" in line and "FILETABLE" not in line):
                current_table = get_table_name(line)
                tables.append({"name":current_table, "columns":[]})
                current_table_index = len(tables)-1

        # Add column to the current table
        else:
            # Close table
            if ("PRIMARY KEY" in line):
                current_table = None
            else:

                # Find [ and ] Character
                # First element is column name, second one is column type

                # Find ( and ) Character
                # inside is lenght of the column type

                col_name = get_column_name(line)
                col_type = get_column_type(line)
                type_lenght = get_type_lenght(line)

                column = {"name":col_name,"type":col_type,"length":type_lenght}
                tables[current_table_index]["columns"].append(column)


    return tables


def get_table_name(line):
    result = line.replace("CREATE TABLE", "")
    result = result.replace("dbo", "")
    result = result.replace("[", "")
    result = result.replace("]", "")
    result = result.replace("(", "")
    result = result.replace(".", "")
    result = result.replace(" ", "")
    result = result.replace("\t", "")
    result = result.replace("\n", "")
    return result


def get_column_name(line):

    start_pos = None
    end_pos = None
    for pos,char in enumerate(line):
        if(char == '[' and start_pos == None):
            start_pos = pos
        if(char == ']' and end_pos == None):
            end_pos = pos

    result = line[start_pos+1: end_pos]
    return result


def get_column_type(line):
    start_pos = None
    end_pos = None
    for pos,char in enumerate(line):
        if(char == '['):
            start_pos = pos
        if(char == ']'):
            end_pos = pos

    result = line[start_pos+1: end_pos]
    return result


def get_type_lenght(line):
    return None
