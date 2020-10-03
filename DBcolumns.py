# Define a function that gets the column names from a PostgreSQL table
def get_columns_names(table, connection):

    # declare an empty list for the column names
    columns = []

    # declare cursor objects from the connection    
    col_cursor = connection.cursor()

    # concatenate string for query to get column names
    # SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'some_table';
    col_names_str = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE "
    col_names_str += "table_name = '{}';".format( table )

    try:
        sql_object = sql.SQL( 
            col_names_str # pass SQL statement to sql.SQL() method
        ).format(
            sql.Identifier( table ) # pass the identifier to the Identifier() method
        )
        
        col_cursor.execute( sql_object ) # execute the SQL string to get list with col names in a tuple

        col_names = ( col_cursor.fetchall() ) # get the tuple element from the liast
        
        for tup in col_names: # iterate list of tuples and grab first element
            columns += [ tup[0] ] # append the col name string to the list

        col_cursor.close() # close the cursor object to prevent memory leaks

    except Exception as err:
        print ("get_columns_names ERROR:", err)

    return columns # return the list of column names

# if the connection to PostgreSQL is valid
if conn != None:

    # pass a PostgreSQL string for the table name to the function
    columns = get_columns_names( "nasa" )

    print (columns)