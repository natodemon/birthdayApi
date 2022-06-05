from datetime import date,datetime

date_0 = '2022-02-17'
today = datetime.now()

date_stamp = datetime.strptime(date_0, '%Y-%m-%d')

delta = date_stamp.replace(year=2023).date() - today.date()
delta_1 = today.date() - date_stamp.replace(year=2023).date()

print(delta)