import mysql.connector as mysql
import pandas as pd
import datetime as dt

#список станций, пики которых нам нужны
ListSta=['B209','B210','B213','B214','B215','BRK9']

#параметры для входа в БД
host="192.168.35.11"
user="sysop"
passwd="sysop"
dbase="seiscomp3"

#рассматриваемый интервал времени
date1="2021-04-27 10:00:00"
date2="2021-04-27 20:00:00"

#подключение к БД
db = mysql.connect(host=host, user=user, passwd=passwd, database=dbase)
cur = db.cursor()

#запрос к БД
MyDict=[]
MyDict.append(date1)
MyDict.append(date2)
cur.execute("Select _oid, time_value, time_value_ms, waveformID_networkCode,waveformID_stationCode,waveformID_locationCode,waveformID_channelCode From seiscomp3.Pick WHERE unix_timestamp(%s)<=unix_timestamp(time_value) AND unix_timestamp(%s)>=unix_timestamp(time_value);",MyDict)

#обработка результатов запроса, делим его на списки. Время преобразуем в datetime
rows = cur.fetchall()
pickID=[str(i[0]) for i in rows]
timeID=[str(i[1]) for i in rows]
msID=[str(i[2]) for i in rows]
time2=[timeID[i]+'.'+msID[i] for i in range(len(timeID))]
timeID=[dt.datetime.strptime(i, '%Y-%m-%d %H:%M:%S.%f') for i in time2]
netID=[str(i[3].decode()) for i in rows]
staID=[str(i[4].decode()) for i in rows]
locID=[str(i[5].decode()) for i in rows]
chnID=[str(i[6].decode()) for i in rows]

#преобразуем списки во фрейм, фильтруем по списку станций и сохраняем результат в файл
frame=pd.DataFrame(list(zip(pickID,timeID,netID,staID,locID,chnID)), columns=['pickID','date','net','sta','loc','ch'])
df=frame[frame['sta'].isin(ListSta)]
df.to_excel('pick.xls', index=False)