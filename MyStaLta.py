from obspy import read
from obspy.signal.trigger import classic_sta_lta
from obspy.signal.trigger import plot_trigger
from obspy.signal.trigger import coincidence_trigger
from pprint import pprint

st = read("https://examples.obspy.org/ev0_6.a01.gse2")
st = st.select(component="Z")
tr = st[0]
tr_taper = st[0].taper(100)
f1=1
f2=10


#tr_filt=tr.copy()
#tr_filt.taper(10)
#tr_filt.filter('bandpass', freqmin=f1,freqmax=f2, corners=8, zerophase=True)

df = tr.stats.sampling_rate
cft = classic_sta_lta(tr.data, int(5 * df), int(10 * df))
#plot_trigger(tr, cft, 1.5, 0.5)

trig = coincidence_trigger("classicstalta", 1.5, 1 ,st, 1, sta=0.5, lta=10, details=True)
pprint(trig)
