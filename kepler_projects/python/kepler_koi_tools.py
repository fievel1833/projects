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
    #the Stefan-Boltzman Law. https://www.e-education.psu.edu/astro801/content/l3_p5.html.
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
        object_name = str(row["kepler_name"])
        if object_name == "nan": #nan is returned when the object name isn't populated in the koi csv
            object_name = "OBJECT NAME WASN'T RECORDED" #I feel like there's a better way to do this
        luminosity = calculate_luminosity(row["koi_srad"], row["koi_steff"])
        star_color = estimate_star_color(row["koi_steff"])
        koi_disposition = row["koi_disposition"]
        koi_pdisposition = row["koi_pdisposition"]
        object_list.append({"object_name": object_name, "luminosity": luminosity, "star_color": star_color,
                            "koi_disposition": koi_disposition, "koi_pdisposition": koi_pdisposition})
    
    return object_list

"""This function estimates the color of a star based on its effective temperature, assuming a blackbody model.

    Args:
        object_data: The effective temperature of the star in Kelvin
        
    Returns:
        star_color: A string representing the estimated color of the star.
"""
def estimate_star_color(object_data):
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
    
"""This function groups the exoplanet candidates listed in the KOI by disposition."""    
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
        
def get_confirmed_by_star_color(object_data):
    host_star_blue = 0
    host_star_bluewhite = 0
    host_star_white = 0
    host_star_yellowwhite = 0
    host_star_yellow = 0
    host_star_orange = 0
    host_star_red = 0
    
    for index, row in object_data[:-1].iterrows():
        if row["koi_disposition"] == "CONFIRMED":
            
            host_star = estimate_star_color(row["koi_steff"])
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