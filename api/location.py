from .api import Api


class Location:
    def sort_json(JSON, query):
        data = dict()

        properties = JSON['features'][0]['properties']
        for key in query.keys():
            try:
                _ = len(query[key])
                data[key] = dict()
                for subkey in query[key].keys():
                    data[key][subkey] = properties[subkey]
            except:
                data[key] = properties[key]

        return data

    def collect_data(location: str, query: dict):
        _api_key = '257949456eac438fb7a10ee7002fd5a4'
        url = f'https://api.geoapify.com/v1/geocode/search?text={location}&limit=1&apiKey={_api_key}'
        JSON = Api(url).JSON

        data = Location.sort_json(JSON=JSON, query=query)
        return data


# EXAMPLE ON HOW TO USE
if __name__ == "__main__":
    # Defining a location and query
    location = "Grønland Oslo, No"  # <Address> <City>, <Country>
    query = {
        "coordinate": {
            "lon": None,
            "lat": None
        },
        "postcode": None,
        "formatted": None
    }

    # Collecting the query-data in the given format
    print(Location.collect_data(location=location, query=query))

