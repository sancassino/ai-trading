"""COT-studie (D-103 vervolg, trial 5-6): positionering (CFTC, publiek) -> volgende-week rendement.
Hypotheses VOORAF: H1 contrarian bij extreme netto-positie van speculanten (z over 156 weken >=+1.5 short, <=-1.5 long);
H2 trend op 4-weeks-verandering (z>=+1.5 long, <=-1.5 short). Instap vrijdag-close (publicatiemoment), uit volgende vrijdag-close. Data 2010-2024 (reserve dicht)."""
import pandas as pd, numpy as np, glob, warnings; warnings.filterwarnings('ignore')
def load(kind):
    fs=sorted(glob.glob(f'/tmp/cot/x_{kind}_txt_20*/*'))
    return pd.concat([pd.read_csv(f,low_memory=False) for f in fs])
tff=load('fut_fin'); dis=load('com_disagg')
def series(df,name_start,long_col,short_col,exact=None):
    m=df[df.Market_and_Exchange_Names.str.startswith(name_start)].copy()
    m['d']=pd.to_datetime(m['Report_Date_as_YYYY-MM-DD'])
    m=m.sort_values('d').drop_duplicates('d')
    net=(m[long_col]-m[short_col])/m['Open_Interest_All']
    return pd.Series(net.values,index=m['d'].values)
SPEC=[ # (naam, df, marktprefix, long, short, proxybestand, teken, ftmo-symbool)
 ('US500',tff,'E-MINI S&P 500 - CHICAGO','Lev_Money_Positions_Long_All','Lev_Money_Positions_Short_All','SPX_TR',1,'US500.cash'),
 ('US100',tff,'NASDAQ MINI - CHICAGO','Lev_Money_Positions_Long_All','Lev_Money_Positions_Short_All','NDX',1,'US100.cash'),
 ('EURUSD',tff,'EURO FX - CHICAGO','Lev_Money_Positions_Long_All','Lev_Money_Positions_Short_All','FX_EURUSD',1,'EURUSD'),
 ('GBPUSD',tff,'BRITISH POUND - CHICAGO','Lev_Money_Positions_Long_All','Lev_Money_Positions_Short_All','FX_GBPUSD',1,'GBPUSD'),
 ('AUDUSD',tff,'AUSTRALIAN DOLLAR - CHICAGO','Lev_Money_Positions_Long_All','Lev_Money_Positions_Short_All','FX_AUDUSD',1,'AUDUSD'),
 ('USDJPY',tff,'JAPANESE YEN - CHICAGO','Lev_Money_Positions_Long_All','Lev_Money_Positions_Short_All','FX_USDJPY',-1,'USDJPY'),
 ('USDCAD',tff,'CANADIAN DOLLAR - CHICAGO','Lev_Money_Positions_Long_All','Lev_Money_Positions_Short_All','FX_USDCAD',-1,'USDCAD'),
 ('USDCHF',tff,'SWISS FRANC - CHICAGO','Lev_Money_Positions_Long_All','Lev_Money_Positions_Short_All','FX_USDCHF',-1,'USDCHF'),
 ('XAUUSD',dis,'GOLD - COMMODITY EXCHANGE','M_Money_Positions_Long_All','M_Money_Positions_Short_All','GOLD_F',1,'XAUUSD'),
 ('XAGUSD',dis,'SILVER - COMMODITY EXCHANGE','M_Money_Positions_Long_All','M_Money_Positions_Short_All','SILVER_F',1,'XAGUSD'),
 ('USOIL',dis,'CRUDE OIL, LIGHT SWEET - NEW YORK','M_Money_Positions_Long_All','M_Money_Positions_Short_All','WTI_F',1,'USOIL.cash'),
 ('NATGAS',dis,'NAT GAS NYME','M_Money_Positions_Long_All','M_Money_Positions_Short_All','NATGAS_F',1,'NATGAS.cash'),
]
cs=pd.read_csv('/tmp/costs.csv',sep=';',comment='#',usecols=range(9),engine='python',on_bad_lines='skip').set_index('symbol')
sw=pd.read_csv('results/ceo/swap_side_map.csv',sep=';').set_index('symbol')
def cost(s,side):
    rt=float(cs.at[s,'rondreis_bp']) if s in cs.index else 3.0
    n=s if s in sw.index else s.replace('.cash','cash')
    if n not in sw.index: return rt
    pct=sw.at[n,'long_pct_yr'] if side>0 else sw.at[n,'short_pct_yr']
    return rt+max(0.0,-float(pct))*100*7/365
rows=[]
for nm,df,pre,lc,sc,prox,sg,fs in SPEC:
    net=series(df,pre,lc,sc)
    if len(net)<200: print('te weinig data',nm,len(net)); continue
    net=net*sg
    z=(net-net.rolling(156,min_periods=100).mean())/net.rolling(156,min_periods=100).std()
    dz=net.diff(4); dzz=(dz-dz.rolling(156,min_periods=100).mean())/dz.rolling(156,min_periods=100).std()
    px=pd.read_csv(f'/tmp/daily/{prox}.csv',sep=';',comment='#',parse_dates=['date']).set_index('date')['close'].dropna()
    px=px[~px.index.duplicated()]
    for d in z.index:
        fri=pd.Timestamp(d)+pd.Timedelta(days=3); nxt=fri+pd.Timedelta(days=7)
        if fri<pd.Timestamp('2010-06-01') or nxt>=pd.Timestamp('2025-01-01'): continue
        a=px.asof(fri); b=px.asof(nxt)
        if np.isnan(a) or np.isnan(b): continue
        rows.append(dict(m=nm,fri=fri,z=z[d],dz=dzz[d],ret=(b/a-1)*1e4,fs=fs))
R=pd.DataFrame(rows).dropna(); R['yr']=R.fri.dt.year
print('weken x markten:',len(R), 'markten:',R.m.nunique(), 'periode',R.fri.min().date(),R.fri.max().date())
def rep(name,sel,side):
    S=R[sel].copy(); S['gross']=side[sel]*S.ret; S['net']=S.gross-S.apply(lambda r:cost(r.fs,int(np.sign(side[sel][r.name]))) ,axis=1)
    w=S.groupby('fri').net.mean(); wg=S.groupby('fri').gross.mean()
    t=lambda x:x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))
    print(f'{name:34s} N={len(S):5d} bruto={S.gross.mean():+6.2f}bp (t_week {t(wg):+.2f}) netto={S.net.mean():+6.2f}bp (t_week {t(w):+.2f})')
    return S
s1=-np.sign(R.z); e1=R.z.abs()>=1.5
S1=rep('H1 contrarian |z|>=1.5',e1,s1)
s2=np.sign(R.dz); e2=R.dz.abs()>=1.5
S2=rep('H2 trend op 4w-verandering',e2,s2)
e1b=R.z.abs()>=2.0; rep('H1 contrarian |z|>=2.0 (gevoeligheid)',e1b,s1)
print('\nper markt (bruto, t_week-onafh. t over trades) H1:')
for m,g in S1.groupby('m'): print(f'  {m:7s} N={len(g):4d} bruto={g.gross.mean():+6.2f} netto={g.net.mean():+6.2f} t={g.gross.mean()/(g.gross.std(ddof=1)/np.sqrt(len(g))):+.2f}')
print('per jaar H1:'); 
for y,g in S1.groupby('yr'): print(' ',y,f'N={len(g)} bruto={g.gross.mean():+6.2f} netto={g.net.mean():+6.2f}')
print('\ncorr(z, volgende-week-rendement/vol) per markt (eenvoudige check):')
R['rn']=R.groupby('m').ret.transform(lambda x:x/x.std())
print(R.groupby('m').apply(lambda g:np.corrcoef(g.z,g.rn)[0,1]).round(3).to_dict())
