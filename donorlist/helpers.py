from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic

# Use API to look up geocode of a city
def geocode(city):

	# Key to use OpenCageGeocode API
	key = '9a9d6a61303046c8987b7bf2dc3827ff'
	# Set up call to the OpenCageGeocode API
	geocoder = OpenCageGeocode(key)
	# Store result from API request
	results = geocoder.geocode(city)
	# Return the result of API request
	return results

# Return latitude based on API call results
def get_latitude(results):
	return results[0]['geometry']['lat']

# Return longitude based on API call results
def get_longitude(results):
	return results[0]['geometry']['lng']

# Calculate the miles between two cities
def miles(lat_A, lng_A, lat_B, lng_B):
	return (geodesic((lat_A,lng_A), (lat_B,lng_B)).miles)
