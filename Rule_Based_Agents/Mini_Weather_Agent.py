import requests
import time

def get_weather(city):

    url = f"https://wttr.in/{city}"
    params = params = {"format": "j1"}
    response = requests.get(url,params=params)
    print("Response status", response.status_code)
    # print("Response text", response.text)
    # print("Response headers", response.headers)

    if response.status_code == 200:
        # print("Feels like C: ",data['current_condition'][0]['FeelsLikeC'])
        # print("weatherDesc: ",data['current_condition'][0]['weatherDesc'][0]['value'])
        # print("response",response)
        return response.json()


    else:
        return None

def Extract_data(data):
    current_temp = data['current_condition'][0]['FeelsLikeC']
    current_weather = data['current_condition'][0]['weatherDesc'][0]['value']

    #return f"----------------------current temperature is <{current_temp}C> and current weather is <{current_weather}>-------------"
    return current_temp

def weather_Agent():
    user_input = input("Enter your city:")
    get_data = get_weather(user_input)
    # parse_data = Extract_data(get_data)

    if get_data:
        print("success")
        parse_data = Extract_data(get_data)
        print(parse_data)
        return parse_data

    else:
        return None

## Main function calling

if __name__=="__main__":


    start = time.perf_counter() ## Start time before calling

    result = weather_Agent()

    end = time.perf_counter()  ## End time after function completed

    print(f"time taken :{end - start:.6f} seconds")

    if int(result) < 10:
        print("Too Cold")

    elif int(result) > 30:
        print("Hot Outside")

    else:
        print("Normal temperature")