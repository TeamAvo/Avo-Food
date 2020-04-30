import os
import json
import random
import requests
from datetime import datetime
from pytz import timezone

days_short = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
days_full = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

with open('temp/accordion.html','r', encoding='UTF8') as f:
    accordion_raw = f.read()

with open('temp/item.html','r', encoding='UTF8') as f:
    item_raw = f.read()

with open('temp/card.html','r', encoding='UTF8') as f:
    card_raw = f.read()

with open('temp/menu.html','r', encoding='UTF8') as f:
    menu_raw = f.read()


week_type = 'This'
item_list = ''
avon = datetime.now(timezone('US/Eastern'))

for day in range(0, 7):
    response = requests.get(f"https://e82437da.ngrok.io/cafeapi/food?day={day}")
    data = json.loads(response.text)
    #print(data)
    
    card_list = ''
    for time_meal in data:
        menu_list = ''
        for meal_info in time_meal['data']:
            menu_list += menu_raw.replace('{menu}', meal_info) + '\n'

        if menu_list == '':
            menu_list = '<p>There is no infromation.</p>'
            img_url = 'https://source.unsplash.com/1600x900/?food'
        else:
            img = random.choice(time_meal['data'])
            img_url = f'https://source.unsplash.com/1600x900/?{img}'

        card = card_raw.replace('{img}', img_url.replace(' ', '%20'))
        card = card.replace('{time}', time_meal['title'])
        card_list += card.replace('<!-- Menus -->', menu_list) + '\n'

        #print(menu_list)
        #print(card)
    
    item = item_raw.replace('{WeekType}', week_type)
    item = item.replace('headingOne', f'heading{week_type}{days_short[day]}')
    item = item.replace('collapseOne', f'collapse{week_type}{days_short[day]}')
    item = item.replace('{day}', days_short[day][:1])

    if day == avon.weekday() + 1 % 6:
        item = item.replace('{bool}', 'true')
        item = item.replace('{show}', ' show')
        item = item.replace('{day_title}', days_full[day] + ' - Today')
    else:
        item = item.replace('{bool}', 'false')
        item = item.replace('{show}', '')
        item = item.replace('{day_title}', days_full[day])
    
    item_list += item.replace('<!-- card -->', card_list) + '\n'
    #print(item)

accordion = accordion_raw.replace('{WeekType}', week_type)
accordion = accordion.replace('{Week_Title}', f'{week_type} Week\'s Menus')
accordion = accordion.replace('<!-- WeekItems -->', item_list)

with open('index_template.html','r', encoding='UTF8') as f:
    html = f.read()

if os.path.isfile('index.html'):
  os.remove('index.html')

html = html.replace('<!-- ThisWeekDropDown -->', accordion)
with open('index.html', 'w', encoding='UTF8') as f:
    f.write(html)
