#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import cv2
import numpy as np
import pandas as pd
import psycopg2 as p2
#from psycopg2 import sql, connect


#################################################################################
# MAIN FUNCTIONS
#################################################################################


# Returns Ranking of (number_cities) elements from top or button 
def get_ranking_arr(comm, number_cities, top_button):
	if not top_button: select_string = "SELECT * FROM public.nasa ORDER BY ratio DESC LIMIT " + str(number_cities)
	else: select_string = "SELECT * FROM public.nasa ORDER BY ratio DESC LIMIT " + str(number_cities)
	df = postgresql_to_dataframe(comm,select_string)
	ranking = df.to_numpy()


# Returns city info from city_name
def get_city_info(city_name):
	select_string = "SELECT * FROM public.nasa ORDER BY ratio DESC LIMIT " + str(number_cities)
	df = postgresql_to_dataframe(comm,select_string)
	ranking = df.to_numpy()


# Return randomized image
def create_image():
	...


# Return some kind of plot
def create_plot():
	...


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
        sql_object = p2.SQL( 
            col_names_str # pass SQL statement to sql.SQL() method
        ).format(
            p2.Identifier( table ) # pass the identifier to the Identifier() method
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