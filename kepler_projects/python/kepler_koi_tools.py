import numpy as np

"""Calculates the luminosity of a star given its radius and temperature.
    
    Args:
      radius: The radius of the star in meters.
      temperature: The effective temperature of the star in Kelvin.
      
    Returns:
      The luminosity of the star in watts.
"""
def calculate_luminosity(radius, temperature):
    
    #I obtained this formula from an internet search. It seems accurate,
    #though I don't know how precise it is. This formula is known as
    #the Stefan-Boltzmann Law. https://www.e-education.psu.edu/astro801/content/l3_p5.html.
    radius = radius * 6.957e8
    sigma = 5.670374419e-8
    luminosity = 4 * np.pi * sigma * radius**2 * temperature**4
    
    return luminosity

"""This function iterates through the Kepler data and creates a list of dictionaries,
where each dictionary represents a processed object (presumably a star-planet system).

    Returns:
        object_list: A list of dictionaries.
"""
def compile_list_of_objects(data):
    object_list = []
    
    for index, row in data[:-1].iterrows():
        object_name = str(row["kepler_name"]) #nan is returned when the object name isn't populated in the koi csv.
                                              #The python math library has a .isnan() method. That might be another route
                                              # to assign a string to the missing kepler_name.
        if object_name == "nan":
            object_name = "OBJECT NAME WASN'T RECORDED"
        luminosity = calculate_luminosity(row["koi_srad"], row["koi_steff"])
        host_color = estimate_host_color(row["koi_steff"])
        koi_disposition = row["koi_disposition"]
        koi_pdisposition = row["koi_pdisposition"]
        object_list.append({"object_name": object_name, "host_luminosity": luminosity, "host_color": host_color,
                            "koi_disposition": koi_disposition, "koi_pdisposition": koi_pdisposition})
    
    return object_list

"""This function estimates the color of a star based on its effective temperature, assuming a blackbody model.

    Args:
        object_data: The effective temperature of the star in Kelvin
        
    Returns:
        host_color: A string representing the estimated color of the star.
"""
def estimate_host_color(object_data):
    #I've spot checked some stars using https://science.nasa.gov/exoplanets/exoplanet-catalog/
    #and this (simplified) algorithm is roughly accurate
    temperature = object_data
    
    if temperature > 30000:
        return "Blue"
    elif temperature > 10000:
        return "Blue-white"
    elif temperature > 7500:
        return "White"
    elif temperature > 6000:
        return "Yellow-white"
    elif temperature > 5200:
        return "Yellow"
    elif temperature > 3700:
        return "Orange"
    else:
        return "Red"
    
"""Counts the number of exoplanets in each disposition category.

    Iterates through the provided object data and categorizes each row based on its
    'koi_disposition' value.

    Args:
        object_data (pandas.DataFrame): DataFrame containing exoplanet data.
            Expected column: 'koi_disposition'.

    Returns:
        tuple: A tuple of four integers representing the counts of confirmed,
            false positive, candidate, and unknown exoplanets.
"""    
def get_exoplanet_disposition(object_data):
    confirmed = 0
    false_positives = 0
    candidates = 0
    unknown = 0
    
    for index, row in object_data[:-1].iterrows():
        if row["koi_disposition"] == "CONFIRMED":
            confirmed += 1
        elif row["koi_disposition"] == "FALSE POSITIVE":
            false_positives += 1
        elif row["koi_disposition"] == "CANDIDATE":
            candidates += 1
        else:
            unknown += 1
    
    return confirmed, false_positives, candidates, unknown


"""Counts confirmed exoplanet host stars by color category.

    Iterates through the provided object data, filtering for confirmed exoplanets.
    For each confirmed exoplanet, estimates the host star's color based on its
    effective temperature (koi_steff) and increments the corresponding counter.

    Args:
        object_data (pandas.DataFrame): DataFrame containing exoplanet data.
            Expected columns: 'koi_disposition', 'koi_steff'.

    Returns:
        tuple: A tuple of seven integers representing the counts of confirmed
            exoplanet host stars in the following color categories:
            (blue, blue-white, white, yellow-white, yellow, orange, red).
"""
def get_confirmed_by_host_color(object_data):
    host_star_blue = 0
    host_star_bluewhite = 0
    host_star_white = 0
    host_star_yellowwhite = 0
    host_star_yellow = 0
    host_star_orange = 0
    host_star_red = 0
    
    for index, row in object_data[:-1].iterrows():
        if row["koi_disposition"] == "CONFIRMED":
            
            host_star = estimate_host_color(row["koi_steff"])
            if host_star == "Blue":
                host_star_blue += 1
            elif host_star == "Blue-white":
                host_star_bluewhite += 1
            elif host_star == "White":
                host_star_white += 1
            elif host_star == "Yellow-white":
                host_star_yellowwhite += 1
            elif host_star == "Yellow":
                host_star_yellow += 1
            elif host_star == "Orange":
                host_star_orange += 1
            elif host_star == "Red":
                host_star_red += 1
                
    return host_star_blue, host_star_bluewhite, host_star_white, host_star_yellowwhite, host_star_yellow, host_star_orange, host_star_red