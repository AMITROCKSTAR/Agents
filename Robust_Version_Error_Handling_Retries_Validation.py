import requests
import time
import re

api_key = (❁´◡`❁)
url = "https://api.openweathermap.org/data/2.5/weather"

def is_valid_city(city:str)->bool:
    """Allow only letters and spaces , min length 2"""
    return bool(re.match(r"^[a-zA-Z\s]{2,}$",city))

def fetch_weather(city:str , retries=3, backoff=2):
    if not is_valid_city(city):
        return f"Invalid city name : '{city}' . Please try again"
    
    params = {"q":city,"appid":api_key,"units":"metric"}

    for attempt in range(1, retries+1):
        try:
            resp=requests.get(url,params=params,timeout=5)
            resp.raise_for_status()
            data= resp.json()

            temp=data["main"]["temp"]
            desc = data["weather"][0]["description"].title()
            return f"{city}:{temp} C , {desc}"
        
        except requests.exceptions.Timeout:
            print(f"Timeout , retrying {attempt}/{retries}...")
        except requests.exceptions.RequestException as e:
            return f" API error : {e}"
        
        except KeyError:
            return f" Could'nt parse weather for {city}"
        
        time.sleep(backoff** attempt) ## Exponential wait

    return f"Failed to fetch weather for {city} after {retries} retries"


if __name__=="__main__":
    city = input("Enter a city: ")
    print(fetch_weather(city))
