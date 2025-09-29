import aiohttp
import requests
import asyncio

api_key = "***************"
url = "https://api.openweathermap.org/data/2.5/weather"

async def weather_Agent(session,city:str):


    params ={
        "q":city,
        "appid": api_key,
        "units": "metric"
    }
    async with session.get(url, params=params) as response:
        data = await response.json()
        temp = data['main']['temp']


        return f"City :{city} and temperature : {temp} degrees"

async def main():
    cities = ["London", "Paris", "Delhi", "New York"]
    async with aiohttp.ClientSession() as session:
        tasks =[weather_Agent(session,c) for c in cities]
        results = await asyncio.gather(*tasks)
        for res in results:
            print(res)


if __name__ == "__main__":

    asyncio.run(main())
