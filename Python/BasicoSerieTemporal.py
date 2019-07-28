#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create by Fabio
"""
#------------------------------------------------------------------------------
#Import libraries
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.seasonal import seasonal_decompose



#------------------------------------------------------------------------------
#Leitura e tratamento dos dados
dados=pd.read_csv('OnlineRetail.csv')
dados['Date_transformado']=pd.to_datetime(dados['InvoiceDate']).dt.date
#Agrupando e suavizando os dados os dados
Quantidade=dados[['Date_transformado','Quantity']]
Quantidade=Quantidade.groupby(['Date_transformado']).sum()


#------------------------------------------------------------------------------
#Funcoes
def GraficoLinhas(serie, Titulo, y_label, x_label):
    plt.plot(serie)
    plt.title(Titulo)
    plt.ylabel(y_label)
    plt.xlabel(x_label)

def Componentes(serie, ylab, titulo):
    plt.figure(figsize=(16,12))
    ax=plt.subplot(3,1,1) 
    ax.set_title(titulo, fontsize=18, loc='left')
    plt.plot(serie[0])
    plt.ylabel(ylab[0])
    plt.subplot(3,1,2)
    plt.plot(serie[1])
    plt.ylabel(ylab[1])
    plt.subplot(3,1,3)
    plt.plot(serie[2])
    plt.ylabel(ylab[2])
    ax=ax








#------------------------------------------------------------------------------
#Análise gráfica
GraficoLinhas(Quantidade["Quantity"], "Série", "Valores", "Tempo")


#------------------------------------------------------------------------------
#Decomposicao da serie
Quantidade['Aumento']=Quantidade['Quantity'].diff()
GraficoLinhas(Quantidade["Aumento"], "Série", "Aumento", "Tempo")

Quantidade['Aceleracao']=Quantidade['Aumento'].diff()
GraficoLinhas(Quantidade["Aceleracao"], "Série", "Aceleracao", "Tempo")

#Plot dos 3 graficos
Componentes([Quantidade["Quantity"],
           Quantidade["Aumento"],
           Quantidade["Aceleracao"]],
           ['Serie','Aumento','Aceleracao'],
           'Analise da serie temporal')



#------------------------------------------------------------------------------
#Analise de autocorrelacao
ax=plt.figure(figsize=(16,12))
autocorrelation_plot(Quantidade["Quantity"])
plt.title('Grafico de autocorrelacao',fontsize=18, loc='left')
plt.ylabel('Autocorrelacao', fontsize=16)
plt.xlabel('Tempo')
ax=ax

ax=plt.figure(figsize=(16,12))
autocorrelation_plot(Quantidade["Aumento"][1:])
plt.title('Grafico de autocorrelacao',fontsize=18, loc='left')
plt.ylabel('Autocorrelacao', fontsize=16)
plt.xlabel('Tempo')
ax=ax

ax=plt.figure(figsize=(16,12))
autocorrelation_plot(Quantidade["Aumento"][2:])
plt.title('Grafico de autocorrelacao',fontsize=18, loc='left')
plt.ylabel('Autocorrelacao', fontsize=16)
plt.xlabel('Tempo')
ax=ax




#------------------------------------------------------------------------------
# Decomposicao da serie
resultado=seasonal_decompose([Quantidade["Quantity"]], freq=1)

tabela=({
        'Observacao':resultado.observed,
        'Tendencia':resultado.trend,
        'Sazonalidade':resultado.seasonal,
        'Ruido':resultado.resid
        })
tabela=pd.DataFrame(tabela)

Componentes([tabela['Observacao'],
           tabela['Tendencia'],
           tabela['Sazonalidade']],
          ['Observacao','Tendencia','Sazonalidade'],
          'Analise da serie temporal')

ax=resultado.plot()




#------------------------------------------------------------------------------
# Normalizacao da serie via media moveis
Quantidade["MediaMovel_7_Dias"]=Quantidade["Quantity"].rolling(7).mean()
Quantidade["MediaMovel_21_Dias"]=Quantidade["Quantity"].rolling(21).mean()

Componentes([Quantidade['Quantity'],
           Quantidade['MediaMovel_7_Dias'],
           Quantidade['MediaMovel_21_Dias']],
          ['Quantity','MediaMovel_7_Dias','MediaMovel_21_Dias'],
          'Analise da serie temporal')



