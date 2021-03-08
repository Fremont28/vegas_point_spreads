#This script gives the differences in point spreads between Las Vegas’ 
# VI Consensus and online sportsbooks William Hill, BetMGM, WynnBET, 
# SportsBetting.com, FanDuel, DraftKings, and Circa Sports. 

#import libraries 
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
import matplotlib

#import vi consensus spread (csv file)
sp=pd.read_csv("bball_hoy.csv",encoding="latin-1") #spreada1.csv, spread_bets1.csv 
sp.rename(columns={'3/6/21 12:00': 'team'}, inplace=True)

#teams 
tm=sp['team'] 
tm=pd.DataFrame(tm)

#check if the point spread is an even decimal (i.e. 5.0) or non-decimmal (i.e. 4.5)
check_half=sp['Unnamed: 2'].str.contains('_Ê')
check_half=pd.DataFrame(check_half)
check_half.columns=['check_half']

check_half1=sp['Unnamed: 2'].str.contains('_u')
check_half1=pd.DataFrame(check_half1)
check_half1.columns=['check_half1']

#split into 1/2 and non-1/2 
#split split into 1/2 and non-1/2 for spread (and then sort by number to get the correct ordring of teams)
sp=pd.concat([sp,check_half,check_half1],axis=1)
sp=sp.dropna(thresh=5) 

#1/2 spread 
sp1=sp[(sp.check_half==True) | (sp.check_half==True)]
t1=sp1['Unnamed: 2'].str.extract('(\d+)')
t1.columns=['vi1']
t1['vi1']=t1['vi1'].astype(float)
t1['vi1']=t1['vi1']+0.5

#subset on the game spread 
t1_sp=t1[t1.vi1<50]
t1_sp=tm.join(t1_sp, how='outer')

#even spread 
sp2=sp[(sp.check_half==False) & (sp.check_half==False)]
t2=sp2['Unnamed: 2'].str.extract('(\d+)')
t2.columns=['vi2']
t2['vi2']=t2['vi2'].astype(int)

#subset on the game spread 
t2_sp=t2[t2.vi2<50]
t2_sp=tm.join(t2_sp, how='outer')

#merge on the index for the game spreads 
spreads=pd.merge(t1_sp,t2_sp,on="team")
spreads.columns=['team','v1_sp','v2_sp']
spreads['team']=spreads['team'].astype(str)
spreads=spreads[~spreads['team'].str.contains(':')]
spreads=spreads[~spreads['team'].str.contains('nan')]

spreads=spreads.dropna(thresh=2)
spreads.v1_sp.fillna(spreads.v2_sp, inplace=True)
del(spreads['v2_sp'])
spreads.columns=['team','vi_sp']


#calculate the point spreads for online sportsbooks
bet_source='Unnamed: 4' #input the name of the online sportsbook (i.e. BetMGM, FanDuel)
source_name='Bet MGM'
check_half_fd=sp[bet_source].str.contains('_Ê')
check_half_fd=pd.DataFrame(check_half_fd)
check_half_fd.columns=['check_half_fd']

check_half_fd1=sp[bet_source].str.contains('_u')
check_half_fd1=pd.DataFrame(check_half_fd1)
check_half_fd1.columns=['check_half_fd1']

sp=pd.concat([sp,check_half_fd,check_half_fd1],axis=1)
sp=sp.dropna(thresh=5) 

sp1_fd=sp[(sp.check_half_fd==True) | (sp.check_half_fd1==True)]
t1_fd=sp1_fd[bet_source].str.extract('(\d+)')
t1_fd.columns=['fd1']
t1_fd['fd1']=t1_fd['fd1'].astype(float)
t1_fd['fd1']=t1_fd['fd1']+0.5

#subset on the game spread 
t1_fd=t1_fd[t1_fd.fd1<50]
t1_fd=tm.join(t1_fd, how='outer')
t1_fd=t1_fd.dropna()
t1_fd.columns=['team','fd_sp']

#no-half 
sp2_fd=sp[(sp.check_half_fd==False) & (sp.check_half_fd1==False)]
t2_fd=sp2_fd[bet_source].str.extract('(\d+)')
t2_fd.columns=['fd2']
t2_fd['fd2']=t2_fd['fd2'].astype(int)

#subset on the game spread 
t2_fd=t2_fd[t2_fd.fd2<50]
t2_fd=tm.join(t2_fd,how="outer")
t2_fd=t2_fd.dropna()
t2_fd.columns=['team','fd_sp']

#combine t1_fd and t2_fd
fd=pd.concat([t1_fd,t2_fd],axis=0)
fd_fin=pd.merge(spreads,fd,on="team")
fd_fin['diff']=fd_fin.vi_sp-fd_fin.fd_sp

#bet on favorites (fan duel)
fav_fd=fd_fin[fd_fin['diff']>0]
print(fav_fd) 

#bet on unders (fan duel)
under_fd=fd_fin[fd_fin['diff']<0]
print(under_fd)

under_fd, fav_fd 

#i. favorite spread (vi vs. sportsbook)
fav_fd1=fav_fd 
fav_fd1.columns=['Favored Team','VI Spread',source_name + ' Spread','Diff']

f1= go.Figure(data=[go.Table(
    header=dict(values=list(fav_fd1.columns),
                fill_color='plum',
                align='left'),
    cells=dict(values=[fav_fd1['Favored Team'],fav_fd1['VI Spread'],fav_fd1[source_name + ' Spread'],fav_fd1['Diff']],
               fill_color='white',
               align='left')) ])

f1.update_layout(
    height=600,
    showlegend=False,
    title_text= "Differences In Vegas' VI Spread vs. " + source_name + " SportsBook",
)            
f1.show()

#ii. under spread (vi vs. sportsbook)
under_fd1=under_fd 
under_fd1.columns=['Favored Team','VI Spread',source_name + ' Spread','Diff']

f2x= go.Figure(data=[go.Table(
    header=dict(values=list(under_fd1.columns),
                fill_color='plum',
                align='left'),
    cells=dict(values=[under_fd1['Favored Team'],under_fd1['VI Spread'],under_fd1[source_name + ' Spread'],under_fd1['Diff']],
               fill_color='white',
               align='left')) ])

f2x.update_layout(
    height=600,
    showlegend=False,
    title_text= "Differences In Vegas' VI Spread vs. " + source_name + " SportsBook",
)            
f2x.show()
















