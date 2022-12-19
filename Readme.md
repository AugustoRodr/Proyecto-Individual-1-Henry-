 ## <h1 align=center>**Proyecto Individual 1°N**</h1>
 # <h2 align=center>Data Engineering</h2>
 
 <hr>

 ## <h2 align=center>**Introduccion**</h3>

En este proyecto se realiza algunos de los principales procesos que realiza un **Data Engineer** como los son,
la ingesta de datos de diversas fuentes utlizando `Python`, creacion de una API con `FastAPI`, ejecucion de la API en un servidor `Uvicorn` y utilizar `Docker Desktop`, en mi caso.


## **Pasos del proyecto**

1. Ingesta y normalización de datos en funcion del criterio tomado.

2. Relacionar el conjunto de datos y crear la tabla necesaria para realizar consultas. 

3. Crear la API en un entorno Docker

5. Realizar consultas solicitadas


## **ETL - EDA**
Iniciamos el proyecto con la carga de las 4 tablas que conseguiremos en la carpeta **Datasets**.
Dichas tablas son 3 archivos con extencion ``CVS`` y 1 con extencion `JSON`. Al momento de cargar los datasets
los previsualizamos para observar en primeria instancia el aspecto de las tablas y si es necesario hacer alguna modificacion antes de unirlas. Las tablas no necesitaban ninguna modificacion, pero de todas formas agregamos la columna `Categoria` para futuras Querys. Una vez creada las columnas en las tablas las concatenamos y procedemos  realizar la limpieza de datos, utilizando funciones de `Python` buscamos valores faltantes y los contamos para poder dimencionar si es posible eliminar registros, lo cual solo por criterio propio no lo he hecho. Observando los valores de la columna `duration` se denota que es necesario separar su contenido segun las unidades de  `Season` y `min`, para esto se crean las columnas `duration(min)` y `duration(Season)` asignandoles los valores respectivos.
Siempre teniendo en cuenta las Querys a responder se observa que la columna de `cast` debe ser normalizada ya que lo que necesitamos es que esten los nombres de los actores por separado y no como un conjunto. Para solucionar esto utilizamos `Diccionarios en Python` de esta forma podremos filtrar por plataforma y por año a cada actor.
Siguiendo esta logica hacemos lo mismo, crear un diccionario, para la columna de `listed_in` el cual almacenara
las distintas categorias de film segun su plataforma.

## **Creacion de la API**
La creacion de la API se realizo  en el archivo `main.py`. En el archivo main se dan todas las ordenes necesarias
para crear y levantar la API de forma local.

## **Docker**
Con `Docker` podemos crear un contenedor en el cual podra esta nuestra API y podra ser ejecutada de forma funcional. Para la creacion del contenedor se utilizo la terminal de `Visual Studio Code`, tambien podria usarse ``cmd`` ó `git bash`.
### **URLs usados**
+ Creacion de API: https://www.youtube.com/watch?v=dAQENEPAqsc&list=PLt6P0bD6lLRorpc7-VqFaG0ZP4azgzwta&index=3
+ Ayuda con Doker: https://www.youtube.com/watch?v=BvvH3ohis6E&list=PLt6P0bD6lLRorpc7-VqFaG0ZP4azgzwta&index=6

### **Video del PI**
+ https://drive.google.com/drive/folders/1CGYIhpnhYhSxpdu5FIaDWXVra0qzQb_O?usp=sharing
