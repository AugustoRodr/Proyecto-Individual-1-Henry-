import pandas as pd
import numpy as np

dicc_actor_distin= {
    'Amazon':{},
    'Disney':{},
    'Hulu':{},
    'Netflix':{}
}

dicc_listedin_distin={
    'Netflix':{},
    'Amazon':{},
    'Disney':{},
    'Hulu':{}
}


plataformas=['Amazon','Disney','Hulu','Netflix']


def ingesta():
    path='./Datasets/amazon_prime_titles.csv'
    path_2='./Datasets/disney_plus_titles.csv'
    path_3='./Datasets/hulu_titles.csv'
    path_4='./Datasets/netflix_titles.json'
    df_amazon= pd.read_csv(path).copy()
    df_disney= pd.read_csv(path_2).copy()
    df_hulu= pd.read_csv(path_3).copy()
    df_netflix= pd.read_json(path_4).copy()

    return df_amazon,df_disney,df_hulu,df_netflix


def etl_eda():
    df_amazon,df_disney,df_hulu,df_netflix=ingesta()
    #Agrego la columna plataforma para mas adelante
    df_amazon['Plataforma'],df_disney['Plataforma'],df_hulu['Plataforma'],df_netflix['Plataforma']='Amazon','Disney','Hulu','Netflix'

    # Concateno las 4 tablas
    data_total=pd.concat([df_amazon,df_disney,df_hulu,df_netflix], ignore_index=True)

    # limpio y nosmalizo los NaN
    data_total.replace({np.nan:'Sin Informacion'}, inplace=True)
    data_total.replace({'nan':'Sin Informacion'}, inplace=True)
    data_total['duration'].replace({'Sin Informacion':'0 min'}, inplace=True) #solo en la columna de duration los cambio por 0 min 

    # creacion de 2 columnas a partir de las unidades distintas de la columna 'duration'
    data_total['duration(Season)']= data_total['duration'].apply( lambda row: row.split()[0] if (row.split()[1]=='Season' or row.split()[1]=='Seasons') else '0')
    data_total['duration(min)']= data_total['duration'].apply( lambda row: row.split()[0] if row.split()[1]=='min' else '0')

    # cambio los tipos de datos a int ya que estos solo contienen datos numericos no decimales
    data_total['duration(Season)']=data_total['duration(Season)'].astype(int)
    data_total['duration(min)']=data_total['duration(min)'].astype(int)

    # una vez que reviso que esten correctas las columnas creadas dropeo la columna original
    data_total.drop(columns='duration', inplace=True)

    return data_total

# Funcion que carga las fechas de cada plataforma al diccionario
def carga_dicc_fechas(df):
    for plat in plataformas:
        df_temp=df[df['Plataforma']==plat]
        fechas=sorted(list(df_temp['release_year'].unique()))
        for fecha in fechas:
            if fecha in dicc_actor_distin[plat]:
                pass
            else:
                dicc_actor_distin[plat][fecha]={}

# funcion: carga y conteo de actores para cada plataforma segun fecha por separado
def carga_dicc_actores(df):
    carga_dicc_fechas(df)

    for plat in plataformas:
        df_temp=df[df['Plataforma']==plat]
        fechas_x_plat=sorted(list(df_temp['release_year'].unique()))
        for fecha in fechas_x_plat:
            df_temp_2= df_temp[df_temp['release_year']==fecha]    
            for i in df_temp_2['cast']:
                if i != 'Sin Informacion':
                    actores= i.split(',')
                    for actor in actores:
                        actor=actor.replace('\"','').replace('\'','').replace('St.','').replace('Sr.','').replace('Jr.','')\
                            .strip().title()
                        if actor in dicc_actor_distin[plat][fecha]:
                            dicc_actor_distin[plat][fecha][actor]+=1
                        else:
                            dicc_actor_distin[plat][fecha][actor]=1


# funcion: carga y conte de las distintas categorias
def carga_dicc_listedin(df):

    for plat in dicc_listedin_distin:
        temp_df=df[df['Plataforma']==plat]
        for row in temp_df['listed_in']:
            if row != 'Sin Informacion':
                categorias=row.split(',')
                for categoria in categorias:
                    categoria=categoria.replace('\"','').replace('\'','').strip()
                    if categoria in dicc_listedin_distin[plat]:
                        dicc_listedin_distin[plat][categoria]+=1
                    else:
                        dicc_listedin_distin[plat][categoria]=1


def crear_tablas(df):
    #otra forma de crear la tabla
    #tabla para la query 1
    tabla_tipo_film=pd.DataFrame()
    tabla_tipo_film['title']=list(df['title'])
    tabla_tipo_film['anio']=list(df['release_year'])
    tabla_tipo_film['duration(min)']=list(df['duration(min)'])
    tabla_tipo_film['duration(Season)']=list(df['duration(Season)'])
    tabla_tipo_film['Plataforma']=list(df['Plataforma'])

    #tabla para la query 2
    tabla_count_plat=[]
    for i in plataformas:
        df_temp=df[df['Plataforma']==i]
        tabla_count_plat.append([i,(df_temp['type']=='TV Show').sum(),(df_temp['type']=='Movie').sum()])

    tabla_count_plat= pd.DataFrame(tabla_count_plat, columns=['Plataforma','TV Show','Movie'])

    #tabla para la query 3
    carga_dicc_listedin(df)

    tabla_categorias=[]
    for plat in dicc_listedin_distin:
        for cat in dicc_listedin_distin[plat]:
            tabla_categorias.append([plat,cat,dicc_listedin_distin[plat][cat]])

    tabla_categorias=pd.DataFrame(tabla_categorias, columns=['Plataforma','Categoria','Cantidad'])

    #tabla para la query 4
    tabla_actores=[]
    
    for plat in dicc_actor_distin:
        for fecha in dicc_actor_distin[plat]:
            for actor in dicc_actor_distin[plat][fecha]:
                tabla_actores.append([plat,fecha,actor,dicc_actor_distin[plat][fecha][actor]])
    
    tabla_actores=pd.DataFrame(tabla_actores, columns=['Plataforma','Anio','Nombre','Cantidad'])


    return tabla_actores,tabla_tipo_film,tabla_count_plat,tabla_categorias



# funcion de la query 1
def funcion_query1(año, plataforma, tipo ,df):#(min/Seasons)
    plataforma=plataforma.strip().title()

    if tipo=='min':
        df_query_1=df[((df['Plataforma']==plataforma) & (df['anio']==año))]
        df_query_1=df_query_1[df_query_1['duration(min)']==max(df_query_1['duration(min)'])]
        return df_query_1
    else:
        df_query_1=df[((df['Plataforma']==plataforma) & (df['anio']==año))]
        df_query_1=df_query_1[df_query_1['duration(Season)']==max(df_query_1['duration(Season)'])]
        return df_query_1


# funcion de la query 2
def funcion_query2(plataforma,df):
    plataforma=plataforma.strip().title()
    return df[df['Plataforma']==plataforma]

# funcion de la query 3
def funcion_query3(cat,df):
    cat=cat.strip().title()
    sub_df=df[df['Categoria']==cat]
    return sub_df[sub_df['Cantidad']==max(sub_df['Cantidad'])]

# funcion de la query 4
def funcion_query4(plat, anio,df):
    plat=plat.strip().title()
    df_query=df[((df['Plataforma']==plat) & (df['Anio']==anio))]
    return df_query[df_query['Cantidad']==max(df_query['Cantidad'])]

