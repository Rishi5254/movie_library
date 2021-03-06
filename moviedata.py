import requests


def search_movie(movie_name):
    parameters = {
        'api_key': '0831005b836fca6472acac98e025e8a7',
        'language': 'en-US',
        'query': movie_name,
        'region': 'IN-AP',
    }
    data = requests.get(url='https://api.themoviedb.org/3/search/movie', params=parameters).json()['results'][:3]
    return data

