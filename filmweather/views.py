import requests, random
from decouple import config
from django.shortcuts import render
from requests.exceptions import RequestException

def index_view(request):
    context = {
        'weather_data': weather_info(),
        'advice_data': advice_info(),
        'omdb_data': omdb_info(),
    }
    return render(request, 'index.html', context)

def weather_info():
    api_key = config('OPENWEATHER_API_KEY')
    city = 'Colonia del Sacramento'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except (RequestException, ValueError) as e:
        print(f"Weather API error: {str(e)}")
        return {'error': str(e)}

def advice_info():
    url = "https://api.adviceslip.com/advice"  
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  
        data = response.json()
        
        if "slip" in data:
            return {
                "advice": data["slip"]["advice"],
                "type": "advice",
                "error": None
            }
        else:
            raise ValueError("Formato de respuesta inesperado")
    
    except (requests.RequestException, ValueError, KeyError) as error:
        print(f"[Advice API] Error: {error}")
        # Fallback: Consejo por defecto
        return {
            "advice": "When in doubt, take a deep breath and try again.",
            "type": "fallback",
            "error": str(error)
        }

def omdb_info(max_retries=3):
    api_key = config('OMDB_API_KEY')

    for _ in range(max_retries):
        imdb_id = f"tt{random.randint(1, 4000000):07d}"
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}&type=movie"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            return {
                "title": data.get("Title", "Título no disponible"),
                "year": data.get("Year", "Año no disponible"),
                "poster": data.get("Poster", False),
            }
        
        except Exception as e:
            print(f"Error en OMDB API: {e}")
            return {
                "title": "Película de ejemplo",
                "year": "N/A",
                "poster": None,
                "error": str(e)
            }