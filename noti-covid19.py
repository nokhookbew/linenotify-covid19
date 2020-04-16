import requests
import schedule
import time
from datetime import datetime

current_infected = 0
current_healed = 0
current_healing = 0
current_die = 0

def send(format_data, now):
    token = '<token form linenotify>'
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Bearer ' + token}
    r = requests.post(url, headers=headers, data={'message': format_data})
    print(r.content, now)

def noti():
    global current_infected
    global current_healed
    global current_healing
    global current_die
    #timestamp
    now = datetime.now()
    response = requests.get('https://covid19.th-stat.com/api/open/today')
    try:
        data = response.json()
        print(data)
        new_infected = int(data['Confirmed'])
        new_healed = int(data['Recovered'])
        new_healing = int(data['Hospitalized'])
        new_die = int(data['Deaths'])
        format_data = ''
        if new_infected != current_infected or new_healed != current_healed or new_healing != current_healing or new_die != current_die:
            for key, value in data.items():
                format_data += key + ': ' + str(value) + '\n'
            send(format_data, now)
            current_infected = new_infected
            current_healed = new_healed
            current_healing = new_healing
            current_die = new_die
        else:
            print('ยอดเท่าเดิม', now)
        print(current_infected)
    except Exception as e:
        print(e)
        format_data = 'api responses something wrong'
        send(format_data, now)

print('running...............')
noti()
schedule.every().hour.do(noti)
while True:
    schedule.run_pending()
    time.sleep(1)
