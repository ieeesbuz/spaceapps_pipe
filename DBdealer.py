import psycopg2 as p2
import pandas as pd
import sys
import numpy as np

# Connection parameters, yours will be different
param_dic = {
    "host"      : "192.168.0.120",
    "database"  : "mydb",
    "user"      : "postgres",
    "password"  : "WoodenRumba00"
}

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    print(22)
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = p2.connect(**params_dic)
        print("Connection successful")
    except (Exception, p2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    return conn

def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    
    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df



if __name__=='__main__':
	# Connect to the database
	conn = connect(param_dic)
	column_names = ["id", "ciudades", "co2"]
	# Execute the "SELECT *" query
	df = postgresql_to_dataframe(conn, "select * from prueba", column_names)
	data = df.to_numpy()
	print(data)

	b=data[:,2]
	b.sort()
	b=b[::-1]
	ranking=b[0:4]
	print(ranking)
	c=np.sort(data, axis=2)
	# newarray=numpy.append(ranking, c, axis = 1)
	print(c)




	# Close the connection
	conn.close()