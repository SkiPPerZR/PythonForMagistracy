import requests

print("\nПолучение данных из публичного API")
url_posts = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(url_posts)
if response.status_code == 200:
    posts = response.json()[:5]
    for post in posts:
        print(f"Заголовок: {post['title']}")
        print(f"Тело: {post['body']}")
else:
    print(f"Ошибка при получении постов: {response.status_code}")

print("\nРабота с параметрами запроса (погода)")
city = input("Введите название города: ")
api_key = "69343df8be2f201b540b8f90bbc0ddee"

url_weather = "https://api.openweathermap.org/data/2.5/weather"

params = {"q": city, "appid": api_key, "units": "metric", "lang": "ru"}
weather_response = requests.get(url_weather, params=params)

if weather_response.status_code == 200:
    data = weather_response.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    print(f"В городе {city} сейчас {temp}°C, {desc}.")
elif weather_response.status_code == 404:
    print("Город не найден.")
else:
    print(f"Ошибка при получении данных о погоде: {weather_response.status_code}")

print("\nPOST-запрос для создания нового поста")
post_data = {
    "title": "Почему Человек-Паук лучший герой современности? ",
    "body": "Согласно исследованиям, он больше всего спас людей на улицах Манхетона, и замете без особого вреда для них и инфраструктуре города!",
    "userId": 1
}

post_response = requests.post(url_posts, json=post_data)

if post_response.status_code == 201:
    created_post = post_response.json()
    print(f"Создан пост с ID: {created_post['id']}")
    print(f"Содержимое: {created_post}")
else:
    print(f"Ошибка при создании поста: {post_response.status_code}")


print("\nОбработка ошибок")
test_urls = [
    "https://jsonplaceholder.typicode.com/invalid_endpoint",
    "https://jsonplaceholder.typicode.com/posts/1"
]

for url in test_urls:
    r = requests.get(url)
    if r.status_code == 200:
        print(f"Успешный запрос к {url}")
    elif r.status_code == 404:
        print(f"Ошибка 404: ресурс не найден — {url}")
    elif r.status_code == 400:
        print(f"Ошибка 400: неверный запрос — {url}")
    else:
        print(f"Неизвестная ошибка {r.status_code} при запросе {url}")
