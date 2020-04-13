# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - procesamiento de datos
# -- mantiene:santiago
# -- repositorio: https://github.com/santiagobgb/LAB_2_SBG
# -- ------------------------------------------------------------------------------------ -- #
import datetime
import pandas as pd
import numpy as np
import math as math
import visualizaciones as vs 
from datetime import datetime
from datetime import timedelta
import yfinance as yf 
import matplotlib.pyplot as plt

#%% FUNCION: leer archivo
def f_leer_archivo(param_archivo):
    """"
    Parameters
    ----------
    param_archivos : str : nombre de archivo a leer

    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido

    Debugging
    ---------
    param_archivo =  'trading_historico.xlsx'

    """
    # Leer archivo de datos y guardarlo en Data Frame
    df_data = pd.read_excel(param_archivo, sheet_name='Hoja1')

    # Convertir a minusculas el nombre de las columnas
    df_data.columns = [list(df_data.columns)[i].lower() for i in range(0, len(df_data.columns))]
    
    # Asegurar que ciertas columnas son tipo numerico
    numcols =  ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)

    return df_data

#%% FUNCION: 
def f_pip_size(param_ins):
    """"
    Parameters
    ----------
    param_ins : str : nombre de instrumento 

    Returns
    -------
    pips_inst : 

    Debugging
    ---------
    param_ins =  'trading_historico.xlsx'

    """
    
    ""
    
    # encontrar y eliminar un guion bajo
    inst = param_ins.replace('_', '')
    inst = param_ins.replace('-2', '')
    
    # transformar a minusculas
    inst = inst.lower()
    
    #lista de pips por instrumento
    pips_inst =  {'audusd' : 10000,
                  'gbpusd': 10000,
                  'xauusd': 10,
                  'eurusd': 10000,
                  'xaueur': 10,
                  'nas100usd': 10,
                  'us30usd': 10,
                  'mbtcusd':100,
                  'usdmxn': 10000,
                  'eurjpy':10000, 
                  'gbpjpy':10000,
                  'usdjpy':10000,
                  'btcusd':10,
                  'eurgbp':10000,
                  'usdcad':10000,}
    
    return pips_inst[param_ins]

#%% FUNCION:
def f_columnas_tiempo(param_data):

#convertir columna de 'closetime' y 'opentime' utilizando pd.to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])
    
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1*np.exp(9)
    for i in range(0, len(param_data['closetime']))]
    
    return param_data
    
#%% FUNCION:
def f_columnas_pips(param_data):
    param_data['pips'] = np.zeros(len(param_data['type']))
    for i in range(0,len(param_data['type'])):
        if param_data['type'][i] == 'buy':
            param_data['pips'][i] = (param_data.closeprice[i] - param_data.openprice[i])*f_pip_size(param_ins=param_data['symbol'][i])
        else:
            param_data['pips'][i] = (param_data.openprice[i] - param_data.closeprice[i])*f_pip_size(param_ins=param_data['symbol'][i])
    
    param_data['pips_acum'] = np.zeros(len(param_data['type']))
    param_data['profit_acum'] = np.zeros(len(param_data['type']))    
    param_data['pips_acum'][0] = param_data['pips'][0]
    param_data['profit_acum'][0] = param_data['profit'][0]
            
    for i in range(1,len(param_data['pips'])):
         param_data['pips_acum'][i] = param_data['pips_acum'][i-1] + param_data['pips'][i]
         param_data['profit_acum'][i] = param_data['profit_acum'][i-1] + param_data['profit'][i]
        
    return param_data
    

    
#%% FUNCION:
def f_estadisticas_ba(param_data):
    
    medida = ['Ops totales','Ganadoras','Ganadoras_c','Ganadoras_v','Perdedoras','Perdedoras_c','Perdedoras_v','Media(profit)','Media(pips)',
              'r_efectividad','r_proporcion','r_efectividad_c','r_efectividad_v']
    descripcion = ['Operaciones Totales',
                   'Operaciones Ganadoras',
                   'Operaciones Ganadoras de Compra',
                   'Operaciones perdedoras de Venta',
                   'Operaciones Perdedoras',
                   'Operaciones Perdedoras de Compra',
                   'Operaciones Perdedoras de Venta',
                   'Mediana de Profit de Operaciones', 
                   'Media de Pips de Operaciones',
                   'Ganadoras Totales / Operaciones Totales',
                   'Ganadoras Totales/Perdedoras Totales',
                   'Ganadoras Compras / Operaciones Totales',
                   'Ganadoras Ventas / Operaciones Totales']
   
    #crear uno nuevo lleno de ceros
    zero_data = np.zeros(shape=(len(descripcion),3))
    df_1_tabla = pd.DataFrame(zero_data, columns = ['medida', 'valor', 'descripcion'])
    #resolver las descripciones dadas 
    df_1_tabla['valor'][0] = len(param_data['profit'])
    df_1_tabla['valor'][1] = param_data['profit'].gt(0).sum()
    x = 0
    for i in range(0,len(param_data['type'])): 
        if param_data['type'][i] == 'buy' and param_data['profit'][i] > 0 :
            x = x+1
    df_1_tabla['valor'][2] = x
    
    x = 0
    for i in range(0,len(param_data['type'])): 
        if param_data['type'][i] == 'sell' and param_data['profit'][i] > 0 :
            x = x+1
    df_1_tabla['valor'][3] = x
    df_1_tabla['valor'][4] = df_1_tabla['valor'][0] - df_1_tabla['valor'][1]
    x = 0
    for i in range(0,len(param_data['type'])): 
        if param_data['type'][i] == 'buy' and param_data['profit'][i] < 0 :
            x = x+1
    df_1_tabla['valor'][5] = x
    
    x = 0
    for i in range(0,len(param_data['type'])): 
        if param_data['type'][i] == 'sell' and param_data['profit'][i] < 0 :
            x = x+1
    df_1_tabla['valor'][6] = x
    df_1_tabla['valor'][7] = param_data.profit.median()
    df_1_tabla['valor'][8] = param_data.pips.median()
    df_1_tabla['valor'][9] = df_1_tabla['valor'][1] / df_1_tabla['valor'][0]
    df_1_tabla['valor'][10] = df_1_tabla['valor'][1] / df_1_tabla['valor'][4]
    df_1_tabla['valor'][11] = df_1_tabla['valor'][2] / df_1_tabla['valor'][0] 
    df_1_tabla['valor'][12] = df_1_tabla['valor'][3] / df_1_tabla['valor'][0] 
    
    for i in range(0,len(medida)):
        df_1_tabla['medida'][i] = medida[i]
        df_1_tabla['descripcion'][i] = descripcion[i]
        
    return df_1_tabla

#%%def f_estadisticas_ba2(param_data):
    


def f_estadistica_ba2(param_data):

    #crear un arreglo con los symbolos que se uilizaran para el ranking
    symbol = ['xauusd',
              'eurusd',
              'xaueur',
              'bcousd',
              'cornusd',
              'mbtcusd',
              'wticousd',
              'spx500usd',
              'audusd', 
              'gbpusd',
              'xaueur', 
              'nas100usd',
              'usdmxn',
              'eurjpy',
              'gbpjpy', 
              'usdjpy',
              'btcusd',
              'eurgbp', 
              'usdcad']
    
    columns = {'symbol':np.zeros(len(symbol)),
                   'rank':np.zeros(len(symbol))}
    
    df_1_ranking = pd.DataFrame(columns)
    
    #
    for i in range(len(df_1_ranking)):
        f0 = param_data['symbol']==symbol[i]
        f1 = param_data[f0]
        if f1.empty == False:
            f1 = param_data[f0]
            f2 = param_data[(param_data['symbol']==symbol[i]) & (param_data['profit']>=0)]            
            df_1_ranking['rank'][i]=round(len(f2)/len(f1),4)*100
            df_1_ranking['symbol'][i]=symbol[i]
        else:
            df_1_ranking['rank'][i]="nan"
        pass
   
    df_1_ranking =df_1_ranking.sort_values(by=['rank'],ascending=[False])
    
    df_1_ranking =df_1_ranking.dropna()
 
    


    return df_1_ranking





        
#%% funcio de capital acumulado empezando com capital de 5000

def f_columnas_capital_acum(param_data):
                                
    param_data['capital_acum'] = np.zeros(shape=(len(param_data['profit']),1))
    
    
    initial_investment = 5000
    for i, r in enumerate(param_data['profit']):
        param_data['capital_acum'][i] = initial_investment + r
        initial_investment = initial_investment + r

    



   

    return param_data  




#%%crear una columna con los rendimientos logaritmicos
def f_columnas_log(param_data):
    
    param_data['rendimiento_log'] = np.zeros(len(param_data['type']))
    param_data['rendimiento_log'][0] = math.log(param_data['capital_acum'][0] / 5000)
    
      
    for i in range(1,len(param_data['pips'])):
         param_data['rendimiento_log'][i] = math.log(param_data['capital_acum'][i] / param_data['capital_acum'][i-1])
    
    return param_data


#%%
    

def f_profit_diario(param_archivo):
    #tuve que volver  descargar el excel por problemas de fechas, lo senti mas facil haciendolo desde cero
    d = pd.read_excel(param_archivo, sheet_name='Hoja1')

     
    
#aplicamos to_datetime
    d['closeTime'] = pd.to_datetime(d['closeTime'].copy()).dt.date
#creamos el dataframe con las columnas
    trades = pd.DataFrame(columns=['timestamp', 'profit_d', 'profit_acum_d'])
#timesstamp lo hice de los closetime, ya que habia intentado con opentime peor no daba el profit diario realmente
    trades['timestamp'] = d['closeTime']
    trades['profit_d'] = d['Profit']
    trades['profit_acum_d'] = np.zeros(shape=(len(trades),1))
    #sumas los close time que sean iguales  ... para que sea diario, termina siendo timestamp el index
    trades = trades.groupby(['timestamp']).sum()
#creas el profit acumulado diario
    initial_investment = 5000
    for i, r in enumerate(trades['profit_d']):
        trades['profit_acum_d'][i] = initial_investment + r
        initial_investment = initial_investment + r

    return trades
     

    


#%%para sacar sortinos y sharps equidistantes
    

def f_profit_diario_eq(param_archivo):
    #tuve que volver  descargar el excel por problemas de fechas, lo senti mas facil haciendolo desde cero
    d = pd.read_excel(param_archivo, sheet_name='Hoja1')

     
    
#aplicamos to_datetime
    d['closeTime'] = pd.to_datetime(d['closeTime'].copy()).dt.date
    
#creamos el dataframe con las columnas
    trades = pd.DataFrame(columns=['timestamp', 'profit_d', 'profit_acum_d',
                                   'profit_d_c', 'profit_d_v',
                                   'profit_acum_d_v','profit_acum_d_c',
                                   'rendimiento_log'])
#timesstamp lo hice de los closetime, ya que habia intentado con opentime peor no daba el profit diario realmente
    trades['timestamp'] = d['closeTime']
    trades['profit_d'] = d['Profit']
    trades['profit_acum_d'] = np.zeros(shape=(len(trades),1))
    trades['rendimiento_log'] = np.zeros(shape=(len(trades),1))
    trades['profit_acum_d_c'] = np.zeros(shape=(len(trades),1))
    trades['profit_acum_d_v'] = np.zeros(shape=(len(trades),1))
    trades['profit_d_c'] = np.zeros(shape=(len(trades),1))
    trades['profit_d_v'] = np.zeros(shape=(len(trades),1))
    #compra
    for i in range(0,len(d['Type'])): 
        if d['Type'][i] == 'buy' :
            trades['profit_d_c'][i] = d['Profit'][i]
        else:
            trades['profit_d_c'][i] = 0
            
         
    trades['profit_acum_d_c'] = np.zeros(shape=(len(trades),1))
    #venta
    
    for i in range(0,len(d['Type'])): 
        if d['Type'][i] == 'sell' :
            trades['profit_d_v'][i] = d['Profit'][i]
        else:
            trades['profit_d_v'][i] = 0
         
    
    
    
    #juntos por timestamp
    trades = trades.groupby(['timestamp']).sum()
    
    initial_investment = 5000
    ##compr
    for i, r in enumerate(trades['profit_d_c']):
        trades['profit_acum_d_c'][i] = initial_investment + r
        initial_investment = initial_investment + r
    
    ##venta
    initial_investment = 5000
    for i, r in enumerate(trades['profit_d_v']):
        trades['profit_acum_d_v'][i] = initial_investment + r
        initial_investment = initial_investment + r
    
    ##acum
    initial_investment = 5000
    for i, r in enumerate(trades['profit_d']):
        trades['profit_acum_d'][i] = initial_investment + r
        initial_investment = initial_investment + r
    

    
###############
    for i in range(0,len(trades['profit_d'])):
         trades['rendimiento_log'][i] = math.log(trades['profit_acum_d'][i] / trades['profit_acum_d'][i-1])
    
    
 
    return trades
    
    
    
    
     

    

#%%    
def f_estadisticas_mad(param_data):
    
    #termine descargando los rendimientos del etef "MSFT"=Microsoft
    #NASDAQ:  ya que no pude poner la funcion de oanda  que nos dio el profe
    msft = yf.Ticker("MSFT")
    x = pd.DataFrame(msft.dividends)
    x = x.iloc[20,:]
    rf = .08
    m = 0.3/300
    
    medidas = ['sharpe','sortino_c','sortino_v', 'drawdown_capi','drawdown_capi',
               'information_r']
    descripcion = ['Sharpe Ratio', 'Sortino Ratio para Posiciones de Compra','Sortino Ratio para Posiciones de Venta', 'DrawDown de Capital',
                   'DrawUp de Capital','Information Ratio']
                              
                              
      
   
    zero_data = np.zeros(shape=(len(descripcion),3))
    df_estadisticas_mad = pd.DataFrame(zero_data, columns = ['medidas', 
                                                             'valor', 
                                                             'descripcion'])
    for i in range(0,len(medidas)):
        df_estadisticas_mad['medidas'][i] = medidas[i]
        df_estadisticas_mad['descripcion'][i] = descripcion[i]

    #medidas 0 sharp
    salida = np.log(param_data.profit_acum_d / param_data.profit_acum_d.shift()).dropna()
    sum_salid = np.sum(salida)
    std_salid = salida.std()
    df_estadisticas_mad.valor[0] = (sum_salid - rf) / std_salid
    
 
    
    
# medidas 1,2 sortino

    salida2 = np.log(param_data.profit_acum_d_c[1:].values / param_data.profit_acum_d_c[:-1].values)

    de = salida2 - m
    de[de > 0] = 0

    df_estadisticas_mad.valor[1] = (salida2.mean() - m) / (((de*2).mean())*0.5)
    

    # Sortino venta
 

    salida3 = np.log(param_data.profit_acum_d_v[1:].values / param_data.profit_acum_d_v[:-1].values)
    
    de2 = salida3 - m
    de2[de2 > 0] = 0
    
    df_estadisticas_mad.valor[2] = (salida3.mean() - m) / ((de*2).mean())*0.5
    
    

    

   # medidas 3 drawdown_capi_c
    df_estadisticas_mad.valor[3] =  param_data.profit_acum_d.min()

    # medidas 4 drawup_capi_v
    df_estadisticas_mad.valor[4] =  param_data.profit_acum_d.max()







    


    # information_r
    

      
  
    profit_prom = param_data.rendimiento_log.mean()
   
    # Promedio de rendimientos del Microsoft NASDAQ: MSFT
    bench_prom = x.mean()
    
    num_ir = profit_prom - bench_prom

    # Denominador Information Ratio
    # Diferencia por rows de los rendimientos del profit_acm_d y del Microsoft NASDAQ: MSFT
    #dif_denom = param_data['profit_acum_d'].mean() - x.mean()
 
    
    #dif_denom = param_data.rendimiento_log - x
    #denom_ir = dif_denom.std()
    

    df_estadisticas_mad.valor[5] = num_ir#/denom_ir
    
    
    
    
    
    
    
    return df_estadisticas_mad

    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
