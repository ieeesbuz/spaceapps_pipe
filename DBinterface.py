#!/usr/bin/python3
# -*- coding: utf-8 -*-

import utils as ut

class nasaDBinterface(object):
	def __init__ (self):
		path = "/plots"

		try:
		    os.mkdir(path)
		except OSError:
		    print ("Creation of the directory %s failed" % path)
		else:
		    print ("Successfully created the directory %s " % path)

		self.param_dic = {
		    "host"      : "192.168.0.120",
		    "database"  : "mydb",
		    "user"      : "postgres",
		    "password"  : "WoodenRumba00"
			}



	def get_ranking(self, number_cities, top_button=True):
		comm = ut.commect(self.param_dic)
		
		ranking = None
		if comm != None: ranking = ut.get_ranking_arr(comm,number_cities, top_button)
		
		comm.close()

		return ranking

	def get_consulta(self, city_name):
		comm = ut.commect(self.param_dic)
		
		city_info = None
		if comm != None: city_info = ut.get_city_info(comm,city_name)
		
		comm.close()

		return city_info

	def get_image(self):
		comm = ut.commect(self.param_dic)
		
		image_name = None
		if comm != None: image_name = ut.create_image(comm)
		
		comm.close()

		return image_dir

	def get_plot(self):
		comm = ut.commect(self.param_dic)
		
		plot_name = None
		if comm != None: plot_name = ut.create_plot(comm)
		
		comm.close()

		return plot_name