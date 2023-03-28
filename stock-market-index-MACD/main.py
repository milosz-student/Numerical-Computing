import pandas as pd
import matplotlib.pyplot as ptl

dane = pd.read_csv('gold_18_21.csv')
daty = pd.to_datetime(dane['Data'])
ceny = dane['Zamkniecie']
days =[]

for i in range(len(daty)):
    days.append(i)

def alfa(x):
        return 2/(x+1)

def EMA(nr,N,source):
        numerator= 0 #licznik p0 + (1 − α)p1 + (1 − α)2p2 + · · · + (1 − α) N pN
        denominator = 0 #mianownik 1 + (1 − α) + (1 − α) 2 + · · · + (1 − α)N
        if(nr<N):
            x=nr + 1
        else:
            x = N+1
        for i in range(x):
            temp = pow((1 - alfa(N)), i)
            denominator += temp
            numerator += temp * source[nr - i]

        return numerator/denominator

MACD =[]
for i in range(len(ceny)):
    MACD.append(EMA(i,12,ceny)-EMA(i,26,ceny))

SIGNAL = []
for i in range(len(MACD)):
    SIGNAL.append(EMA(i,9,MACD))


#bot do kupowania
BUYx =[]
BUYp =[]
SELLx =[]
SELLp =[]
akcje = 1000
przykladowy = akcje*ceny[26]
print("kapital na poczatku: ",przykladowy)
pieniadze = 0
signal_is_higher = False
macd_is_higher = False
for i in range(26,len(MACD)):
    if SIGNAL[i]>MACD[i] and signal_is_higher == False:
        signal_is_higher= True
        macd_is_higher = False
        if akcje:
            pieniadze+=akcje*ceny[i]
            akcje=0
            SELLx.append(i)
            SELLp.append(ceny[i])

    elif MACD[i]>SIGNAL[i] and macd_is_higher == False:
        macd_is_higher= True
        signal_is_higher = False
        if pieniadze:
            ilosc_akcji = int(pieniadze/ceny[i])
            akcje+=ilosc_akcji
            BUYx.append(i)
            BUYp.append(ceny[i])
            pieniadze=0


pieniadze += akcje*ceny[1000]
print("kapital na koniec: ",pieniadze)
print("przychod/strata: ",str(round((pieniadze-przykladowy)/przykladowy*100, 2)),'%')

#rysowanie wykresow
#wykres gorny
ptl.style.use('seaborn')
fig, (ax1,ax2) = ptl.subplots(nrows=2,ncols=1)
ax1.plot(days,MACD,linestyle='solid',color='blue',label='MACD')
ax1.plot(days,SIGNAL,linestyle='solid',color='red',label='SIGNAL')
ax1.legend()
ax1.set_title("Wykres MACD I SIGNAL")
ax1.set_xlabel("nr dnia")
ax1.set_ylabel("wartosc")
#wykres dolny
ax2.scatter(BUYx,BUYp,20,color = 'green',label='BUY')
ax2.scatter(SELLx,SELLp,20,color = 'red',label='SELL',alpha = 1.0)
ax2.plot(days,ceny,linestyle='solid',color = 'gray',label='CENA')
ax2.set_title("Cena zamkniecia")
ax2.set_xlabel("nr dnia")
ax2.set_ylabel("wartosc akcji przy zamknieciu")
ax2.legend()

#wyswietlanie wykresow
ptl.tight_layout()
ptl.show()
