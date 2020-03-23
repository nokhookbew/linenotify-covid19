import requests
import schedule
import time

current_infected = 0

def noti():
    global current_infected
#     print('called func')
#     print(current_infected)
    response = requests.get('https://covid19-cdn.workpointnews.com/api/constants.json')
    data = response.json()
    print(data)
    new_infected = int(data['ผู้ติดเชื้อ'])
    # print(new_infected)
    format_data = ''
    # print(format_data)
    token = '<token form linenotify>'
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
              'Authorization': 'Bearer ' + token}
    if new_infected > current_infected:
        for key, value in data.items():
            format_data += key + ': ' + value + '\n'
        r = requests.post(url, headers=headers, data={'message': format_data})
        current_infected = new_infected
        print(r.content)
    else:
        print('ยอดเท่าเดิม', new_infected)
    print(current_infected)

schedule.every().hour.do(noti)
while True:
    schedule.run_pending()
    time.sleep(1)
