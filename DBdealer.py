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

def postgresql_to_dataframe(conn, select_query, column_names=None):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, p2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    
    # We just need to turn it into a pandas dataframe
    #df = pd.DataFrame(tupples, columns=column_names)
    if column_names is not None:
    	df = pd.DataFrame(tupples,column_names)
    else:
    	df = pd.DataFrame(tupples)
    return df



if __name__=='__main__':
	# Connect to the database
	conn = connect(param_dic)

	# Execute the "SELECT *" query
	#df = postgresql_to_dataframe(conn, "select * from prueba", column_names)
	df = postgresql_to_dataframe(conn, "SELECT * FROM public.nasa ORDER BY ratio DESC LIMIT 10", column_names)
	#df = postgresql_to_dataframe(conn, "select * from nasa", column_names)
	data = df.to_numpy().T
	print(data)
	for i in range(len(data[1])):
		data[1][i] = str(data[1][i]).lower()
	data = data.T

	# b=data[:,2]
	# b.sort(reverse)
	# b=b[::-1]
	# ranking=b[0:4]
	# print(ranking)

	c=data[data[:,2].argsort()]
	c=c[::-1]
	# newarray=numpy.append(ranking, c, axis = 1)
	print(c)


	#palaba es la entrada de la función buscador de co2
	palabra='pasadena'
	#x = np.where(data[:,1]==palabra)
	
	cities = c.T[1]
	print(cities)
	co2 = c.T[2]
	print(co2)
	ranking = np.linspace(1, len(c), num=len(c), endpoint=True).astype('uint8')
	print(ranking)

	mydict = dict(zip(cities, zip(co2,ranking)))
	print(mydict)
	print(mydict.get(palabra))




	# Close the connection
	conn.close()