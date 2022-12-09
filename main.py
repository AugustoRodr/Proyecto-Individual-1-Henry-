from fastapi import FastAPI, Path, UploadFile, File
import pandas as pd
import numpy as np
from modulos import *

# IMPORTANTE EL ORDEN DE DECLARACION
df_completo=etl_eda() # 1
carga_dicc_actores(df_completo) # 2
df_actores, df_tipo_film, df_count_plat, df_categorias=crear_tablas(df_completo)# 3


app= FastAPI()

# query 1
@app.get('/get_max_duration/')
async def get_max_duration(anio:int,plataforma:str,tipo:str):

   resultado=funcion_query1(anio, plataforma, tipo, df_tipo_film)

   return 'Titulo: {} | Año: {} | Minutos: {} | Seasons: {} | Plataforma: {}'.format(resultado['title'].iloc[0],resultado['anio'].iloc[0],\
    resultado['duration(min)'].iloc[0],resultado['duration(Season)'].iloc[0],resultado['Plataforma'].iloc[0])

# query 2
@app.get('/get_count_plataform/')
async def get_count_plataform(plataforma: str):

   resultado=funcion_query2(plataforma, df_count_plat)
   return f"Plataforma: {resultado['Plataforma'].iloc[0]} | TV Show: {resultado['TV Show'].iloc[0]} | Movie: {resultado['Movie'].iloc[0]}"

# query 3
@app.get('/get_listedin/')
async def  get_listedin(categoria: str):

   resultado=funcion_query3(categoria, df_categorias) 
   return f"Plataforma: {resultado['Plataforma'].iloc[0]} | Categoria: {resultado['Categoria'].iloc[0]} | Cantidad: {resultado['Cantidad'].iloc[0]}"
    

# query 4
@app.get('/get_actor/')
async def get_actor(plataforma: str, anio: int):

   resultado=funcion_query4(plataforma,anio,df_actores)
   return f"Plataforma: {resultado['Plataforma'].iloc[0]} | Anio: {resultado['Anio'].iloc[0]} | Nombre: {resultado['Nombre'].iloc[0]} | Cantidad: {resultado['Cantidad'].iloc[0]}"




