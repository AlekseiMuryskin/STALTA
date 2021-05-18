from obspy import read
from obspy.clients.arclink.client import Client
from obspy.core import UTCDateTime

arc_host = '192.168.35.11'
arc_port = '18001'
arc_user = 'sysop'

t_start=UTCDateTime("2021-04-24T18:00:00")
t_end=UTCDateTime("2021-04-24T20:00:00")
loc_id='*'
ch_id='*'

ListSta=['B209','B210','B213','B214','B215','BRK9']
client = Client(user=arc_user, host=arc_host, port=arc_port)

for Sta in ListSta:
    fsgram = client.get_waveforms('BR', Sta, loc_id, ch_id, t_start, t_end, route=False)
    fsgram.write(f'msd/{Sta}.msd',format='MSEED')
    print(f'{Sta} was downloaded')

