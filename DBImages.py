from simple_image_download import simple_image_download as simp
from DBinterface import nasaDBinterface

interfase = nasaDBinterface()
city = get_random_city()

response = simp.simple_image_download


response().download( city , 5)


#print(response().urls( ciudad , 5))

def get_random_city():
    cities_list = -....Msnurl

    city = cities_list[random.randint(0, len(cities_list)-1)]
    return city 