import pandas as pd
import kepler_koi_tools
import database_tools

"""This program reads the Kepler Objects of Interests list and calculates the
   estimated color of the star for each object, based on the Stefan-Boltzmann Law.
   Then, it writes the object data to a csv.
"""

#TODO: implement habitability analysis using established models
#TODO: calculate stats for each color group (average luminosity, number of objects, etc.)
#TODO: implement error handling
#TODO: see if I can implement parallelization since the dataset is large. Also look
#        into libraries like multiprocessing or concurrent.futures.
#TODO: explore caching for expensive calculations like luminosity estimation to avoid redundant computations
#TODO: store data in a database such as MongoDb
#TODO: implement an EFK stack for logging and visualization
#TODO: explore mongodb or postgres instead of outputting to a csv


#Set the input and output paths
input_path = 'kepler_projects\\python\\kepler_exoplanet_data\\koi_cumulative.csv'
#Ideally this wouldn't be checked in, but I wanted to provide the results without forcing code checkout
output_path = 'kepler_projects\\python\\kepler_exoplanet_data\\output_cumulative.csv'

#Read the data from a csv. This was meant to be the Kepler KOI cumulative list
#obtained from https://exoplanetarchive.ipac.caltech.edu/docs/data.html.
#Also, this is a link to the Kepler KOI column definitions in the input file
#https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html.
data = pd.read_csv(input_path)

#Compile the list
#Add the objects to the record with the appropriate columns
#Write the record to a csv and overwrite if it exists
objects = kepler_koi_tools.compile_list_of_objects(data)

#Try to store our objects in mongodb, but use a csv
#  if there isn't a connection to the database.
#If you supply a filepath for the output path, the
#  data will be stored in a csv instead of attempting
#  to store in a database first.
database_tools.store_in_database(objects)

#Print the results
confirmed_exoplanets, false_positive_exoplanets, candidate_exoplanets, unknown = kepler_koi_tools.get_exoplanet_disposition(data)
print("Confirmed: " + str(confirmed_exoplanets))
print("False Positives: " + str(false_positive_exoplanets))
print("Candidates: " + str(candidate_exoplanets))
print("Unknowns: " + str(unknown))

#Interestingly, while writing this program, I noticed no exoplanets were discovered around blue or blue-white stars by Kepler.
#I looked into why and it turns out blue and blue-white stars are massive, burn hot, and have a shorter lifespan than other
# stars. The belief is that those stars have less time for a planet to form.
host_star_blue, host_star_bluewhite, host_star_white, host_star_yellowwhite, host_star_yellow, \
   host_star_orange, host_star_red = kepler_koi_tools.get_confirmed_by_host_color(data)
print("Confirmed blue stars with exoplanets: " + str(host_star_blue))
print("Confirmed blue-white stars with exoplanets: " + str(host_star_bluewhite))
print("Confirmed white stars with exoplanets: " + str(host_star_white))
print("Confirmed yellow-white stars with exoplanets: " + str(host_star_yellowwhite))
print("Confirmed yellow stars with exoplanets: " + str(host_star_yellow))
print("Confirmed orange stars with exoplanets: " + str(host_star_orange))
print("Confirmed red stars with exoplanets: " + str(host_star_red))
