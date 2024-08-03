import pandas as pd
import kepler_koi_tools

"""This program reads the Kepler Objects of Interests list and calculates the
   estimated color of the star for each object, based on luminosity. Then, it writes
   the object name, luminosity, and estimated star color to a csv.
"""

#TODO: return a count for potentially habitable planets by star color
#TODO: implement habitability analysis using established models
#TODO: calculate stats for each color group (average luminosity, number of objects, etc.)
#TODO: implement error handling
#TODO: see if I can implement parallelization since the dataset is large. Also look
#        into libraries like multiprocessing or concurrent.futures.
#TODO: explore caching for expensive calculations like luminosity estimation to avoid redundant computations

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
#Add the objects to the record
#Write the record to a csv
objects = kepler_koi_tools.compile_list_of_objects(data)
record_df = pd.DataFrame(objects, columns=["object_name", "luminosity", "star_color", "koi_pdisposition", "koi_disposition"])    
record_df.to_csv(output_path, mode="w", header=True, index=False)

confirmed_exoplanets, false_positive_exoplanets, candidate_exoplanets, unknown = kepler_koi_tools.get_exoplanet_disposition(data)
print("Confirmed: " + str(confirmed_exoplanets))
print("False Positives: " + str(false_positive_exoplanets))
print("Candidates: " + str(candidate_exoplanets))
print("Unknowns: " + str(unknown))

host_star_blue, host_star_bluewhite, host_star_white, host_star_yellowwhite, host_star_yellow, \
   host_star_orange, host_star_red = kepler_koi_tools.get_confirmed_by_star_color(data)
print("Confirmed blue stars with exoplanets: " + str(host_star_blue))
print("Confirmed blue-white stars with exoplanets: " + str(host_star_bluewhite))
print("Confirmed white stars with exoplanets: " + str(host_star_white))
print("Confirmed yellow-white stars with exoplanets: " + str(host_star_yellowwhite))
print("Confirmed yellow stars with exoplanets: " + str(host_star_yellow))
print("Confirmed orange stars with exoplanets: " + str(host_star_orange))
print("Confirmed red stars with exoplanets: " + str(host_star_red))
