# -- ------------------------------------------------------------------------------------ -- #

# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance

# -- archivo: funciones.py - datos generales para uso en el proyecto

# -- mantiene: Francisco ME

# -- repositorio: https://github.com/IFFranciscoME/LAB_2_JFME

# -- ------------------------------------------------------------------------------------ -- #

#------------------------------------------------------------FUNCIONES----------#



import pandas as pd

def f_leer_archivo(param_archivo):
    """""
    Parameters
    ----------------
    param_arhivo : str : nombre de archivo a leer

    Returns
    ---------
    df_data : pd.DataFrame: con informacion contenida en archivo leido

    Debugging
    -----------
    para_archivo = 'archivo_tradeview_1.xlsx'

    """
    #leer archivo y guardarlo en un dataframe

    df_data = pd.read_excel(param_archivo, sheet_name='Hoja1')

    #convertir en minusculas el nmbre de las columnas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]


    #asegurar que ciertas columnas son del tipo numerico

    #cambiar tupo de dato en columnas a numerico
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap',
               'taxes', 'order']

    df_data[numcols]= df_data[numcols].apply(pd.to_numeric)

    return df_data

    def f_pip_size(param_ins):

    """""
    Parameters
    ----------------
    param_arhivo : str : nombre de archivo a leer

    Returns
    ---------
    df_data : pd.DataFrame: con informacion contenida en archivo leido

    Debugging
    -----------
    para_archivo = 'archivo_tradeview_1.xlsx'

    """

    # encontrar y eliminar un guion bajo
    inst= para,_ins.replace('_', '')

    # transformar a minisculas
    inst = param_ins.lower()

    #lista de pips por instrumento
    pips_inst={'nas100usd': 10, 'usdmxn' : 10000, 'xauusd' : 10, 'gbpusd': 10000 }

    return pips_inst

#converti columna de closetime y opentime utilizando pd.to_datatime

def fn.f_columnas_datos(param_data):

    param_data['closetime'] = pd.to_datetime(param_data['closetime'])

    param_data['opentime'] = pd.to_datetime(param_data['opentime'])
#tiempo transcurrido de una operacion
    param_data['tiempo'] = [(param_data.loc[i,'closetime'] -
                            param_data.loc[i,'opentime']).delta/le9
    for i in range(0, len(param_data['closetime']))]



    return param_data
