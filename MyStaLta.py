from obspy import read
from obspy.signal.trigger import classic_sta_lta
from obspy.signal.trigger import plot_trigger
from obspy.signal.trigger import coincidence_trigger
from obspy.core.stream import Stream
from pprint import pprint
import os

flist=os.listdir('msd')
st=Stream()
f1=3
f2=30

for i in flist:
    st+=read("msd/"+i)
    st.merge(fill_value='interpolate')

for tr in st:
    tr = tr.taper(0.01)
    tr=tr.filter('bandpass', freqmin=f1,freqmax=f2, corners=8, zerophase=True)
    df = tr.stats.sampling_rate
    cft = classic_sta_lta(tr.data, int(0.5 * df), int(10 * df))

st.plot()
trig = coincidence_trigger(trigger_type="classicstalta", thr_on=4, thr_off=3.2 ,stream=st, thr_coincidence_sum=3, sta=0.5, lta=10)
#pprint(trig[0])
#plot_trigger(tr, cft, 4, 3.2)
with open('res/'+i[:4]+'_res.txt','w') as f:
    f.write('Time\tSta\n')
    for i in trig:
        print(i['time'])
        print(i['coincidence_sum'])
        print(i['stations'])
        print(i['trace_ids'])
        print('---------------------------')
        t=i["time"]
        f.write(f'{t.strftime("%Y-%m-%d %H:%M:%S.%f")}\t{i["stations"][0]}\n')

print(len(trig))

