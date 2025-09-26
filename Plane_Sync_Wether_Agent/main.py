#%%
import requests

def wether_agent(user_input):

    api_key = "138b7e69f73bd092072b032de7d5c30d"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params ={
              "q":user_input,
              "appid": api_key,
              "units": "metric"
    }

    response = requests.get(url, params=params)

    data = response.json()
    temp=City=humidity=''
    if data:
        #print("raw text :", response.text)
        # print("json: ",data)
        # print(f"Co-ordinates are ---> Longitude :{data['coord']['lon']} and Latitude : {data['coord']['lat']} ")
        # print(f"Weather are ---> main :{data['weather'][0]['main']} and description : {data['weather'][0]['description']} ")
        # print(f"Name : {data['name']}")
        temp = data['main']['temp']
        City = data['name']
        humidity = data['main']['humidity']

    return f"{City} : {temp} C : {humidity} "

if __name__== "__main__":
    user_input = input("Enter City: ")
    print(wether_agent(user_input))
