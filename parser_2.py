import requests
from bs4 import BeautifulSoup as bs
import json
import os

URL_TEMPLATE = "https://www.leagueoflegends.com/ru-ru/news/tags/patch-notes/"
r = requests.get(URL_TEMPLATE)
soup = bs(r.content, 'html.parser')
path = "C:/Users/durba/Desktop/PatchNotesGenerator-master/json"
if not os.path.exists(path):
    os.makedirs(path)
# Берём линк, после парсим на название тайтла обновы

for update in soup.find_all('li', {'class': 'style__Item-sc-106zuld-3 a-DAap'}):

        title = update.find('h2', {'class': 'style__Title-sc-1h41bzo-8 fEywOQ'}).text.strip()
        url = 'https://www.leagueoflegends.com'+update.a['href']
        r = requests.get(url)
        soup = bs(r.content, 'html.parser')
        for description in soup.find_all('div', {'class': 'style__Content-sc-17x3yhp-1 bkyeTj'}):
              value = description.find('blockquote', {'class': 'blockquote context'}).text.strip() 
              image_url = description.find('a', {'class' : 'skins cboxElement'})['href']
        print(title, end = '\n')
        print(url, end = '\n')
        print(value, end = '\n')
        print(image_url, end = '\n')
        print(len(value), end = '\n\n\n\n')
        while (len(value) > 1000):
              value = value[:value.rfind(' ')]

    # Создание объекта JSON
        new_json_obj = {
                            "content": "@everyone",
                            "embeds": [
                                {
                                    "title": title,
                                    "url": url,
                                    "color": 15844366,
                                    "fields": [
                                        {
                                            "name": "~",
                                            "value": ">>> " + value,
                                            "inline": True
                                        }
                                    ],
                                    "author": {
                                        "name": "League of Legends"
                                    },
                                    "image": {
                                        "url": image_url
                                    },
                                    "thumbnail": {
                                        "url": "https://patchbot.io/cdn/games/12/league_of_legends_sm.webp"
                                    }
                                }
                            ],
                            "attachments": []
                        }

        # Сохранение объекта JSON
        filename = f"{title}.json"
        with open(os.path.join(path, filename), 'w', encoding='utf-8') as f:
            json.dump(new_json_obj, f, ensure_ascii=False)
