import matplotlib.pyplot as plt 
from DBinterface import nasaDBinterface
import numpy as np

interface=nasaDBinterface()
ranking=interface.get_ranking_arr()

# x-coordinates of left sides of bars 
left = [1, 2, 3, 4, 5] 

# heights of bars 
#height = [10, 24, 36, 40, 5] 
height = [ranking[:,1]]

# labels for bars 
#tick_label = ['Nueva York', 'Los Angeles', 'Pasadena', 'Las Vegas', 'California'] 
tick_label = [ranking[:, 0]] 

# plotting a bar chart 
plt.bar(left, height, tick_label = tick_label, 
  width = 0.8, color = ['black','purple']) 

# naming the x-axis 
plt.xlabel('City') 
# naming the y-axis 
plt.ylabel('CO2/Person') 
# plot title 
plt.title('CO2 Ranking') 
#plt.savefig('PLOT.jpg')
# function to show the plot
 
plt.show()