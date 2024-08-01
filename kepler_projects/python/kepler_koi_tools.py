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
        object_list.append({"object_name": object_name, "luminosity": luminosity, "star_color": star_color})
    
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