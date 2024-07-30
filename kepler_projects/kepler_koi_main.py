import pandas as pd
import kepler_koi_tools

#Set the input and output paths
input_path = 'kepler_projects\\kepler_exoplanet_data\\koi_cumulative.csv'
#Ideally this wouldn't be checked in, but I wanted to provide the results without forcing code checkout
output_path = 'kepler_projects\\kepler_exoplanet_data\\output_cumulative.csv'

#Read the data from a csv. This was meant to be the Kepler KOI cumulative list
#obtained from https://exoplanetarchive.ipac.caltech.edu/docs/data.html
#Also, this is a link to the Kepler KOI column definitions in the input file
#https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html
data = pd.read_csv(input_path)
    
#Compile the list
#Add the objects to the record
#Write the record to a csv
objects = kepler_koi_tools.compile_list_of_objects(data)
record_df = pd.DataFrame(objects, columns=["object_name", "luminosity", "star_color"])    
record_df.to_csv(output_path, mode="w", header=True, index=False)

#TODO: return a count for potentially habitable planets by star color
#TODO: implement habitability analysis using established models
#TODO: calculate stats for each color group (average luminosity, number of objects, etc.)
#TODO: implement error handling
#TODO: see if I can implement parallelization since the dataset is large. Also look
#        into libraries like multiprocessing or concurrent.futures.
#TODO: explore caching for expensive calculations like luminosity estimation to avoid redundant computations