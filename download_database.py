import requests
import json
import pickle
import time
from concurrent import futures

def save_obj(obj, name ):
    with open('data/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def download_database():
    data = requests.get("https://opendata.ecdc.europa.eu/covid19/casedistribution/json/").json()
    countries = {}
    
    for element in data["records"]:
        countries[element["countryterritoryCode"]] = {"total_cases": 0, "total_deaths": 0,"countryname": element["countriesAndTerritories"],"population": element["popData2018"]}

    for element in data["records"]:
        countries[element["countryterritoryCode"]][element["dateRep"]] = {"cases": element["cases"], "deaths": element["deaths"]}
        try:
            countries[element["countryterritoryCode"]]["total_cases"] += int(element["cases"])
            countries[element["countryterritoryCode"]]["total_deaths"] += int(element["deaths"])
        except ValueError:
            pass


    countries.pop("N/A", None)

    for element in countries:
        save_obj(countries[element], element)

    save_obj([country for country in countries], "country_list")





def work_function(intervall):
    download_database()
    wait_time = range(intervall)
    for waited in wait_time:
        time.sleep(1)
        print(f"Waited {waited} of {intervall} seconds...")

if __name__ == "__main__":
    while True:
        try:
            intervall = int(input("How many seconds should be waited between the downloads?\n"))
            while True:
                work_function(intervall)
        except ValueError:
            print("Please enter a valid number...")
            time.sleep(1)