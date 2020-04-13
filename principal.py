# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: santiagobgb
# -- repositorio: https://github.com/santiagobgb/LAB_2_bgb

# -- ----------------------------------------------------------------------------------- -- #

import funciones as fn
import visualizaciones as vs                       
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as py
import plotly.io as pio
pio.renderers.default = "browser"

#%%
datos = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx')
fn.f_pip_size(param_ins='audusd')
datos = fn.f_columnas_tiempo(param_data=datos)
datos = fn.f_columnas_pips(param_data=datos)
datos = fn.f_columnas_capital_acum(param_data=datos)
datos = fn.f_columnas_log(param_data=datos)
df_1tabla = fn.f_estadisticas_ba(param_data=datos)
df_1ranking = fn.f_estadistica_ba2(param_data=datos)
diario = fn.f_profit_diario(param_archivo='archivo_tradeview_1.xlsx')

equidistante = fn.f_profit_diario_eq(param_archivo='archivo_tradeview_1.xlsx')


estadisticas_mad = fn.f_estadisticas_mad(param_data=equidistante)


    
#%%grafica del ranking abierta en browser ya que al parecer mi version de spyder no esta actualizada y no se podian ver aqui mismo
graf = fn.f_estadistica_ba2(param_data=datos)
df = pd.DataFrame(graf)


# pull is given as a fraction of the pie radius
fig = go.Figure()
labels = df['symbol']
values = df['rank']
fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.2, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])])
fig.update_layout(title = "Efectividad", font = dict(size = 20))
py.iplot(fig)



#%%grafica del down abierta en browser

grafs = diario
graf1 = pd.DataFrame(grafs)


fig2 = go.Figure()
fig2.add_trace(go.Scatter(x= graf1.index, y = graf1.profit_acum_d, name = 'profit acumulado', mode = 'lines', marker = dict(color = 'Black')))
fig2.add_trace(go.Scatter(x = graf1.index, y =  [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,5195,None,5263.96,None] , name = 'drawup',connectgaps=True , mode = 'lines', line={'dash': 'dash', 'color': 'green'}))
fig2.add_trace(go.Scatter(x = graf1.index, y = [None,None,None,None,5055.64,None,4843.7,None,None,None,None,None,None,None,None,None,None,None,None,None], name = 'drawdown', connectgaps=True, mode = 'lines', line={'dash': 'dash', 'color': 'red'}))

fig2.update_layout(title = "DrawDown y DrawUp", xaxis_title = "Time", yaxis_title = "Profit")
    
py.iplot(fig2)






















