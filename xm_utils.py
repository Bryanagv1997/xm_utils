from pydataxm import *                          
import datetime as dt  
import pandas as pd
import matplotlib.pyplot as plt

objetoAPI = pydataxm.ReadDB()

def date_convert(date: str='01/01/2025'):
    date = dt.datetime.strptime(date, '%d/%m/%Y')
    day = date.day
    month = date.month
    year = date.year
    return [year,month,day]

def spot_daily(date_init: str = '01/01/2025',date_final: str = '31/01/2025'):
    date_init = date_convert(date_init)

    date_final = date_convert(date_final)

    df =objetoAPI.request_data(
                                    'PrecBolsNaci',
                                    'Sistema',
                                    dt.date(date_init[0],date_init[1],date_init[2]),
                                    dt.date(date_final[0],date_final[1],date_final[2]))
    return df

def spot_mean_daily(date_init: str = '01/01/2025',date_final: str = '31/01/2025'):
    
    df = spot_daily(date_init,date_final)
    df['mean']=round(df.iloc[:,2:26].mean(axis=1),2)
    return df[['Date','mean']]

def spot_mean_barplot(title='Promedio por día',date_init: str = '01/01/2025',date_final: str = '31/01/2025'):
    df = spot_mean_daily(date_init,date_final)
    custom_labels = df['Date'].dt.strftime('%d/%m')
    values = df['mean']
    plt.figure(figsize=(12, 6))
    plt.bar(custom_labels, values)
    plt.xticks(rotation=45)
    plt.title(title+' '+date_init+' a '+date_final)
    plt.xlabel('Dia')
    plt.ylabel('COP/kWh')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def spot_hourly_boxplot(title='Distribución por hora',date_init: str = '01/01/2025',date_final: str = '31/01/2025'):

    df = spot_daily(date_init,date_final)
    hour_cols = [f'Values_Hour{i:02d}' for i in range(1,25)]
    hour_cols_change = [f'H{i:02d}' for i in range(1,25)]
    missing = [col for col in hour_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")

    plt.figure(figsize=(12, 6))
    df[hour_cols].boxplot()
    plt.title(title+' '+date_init+' a '+date_final)
    plt.xlabel('Hora')
    plt.ylabel('COP/kWh')
    plt.xticks(ticks=range(1,25),labels=hour_cols_change)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
