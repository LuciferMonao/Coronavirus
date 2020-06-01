import pickle
import json
import requests
import time
import os
import download_database
import sys

def delete_line(amount=1, up=1):
    for _ in range(amount):
        for _ in range(up):
            sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")

def load_obj(name ):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def get():
    countries = {}

    country_list = load_obj("country_list")

    for country in country_list:
        countries[country] = load_obj(country)

    return(countries)

if __name__ == "__main__":
    print("Loading up...")
    download_database.download_database()
    delete_line()

    while True:
        most_cases = ["", 0]
        most_deaths = ["", 0]
        least_cases = ["", 999_000_000_000]
        least_deaths = ["", 999_000_000_000]
        most_deaths_per_case = ["", 0]
        least_deaths_per_case = ["", 999_000_000_000]

        countries = get()
        try:
            fil = 1_000_000#int(input("What should be the minimum?\n"))
            for country in countries:
                if countries[country]["total_cases"] * countries[country]["total_deaths"] * 10 > fil:
                    if countries[country]["total_cases"] > most_cases[1]:
                        most_cases[0] = countries[country]["countryname"]
                        most_cases[1] = countries[country]["total_cases"]
                    if countries[country]["total_deaths"] > most_deaths[1]:
                        most_deaths[0] = countries[country]["countryname"]
                        most_deaths[1] = countries[country]["total_deaths"]
                    if countries[country]["total_cases"] < least_cases[1]:
                        least_cases[0] = countries[country]["countryname"]
                        least_cases[1] = countries[country]["total_cases"]
                    if countries[country]["total_deaths"] < least_deaths[1]:
                        least_deaths[0] = countries[country]["countryname"]
                        least_deaths[1] = countries[country]["total_deaths"]
                    if countries[country]["total_deaths"] / countries[country]["total_cases"] > most_deaths_per_case[1]:
                        most_deaths_per_case[0] = countries[country]["countryname"]
                        most_deaths_per_case[1] = countries[country]["total_deaths"] / countries[country]["total_cases"]
                    if countries[country]["total_deaths"] / countries[country]["total_cases"] < least_deaths_per_case[1]:
                        least_deaths_per_case[0] = countries[country]["countryname"]
                        least_deaths_per_case[1] = countries[country]["total_deaths"] / countries[country]["total_cases"]
            print(f"Most Cases: {most_cases[0]}, {most_cases[1]} \nMost Deaths: {most_deaths[0]}, {most_deaths[1]} \nLeast Cases: {least_cases[0]}, {least_cases[1]} \nLeast Deaths: {least_deaths[0]}, {least_deaths[1]} \nMost Deaths per Case: {most_deaths_per_case[0]}, {most_deaths_per_case[1]} \nLeast Deaths per Case: {least_deaths_per_case[0]}, {least_deaths_per_case[1]}")
        except ValueError:
            delete_line()
            print("Please enter a valid number...")
            time.sleep(2)
            delete_line()

        search = input("What country should be searched?\n").upper()
        if search == "EXIT": break
        for country in countries:
            if search in countries[country]["countryname"].upper() or search in country.upper():
                print("    ----    ")
                print("\n{}:".format(countries[country]["countryname"]))
                print("Cases: {}, Deaths: {}, Deaths per Case: {}\n ".format(countries[country]["total_cases"], countries[country]["total_deaths"], countries[country]["total_deaths"] / countries[country]["total_cases"]))
                print("    ----    ")
