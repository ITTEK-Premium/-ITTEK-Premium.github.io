####################################################
## SQL Server Documentation -> https://docs.microsoft.com/en-us/sql/sql-server/?view=sql-server-ver16

# Abstract: Library with all functions to read any type of Database creation script. Currently available only SQL Server.
# Author: André Cerqueira
# Start Date: 25/06/2022
# Last Update Date: 13/07/2022
# Current Version: 2.1

####################################################


####################################################
## 1. Get Database primary data
####################################################  


### Get all tables data in Database ###
## Parameters
# 1. @db_data = Database creation script code text
def get_tables(db_data):

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


### Get all stored procedures data in Database ###
## Parameters
# 1. @db_data = Database creation script code text
# 2. @tables = All tables in the database
def get_stored_procedures(db_data, tables):

    # Result data
    stored_procedures = []

    # Get all lines in the database script
    lines = db_data.splitlines()

    # Read database script
    current_line = ""
    for line in lines:

        # Search for stored procedures
        if ("CREATE PROCEDURE" in line):
            current_line = line
        elif ("GO" in line and current_line != ""):
            # Add Procedure
            name = get_stored_procedure_name(current_line)
            columns = get_stored_procedure_columns(tables, current_line)

            # Get headers from Select
            if ("SELECT" in current_line):
                headers = get_stored_procedure_headers(current_line)
                stored_procedures.append({"name":name, "columns":columns, "headers": headers})
            else:
                stored_procedures.append({"name":name, "columns":columns, "headers": None})

            current_line = ""
        elif ("AS" == line):
            current_line += "\nAS\n"
        elif (current_line != ""):
            current_line += line

    return stored_procedures


### Get all queries in a stored procedure ###
## Parameters
# 1. @db_data = Database creation script code text
# 2. @stored_procedure_name = Store Procedure name
def get_queries_in_stored_procedure(db_data, tables, stored_procedure_name):

    queries = []
    
    # Get all lines in the database script
    lines = db_data.splitlines()

    # Read database script
    current_line = ""
    select_count = 0
    found = False
    for line in lines:

        # Search for stored procedures
        if (not found and "CREATE PROCEDURE" in line and stored_procedure_name in line):
            found = True

        # End of the Store Procedure
        elif ("GO" in line and found):
            found = False

            for i in range(select_count):
                query = get_stored_procedure_columns_in_position(tables, current_line, i, stored_procedure_name)
                select_count += 1
                queries.append(query)
                # queries.append({"name":stored_procedure_name, "columns":columns})

            break
        
        elif ("AS" == line):
            current_line += "\nAS\n"
        elif (current_line != ""):
            current_line += line

        # Get all sub queries
        if (found):
            if ("SELECT" in line):
                select_count += 1

    return queries



####################################################
## 2. Get Database secondary data
####################################################  



### Get Database name ###
## Parameters
# 1. @db_data = Database creation script code text
def get_name(db_data):
    
    # Result data
    name = "Default"

    # Get all lines in the database script
    lines = db_data.splitlines()

    for line in lines:

        # Search for database name and select it
        if ("CREATE DATABASE" in line):
            result = line.replace("CREATE DATABASE", "")
            result = result.replace(" ", "")
            result = result.replace("[", "")
            result = result.replace("]", "")
            result = result.replace(" ", "")
            result = result.replace("\t", "")
            result = result.replace("\n", "")
            name = result
            break

    return name


### Get table name ###
## Parameters
# 1. @line = Database creation script current line text
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


### Get stored procedure name ###
## Parameters
# 1. @line = Database creation script current line text
def get_stored_procedure_name(line):
    start_pos = None
    end_pos = None
    for pos,char in enumerate(line):
        if(char == '['):
            start_pos = pos
        if(char == ']'):
            end_pos = pos

    result = line[start_pos+1: end_pos]
    return result


### Get stored procedure select headers used to call the function in the API ###
## Parameters
# 2. @line = Database creation script current line text
def get_stored_procedure_headers(line):
    try:
        headers = []

        line_splited = line.split("]")
        columns_in_line = line_splited[len(line_splited)-1]

        temp = columns_in_line.split("\nAS\n")

        headers_in_line = temp[0]
        raw_headers = headers_in_line.split(",")

        for raw_header in raw_headers:
            col_name = raw_header.split("@")[1].split(" ")[0]
            col_type = raw_header.split("@")[1].split(" ")[1]
            type_lenght = None
            headers.append({"name":col_name,"type":col_type,"length":type_lenght})

        return headers
    except:
        return None
    


### Get stored procedure columns ###
## Parameters
# 1. @tables = All tables in the database
# 2. @line = Database creation script current line text
def get_stored_procedure_columns(tables, line):
    columns = []

    # nao é só uma line é um conjunto de linhas ate AS

    # All Columns are after ] 
    # Each column and type are before ,

    line_splited = line.split("]")
    columns_in_line = line_splited[len(line_splited)-1]

    temp = columns_in_line.split("\nAS\n")

    columns_in_line = temp[0]
    stored_procedure_code = temp[1]

    columns_in_line = columns_in_line.replace("\n", "")
    columns_in_line = columns_in_line.replace("\t", "")
    stored_procedure_code = stored_procedure_code.replace("\n", "")
    stored_procedure_code = stored_procedure_code.replace("\t", "")

    raw_columns = columns_in_line.split(",")

    # SELECT get the columns in the SELECT line
    if ("SELECT" in stored_procedure_code):

        # ex: dv.id as drawing_version_id, c.id as client_id, d.drawing_number, dv.version, dv.color_quantity, sv.description as service_description, dv.width, dv.height, d.observation, d.image
        all_select_store_procedures = stored_procedure_code.split("SELECT")

        # Skip always the 1 element in the list because is the create procedure line
        for index, select_store_procedures in enumerate(all_select_store_procedures):

            if (index == 0):
                continue

            select_columns_in_line = select_store_procedures.split("FROM")[0]
            select_raw_columns = select_columns_in_line.split(",")

            for raw_column in select_raw_columns:

                delim = None
                if (" as " in raw_column):
                    delim = " as "
                elif (" AS " in raw_column):
                    delim = " AS "

                if (delim != None):
                    
                    # Get column original name in tables
                    col_original_name = raw_column.split(delim)[0] # check for . and split
                    if ("." in col_original_name):
                        col_original_name = col_original_name.split(".")[1]
                    col_original_name = col_original_name.replace(" ", "")

                    # Get column new name choosed by the developer
                    col_new_name = raw_column.split(delim)[1]
                    col_new_name = col_new_name.replace(" ", "")

                    # MISSING TYPE FOR NOW
                    col_type = get_type_in_stored_procedure(tables, col_original_name)
                    type_lenght = None

                    columns.append({"name":col_new_name,"type":col_type,"length":type_lenght})
                else:
                    # Get column name
                    col_name = raw_column
                    if ("." in col_name):
                        col_name = col_name.split(".")[1]
                    col_name = col_name.replace(" ", "")
                    
                    # MISSING TYPE FOR NOW
                    col_type = get_type_in_stored_procedure(tables, col_name)
                    type_lenght = None

                    columns.append({"name":col_name,"type":col_type,"length":type_lenght})

    # INSERT AND UPDATE get the columns in the procedure header
    else:
        for raw_column in raw_columns:
            col_name = raw_column.split("@")[1].split(" ")[0]
            col_type = raw_column.split("@")[1].split(" ")[1]
            type_lenght = None
            columns.append({"name":col_name,"type":col_type,"length":type_lenght})

    return columns


# TODO CREATE DOCUMENTATION
def get_stored_procedure_columns_in_position(tables, line, position, stored_procedure_name):
    columns = []
    names = []

    # nao é só uma line é um conjunto de linhas ate AS

    # All Columns are after ] 
    # Each column and type are before ,

    line_splited = line.split("]")
    columns_in_line = line_splited[len(line_splited)-1]

    temp = columns_in_line.split("\nAS\n")

    columns_in_line = temp[0]
    stored_procedure_code = temp[1]

    columns_in_line = columns_in_line.replace("\n", "")
    columns_in_line = columns_in_line.replace("\t", "")
    stored_procedure_code = stored_procedure_code.replace("\n", "")
    stored_procedure_code = stored_procedure_code.replace("\t", "")

    raw_columns = columns_in_line.split(",")

    # SELECT get the columns in the SELECT line
    if ("SELECT" in stored_procedure_code):

        # ex: dv.id as drawing_version_id, c.id as client_id, d.drawing_number, dv.version, dv.color_quantity, sv.description as service_description, dv.width, dv.height, d.observation, d.image
        
        # FIND ALL QUERY NAMES IN COMMENTS
        all_select_store_procedures_names = stored_procedure_code.split("--")
        for query_name in all_select_store_procedures_names:
            new_name = query_name.split("SELECT")[0]
            names.append(new_name)

        all_select_store_procedures = stored_procedure_code.split("SELECT")

        # Skip always the 1 element in the list because is the create procedure line
        for index, select_store_procedures in enumerate(all_select_store_procedures):

            if (index != position+1):
                continue

            select_columns_in_line = select_store_procedures.split("FROM")[0]
            select_raw_columns = select_columns_in_line.split(",")

            for raw_column in select_raw_columns:

                delim = None
                if (" as " in raw_column):
                    delim = " as "
                elif (" AS " in raw_column):
                    delim = " AS "

                if (delim != None):
                    
                    # Get column original name in tables
                    col_original_name = raw_column.split(delim)[0] # check for . and split
                    if ("." in col_original_name):
                        col_original_name = col_original_name.split(".")[1]
                    col_original_name = col_original_name.replace(" ", "")

                    # Get column new name choosed by the developer
                    col_new_name = raw_column.split(delim)[1]
                    col_new_name = col_new_name.replace(" ", "")

                    # MISSING TYPE FOR NOW
                    col_type = get_type_in_stored_procedure(tables, col_original_name)
                    type_lenght = None

                    columns.append({"name":col_new_name,"type":col_type,"length":type_lenght})
                else:
                    # Get column name
                    col_name = raw_column
                    if ("." in col_name):
                        col_name = col_name.split(".")[1]
                    col_name = col_name.replace(" ", "")
                    
                    # MISSING TYPE FOR NOW
                    col_type = get_type_in_stored_procedure(tables, col_name)
                    type_lenght = None

                    columns.append({"name":col_name,"type":col_type,"length":type_lenght})

    # INSERT AND UPDATE get the columns in the procedure header
    else:
        for raw_column in raw_columns:
            col_name = raw_column.split("@")[1].split(" ")[0]
            col_type = raw_column.split("@")[1].split(" ")[1]
            type_lenght = None
            columns.append({"name":col_name,"type":col_type,"length":type_lenght})

    try:
        new_name = names[position+1].replace(" ", "")
        return {"name":new_name, "columns":columns}
    except:
        return {"name":stored_procedure_name, "columns":columns}


### Get variable type for a variable in a stored procedure ###
## Parameters
# 1. @tables = All tables in the database
# 2. @column_name = Variable / Column name
def get_type_in_stored_procedure(tables, column_name):
    result = "MISSING"

    # Find in all tables for a name equal to the column name and get is type
    for table in tables:
        for column in table["columns"]:
            if (column["name"] == column_name):
                return column["type"]

    result = find_type_in_keyword_dictionary_sql_server(column_name)

    return result


### Get variable name / column name ###
## Parameters
# 1. @line = Database creation script current line text
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


### Get variable type / column type ###
## Parameters
# 1. @line = Database creation script current line text
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


### Get variable lenght / column lenght ###
## Parameters
# 1. @line = Database creation script current line text
# TODO [CURRENTLY NOT USED]
def get_type_lenght(line):
    return None



####################################################
## 3. Utils
####################################################  



### Get the variable type for a stored procedure that got none based on some keywords ###
## Parameters
# 1. @line = Database creation script current line text
def get_type_keyword_dictionary_sql_server():
    return {
        "quantity":"int",
        "count":"int",
        "id":"int"
        }


### Get the variable type for a stored procedure by looking for the name in the dictionary ###
## Parameters
# 1. @keyword = variable name / column name
def find_type_in_keyword_dictionary_sql_server(keyword):
    dictionary = get_type_keyword_dictionary_sql_server()
    for word in dictionary:
        if word in keyword:
            return dictionary[word]
    return "MISSING"
    