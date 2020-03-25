import requests
import schedule
import time
from datetime import datetime

current_infected = 0
current_healed = 0
current_healing = 0
current_die = 0

def noti():
    global current_infected
    global current_healed
    global current_healing
    global current_die
    #timestamp
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    response = requests.get('https://covid19-cdn.workpointnews.com/api/constants.json')
    data = response.json()
    print(data)
    new_infected = int(data['ผู้ติดเชื้อ'])
    new_healed = int(data['หายแล้ว'])
    new_healing = int(data['กำลังรักษา'])
    new_die = int(data['เสียชีวิต'])
    format_data = ''
    token = '<token form linenotify>'
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
              'Authorization': 'Bearer ' + token}
    if new_infected != current_infected or new_healed != current_healed or new_healing != current_healing or new_die != current_die:
        for key, value in data.items():
            format_data += key + ': ' + value + '\n'
        r = requests.post(url, headers=headers, data={'message': format_data})
        current_infected = new_infected
        current_healed = new_healed
        current_healing = new_healing
        current_die = new_die
        print(r.content, timestamp)
    else:
        print('ยอดเท่าเดิม', timestamp)
    print(current_infected)

schedule.every().hour.do(noti)
while True:
    schedule.run_pending()
    time.sleep(1)