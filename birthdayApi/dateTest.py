from datetime import date,datetime

date_exp = '2022-05-01'

date_stamp = datetime.strptime(date_exp, '%Y-%m-%d')

date_string = date_stamp.isoformat()

print(date_string)