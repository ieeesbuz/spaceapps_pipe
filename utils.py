#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import cv2
import random
import numpy as np
import pandas as pd
import psycopg2 as p2
import matplotlib.pyplot as plt 
from psycopg2 import sql, connect
from DBimages import simple_image_download


#################################################################################
# MAIN FUNCTIONS
#################################################################################


# Returns Ranking of (number_cities) elements from top or button 
def get_ranking_arr(comm, number_cities, top_button):
	if top_button is True: select_string = "SELECT name, ratio, id FROM public.nasa WHERE population > 10000 AND ratio > 0.1 ORDER BY ratio  DESC LIMIT " + str(number_cities)
	else: select_string = "SELECT DISTINCT name, ratio FROM public.nasa WHERE population > 10000 AND ratio > 0.1 ORDER BY ratio ASC LIMIT " + str(number_cities)
	df = psql_df(comm,select_string)
	ranking = df.to_numpy()

	return ranking	

# Returns city info from city_name
def get_city_info(comm,city_name):
	select_string = "SELECT id, name, ratio FROM public.ranking WHERE LOWER(name) = '" + city_name + "'"
	df = psql_df(comm,select_string)
	city_info = df.to_numpy()

	return city_info


# Return randomized image
def create_image(comm):
	city = get_random_city(comm)
	#city = city + " ,USA"

	response = simple_image_download()
	image_dir = response.download(city , 1)
	
	return image_dir


# Return some kind of plot
def create_ranking_plot(comm, number_cities, top_button):
	ranking = get_ranking_arr(comm,number_cities,top_button)
	left = np.linspace(1, len(ranking), num=len(ranking), endpoint=True).astype('uint8').tolist()
	height = ranking[:,1].tolist()
	tick_label = ranking[:, 0].tolist() 

	plt.bar(left, height, tick_label = tick_label, 
  				width = 0.8, color = ['black','purple']) 
	# naming the x-axis 
	plt.xlabel('City') 
	# naming the y-axis 
	plt.ylabel('CO2 Kg/Person') 
	# plot title 
	plt.title('CO2 Ranking') 
	plot_dir = './plots/ranking.jpg'
	plt.savefig(plot_dir)
	return plot_dir



#################################################################################
# AUXILIAR FUNCTIONS
#################################################################################

# Connect to database from parameters
def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = p2.connect(**params_dic)
        print("Connection successful")
    except (Exception, p2.DatabaseError) as error:
        print(error) 
    return conn



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
        print ("get_columns_names ERROR: ", err)

    return columns # return the list of column names



def psql_df(comm, select_query, column_names=None):
	"""
	Tranform a SELECT query into a pandas dataframe
	"""
	cursor = comm.cursor()
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

def get_big_cities_list(comm):
	select_string = "SELECT name FROM public.nasa WHERE population > 100000 AND ratio > 0.1 ORDER BY ratio  ASC LIMIT 1000"
	df = psql_df(comm,select_string)
	cities_list = df.to_numpy()

	return cities_list



def get_random_city(comm):
    cities_list = get_big_cities_list(comm)

    city = cities_list[random.randint(0, len(cities_list)-1)]
    city = str(' '.join(city))
    return city


def _create_directories(self, main_directory, name):
    name = name.replace(" ", "_")
    try:
        if not os.path.exists(main_directory):
            os.makedirs(main_directory)
            time.sleep(0.2)
            path = (name)
            sub_directory = os.path.join(main_directory, path)
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)
        else:
            path = (name)
            sub_directory = os.path.join(main_directory, path)
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)

    except OSError as e:
        if e.errno != 17:
            raise
        pass
    return


#################################################################################
# DEBUG... TO DELETE
#################################################################################

table = "nasa"
param_dic = {
		    "host"      : "192.168.0.120",
		    "database"  : "mydb",
		    "user"      : "postgres",
		    "password"  : "WoodenRumba00"
			}

connection = connect(param_dic)

# columns = get_columns_names(table,connection)

# print(columns)

# select_query_0 = "SELECT " + str(', '.join(columns[0:3])) + " FROM " + table

# df_1_3 = psql_df(connection, select_query_0, column_names=None)

# print(df_1_3.to_numpy())

ranking = get_ranking_arr(connection, 5, True)

print(ranking)

city_info = get_city_info(connection,'new york')

print(city_info)

dir_image = create_image(connection)

print(dir_image)

dir_plot = create_ranking_plot(connection,25,True)

print(dir_plot)