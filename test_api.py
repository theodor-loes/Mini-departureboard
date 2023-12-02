# Testing the api package

import argparse

from api import Yr


def main():
    argument_choises = [
        "air_pressure_at_sea_level",
        "air_temperature",
        "cloud_area_fraction",
        "relative_humidity",
        "wind_from_direction",
        "wind_speed",
        "symbol_code",
        "precipitation_amount"
    ]

    parser = argparse.ArgumentParser(
        description='Retrieve key-information from a given location.'
    )

    # Positional argument for location
    parser.add_argument('location', help='The location to retrieve information for')

    # Positional argument for key
    parser.add_argument('key', choices=argument_choises, help='The key for the information you want to retrieve')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values of the arguments
    location = args.location
    key = args.key

    query = {
        "air_pressure_at_sea_level": None,
        "air_temperature": None,
        "cloud_area_fraction": None,
        "relative_humidity": None,
        "wind_from_direction": None,
        "wind_speed": None
    }

    yr = Yr(location=location)

    next_hours, data = yr.data(query=query)
    if key in ('symbol_code', 'precipitation_amount'):
        print(next_hours['next_6_hours'][key])
    else:
        for hour in data.keys():
            print(f'{hour} : {data[hour][key]}')

if __name__ == '__main__':
    main()