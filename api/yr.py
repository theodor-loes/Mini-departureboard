from .api import Api
from .location import Location


class Yr:
    def __init__(self, location: str):
        self.api = Api
        self.coordinate = self.get_coordinate(location=location)
        self.update()

    def data(self, query: dict):
        # Defining variables to store the data
        data = dict()       # The data per hour
        next_hours = dict() # The data for the next hours (includes information about precipitation)

        _first = True   # Keeps track of the first loop
        today = str()
        # Loops through the api-keys
        for hour_data in self.json:
            time = hour_data['time']
            formatted_time = self.format_time(time)

            hour = formatted_time['clock']['hour']
            date_day = formatted_time['date']['day']

            if _first:  # Input another query for the data including the information about the next hours
                query_hour = {
                    "next_1_hours": {
                        "symbol_code": None,
                        "precipitation_amount": None
                    },
                    "next_6_hours": {
                        "symbol_code": None,
                        "precipitation_amount": None
                    }
                }
                # Assign the formatted data to next_hours
                next_hours = self.format_data(data=hour_data['data'], query=query_hour)
                today = date_day
                _first = False
            
            if date_day != today:
                return next_hours, data

            data[hour] = self.format_data(data = hour_data['data'], query=query)

        return next_hours, data

    def format_data(self, data, query):
        def get_key(key, parent_key=None):
            if parent_key in data.keys():
                for data_subkey in data[parent_key].keys():
                    if key in data[parent_key][data_subkey].keys():
                        return data[parent_key][data_subkey][key]
            else:
                for data_key in data.keys():
                    for data_subkey in data[data_key].keys():
                        if key in data[data_key][data_subkey].keys():
                            return data[data_key][data_subkey][key]
            return None

        formatted_data = dict()
        for key in query.keys():
            if isinstance(query[key], dict):
                formatted_data[key] = dict()
                for subkey in query[key].keys():
                    formatted_data[key][subkey] = get_key(key=subkey, parent_key=key)
            else:
                formatted_data[key] = get_key(key=key)

        return formatted_data

    def update(self):
        self.api = self._collect_data()

    def _collect_data(self):
        url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={self.coordinate["lat"]}&lon={self.coordinate["lon"]}'

        _headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        return Api(url=url, headers=_headers)

    def format_time(self, time):
        T_index = time.find('T')
        date = time[:T_index]
        clock = time[T_index+1:time.find('Z')]

        year, month, day = date.split('-')
        hour, minutes, seconds = clock.split(':')

        _time = {
            'date': {
                'day': day,
                'month': month,
                'year': year
            },
            'clock': {
                'seconds': seconds,
                'minutes': minutes,
                'hour': hour
            }
        }

        return _time

    def get_coordinate(self, location):
        _query = {
            "lat": None,
            "lon": None
        }
        return Location.collect_data(location=location, query=_query)

    @property
    def json(self):
        return self.api.JSON['properties']['timeseries']


if __name__ == '__main__':
    location = "Bjørvika Oslo, No"
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
    print(data['17']['air_temperature'])
