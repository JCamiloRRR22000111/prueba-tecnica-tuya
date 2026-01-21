# 1.	Ejercicio Conceptual de Creación de Dataset de Números de Teléfono de Clientes
Diseñar e implementar un proceso automatizado y controlado mediante prácticas de CI/CD para la creación, validación, despliegue y mantenimiento de un dataset confiable de números de teléfono de clientes. Este dataset será utilizado para mejorar la comunicación y el servicio al cliente.
---
Solución:

•	Obtención de los datos y creación del dataset 
-

El dataset se construye a partir de la información almacenada en alguna librería de SQL que se encuentre en bodega. La idea es crear una conexión entre SQL y Python para extraer la información. A partir de una consulta de SQL se extraerían los siguientes dos campos:

Identificacion: Número de identificación del cliente.

Telefono: Número de teléfono del cliente.

Adicionalmente se podría tener en cuenta otros campos como el nombre del cliente o el código del país, pero en este caso doy por hecho que todos los números de teléfono son colombianos.

Los datos de la consulta quedan almacenados en un dataframe de Pandas.

•	Validación automática de los datos
-

Lo siguiente es realizar algunas validaciones con la información que se almacenó en el dataframe:

•	Que no haya datos nulos en ninguno de los dos campos.

•	Tanto el número de teléfono como el de identificación deben contener solo caracteres numéricos.

•	El número de teléfono debe tener una longitud exacta de 10 dígitos.

•	No puede haber números de teléfono o identificación repetidos. 

En este punto la idea es separar los registros que cumplen con la validación y los que no. Los registros que cumplan con la validación se van a almacenar en un dataframe que para el ejemplo se va a llamar df_validados y los registros que no cumplieron con al menos una de las validaciones se van a guardar en un dataframe llamado df_errores.

Con respecto a df_errores, es importante mencionar que, aunque presente un error no va a parar de validar ese registro, por el contrario, se van a realizar todas las validaciones, esto porque para df_errores va a existir una tercera columna llamada “Observacion”, en esta columna se van a registrar todos los errores que presenten cada uno de los números analizados. Lo que se busca con esta nueva columna es que se pueda hacer un seguimiento a los números que presentan errores y se conozca con certeza por qué dan error.

•	Test de calidad
-

Luego de terminar la pruebas de validación, se ejecutan automáticamente las pruebas de calidad, estas pruebas buscan que el dataset cumpla con unos estándares mínimos antes de realizar el despliegue. Estas pruebas de calidad se realizan a nivel global y validan:

	Que se cumpla con un porcentaje mínimo de registros válidos.

	Existencia de errores críticos, como por ejemplo números de teléfono vacíos o formatos inválidos, aunque esto ya se validó en la parte de validación de los datos, en este caso se lleva a un enfoque más global, en el ejemplo de los teléfonos nulos lo que se va a validar es la cantidad de campos vacíos con respecto al total de registros del dataset, en caso de que se alcance o pase cierto umbral de datos vacíos, se considera que la información no es confiable y no está lista para el despliegue. 

	Que se cumpla con un volumen de datos esperado, debería haber cierta cantidad mínima de registros.

•	Despliegue del dataset
-

Finalmente, luego de que los datos se hayan validado y se haya hecho los test de calidad, se realiza un despliegue continuo del dataset. La idea es que el dataset se guarde automáticamente como archivo de Excel en una ruta especifica, se eligió el formato como Excel porque la intención es que el archivo tenga 2 hojas, la primera hoja va a contener los datos que pasaron la validación, mientras que la segunda hoja va a contener los registros que dieron errores y en la columna “Observacion” la razón de los errores. El dataset se va a guardar de forma versionada para tener un historial de cambios, por ejemplo la primera versión se llamaría “telefonos_v1.xlsx” y  la segunda versión “telefonos_v2.xlsx”

# 2.	Ejercicio Conceptual de KPI's  

Con base en el resultado del ejercicio conceptual de creación de dataset, plantea también de forma conceptual un mecanismo/herramienta que permita hacer veeduría de la calidad de datos, trazabilidad del dato, etc. Esta será un recurso para los equipos de negocio para obtener KPI's acerca de los teléfonos de los clientes.
---
Solución:

Relacionándose con el ejercicio anterior, se plantea un sistema de monitoreo de calidad de los datos que esté integrado al pipeline que se desarrolló. El mecanismo se apoyará en:

•	Métricas automáticas que se generaran cada que se ejecute el código diseñado anteriormente.

•	Un registro histórico de los resultados obtenidos.

•	Visualización de KPI’s mediante reportes o dashboards.

El objetivo de este mecanismo es que los equipos de negocio puedan evaluar la calidad del dataset en el tiempo, identifiquen problemas recurrentes en los datos y medir como las mejoras o correcciones en la fuente de información impactan al resultado final.

Generación de métricas
-

Cada que el código se ejecute se generarán métricas automáticas relacionadas con la validación y calidad del dataset, como por ejemplo:

•	Cantidad de registros procesados.

•	Número de registros válidos.

•	Número de registros con errores.

•	Cantidad de errores por tipo.

•	Versión del dataset que se generó.

•	Fecha y hora de ejecución.

El resultado de estas métricas se puede almacenar en un archivo de Excel, en el cual cada fila representa una ejecución del código. También otra opción sería guardarlo en una tabla de SQL en la cual cada nueva ejecución inserta también un nuevo registro con los resultados de las métricas.

KPI’s de calidad
-

A partir de las metricas obtenidas se proponen los siguientes KPI’s clave:

•	Porcentaje de teléfonos válidos, lo que se busca es medir la proporción de registros que cumplen con todas las validaciones, lo cual permite evaluar el nivel general de la calidad del dataset.

•	Porcentaje de errores, mide la tasa de registros rechazados durante el proceso de validación, lo cual permite identificar el deterioro en la calidad de los datos y ayuda a detectar problemas en la fuente de la información.

•	Distribución de tipos de error, mide la frecuencia de cada tipo de error, lo cual permite priorizar acciones correctivas.

•	Evolución de la calidad en el tiempo, compara los resultados entre las diferentes versiones del dataset y permite evaluar si las acciones tomadas están siendo efectivas.

•	Volumen de datos confiables, mide la cantidad de registros validos que están disponibles, lo cual puede servir para evaluar el impacto del dataset en procesos de comunicación con el cliente.

Trazabilidad de los datos
-

Mediante el mecanismo propuesto se garantiza una trazabilidad, debido a que se realiza un versionado del dataset, se registran métricas cada que se ejecuta el código, se conservan los registros con errores y se proporciona información acerca de la causa del error. Estas medidas permiten rastrear el origen de los datos, auditar cambios entre versiones y identificar cuando y por qué un registro fue rechazado.

Herramientas de visualización
-

Para facilitar el acceso a los KPI’s se propone hacer uso de alguna herramienta de visualización, como dashboards en Power BI o Tableau. También se pueden generar reportes automáticos en Excel. La idea es que el equipo de negocios pueda acceder y consultar el estado actual de la calidad del dataset, KPI’s históricos y alertas en caso de que algún indicador caiga por debajo de un umbral definido.

Veeduría y control continuo de la calidad
-

Gracias a este mecanismo de KPI’s se puede establecer un un proceso de veeduría continua, que permita establecer umbrales mínimos aceptables por KPI, alertas automáticas cuando disminuya la calidad, bloqueo de despliegue del dataset en caso de que no se cumpla con criterios críticos y seguimiento periódico por parte del equipo de negocio.

# 3.	Rachas

Voy a describir el paso a paso que voy siguiendo para el desarrollo del ejercicio:

•	Usando MySQL, creo una base de datos que se llama prueba_tecnica y creo las tablas historia y retiros.
 
•	Del archivo de Excel que me pasaron lo convierto en dos archivos CSV, uno para cada hoja, historia y retiros. Luego importo dichos archivos a MySQL y los asocio a las tablas que cree anteriormente.

Nota: Tuve que cambiar el formato de las fechas a yyyy/mm/dd para que MySQL me dejara importar los registros.
 
•	Sigo con el siguiente paso que es clasificar a los clientes por nivel de deuda siguiendo las indicaciones del ejercicio. Para el desarrollo del ejercicio lo separo por partes, creando varios CTE, de la siguiente forma: 

	El primer CTE se llama historia_mes, básicamente lo uso para darle formato a la columna corte_mes que voy a estar usando.

	El CTE primera_aparicion sirve para calcular la primera fecha de aparición de cada cliente, dicha fecha de aparición se guarda en una columna llamada fecha_inicio.

	El CTE calendario crea un calendario general que inicia en la primera fecha de aparición que se tiene registro y suma un mes a cada fecha hasta llegar al 31/12/2024.

	Calendario_cliente crea un calendario para cada cliente, el cual va desde la primera aparición de dicho cliente hasta el 31/12/2024.

	Calendario_filtrado excluye aquellos campos en los cuales el cliente tiene fecha de retiro y la fecha del calendario anterior es mayor a la fecha de retiro, de forma que si un cliente tiene fecha de retiro, su calendario va hasta la fecha de retiro.

	El CTE dataset_completo hace un left join entre el CTE calendario_filtrado y el CTE historia_mes. La cuestión es que, al hacer esta unión, los campos correspondientes a fechas faltantes de un cliente en historia_mes van a tener valor nulo en la columna saldo, a estos campos con valor nulo en saldo se les da un valor de cero.

	En el CTE dataset_final se crea la columna nivel, clasificando de acuerdo con el valor almacenado en saldo.

	En el CTE racha_base se crea una nueva columna a partir de la resta de dos row_number(). El primer row_number() crea una numeración consecutiva que se particiona (o sea que se reinicia) cada que se cambia de identificación. El segundo row_number() crea una numeración que se particiona cada que se cambia de identificación o de nivel. La lógica de restar estos dos row_number() es que cada que la columna grp cambia de valor significa que una racha termina y otra empieza.

	El CTE rachas se agrupa por las columnas  identificación, nivel y grp. De esta forma se pueden agrupar más de una fecha. Se calcula en una columna la fecha de inicio de la agrupación, la fecha de fin y la cantidad de registros que se agrupan, esta cantidad de registros que se agruparon corresponden a las rachas.

	Para caso del ejercicio, en el CTE rachas_validad filtro solo por las rachas que sean mayores o iguales a 3.

	En el CTE racha_final se le da orden a las rachas, lo primero que se evalúa es para un cliente cual es su racha mayor, en una columna llamada rn, a la racha mayor se le da valor 1, a la segunda 2 y así consecutivamente. Si un mismo cliente tiene dos rachas iguales, se le da prioridad la que tiene la fecha más reciente.
	En la consulta final se traen los campos que se desean mostrar y se filtra por los campos de la columna rn que sean igual a 1, de esta forma se está trayendo la mayor racha de cada cliente que tuvo al menos una racha mayor a 3.
 


# 4.	Procesamiento de archivos HTML en Python

Para el desarrollo de este ejercicio, primero creé tres páginas de html muy simples, cada página contiene dos imágenes. Las dos primeras páginas las guardé dentro de una carpeta que está en la misma ruta del código que iba a desarrollar, la tercera página la guardé directamente en la carpeta donde esta el código. La intención con esto es que para las dos primeras páginas el código encuentre los archivos html mediante el directorio y para la tercera página pasarle la ruta completa del archivo.

Pasando al código, lo primero que hice fue crear una lista llamada paths, la cual contiene la ruta del directorio donde están las dos primeras páginas y la ruta completa de la tercera página.

En una variable llamada html_files llamo a la función gather_html_files() y le paso como parámetro la lista con las rutas. Dentro de esta función recorro cada una de las rutas mediante un bucle y en cada iteración verifico si la ruta corresponde a un archivo de html, en caso de ser así, se guarda la ruta del archivo en una lista llamada html_files. En caso de que la ruta no corresponda a un archivo, pero sí a un directorio, se recorre cada uno de los archivos y subdirectorios que están en la ruta y verifica si son archivos html, cada archivo html que encuentra la guarda en la lista html_files. Finalmente retorna el valor de html_files.
De nuevo en el flujo principal se declara una variable llamada output_directory la cual almacena la ruta en que se van a guardar los archivos html con base64.
En una variable llamada results, se llama a la función process_html_files y se le pasa como parámetros de entrada las variables html_files y output_directory. Dentro de la función se declara un diccionario llamado results el cual tiene dos claves: “success” y “fail”, pero ninguna de las claves tiene ningún valor por el momento. Se hace una verificación para confirmar que la ruta de salida realmente existe. Se realiza un bucle que itera cada una de las direcciones que contiene la variable html_files, dentro del bucle se crea un objeto llamado parser el cual pertenece a la clase HTMLImageParser, al crear el objeto este va al constructor de la clase, el cual hereda de la clase HTMLParser, además crea una lista vacía en la cual se van a guardar las rutas de todas las imágenes. Continuando con el flujo del bucle, en una variable llamada html_content se abre y se lee el archivo html que se está analizando. Posteriormente el objeto parser llama al método feed, el cual proviene de HTMLParser y se encarga de recorrer y analizar todo el html, cada que encuentre una etiqueta de apertura se llama al método handle_starttag, el cual verifica si dicha etiqueta corresponde a una imagen, en caso de ser así, se busca el atributo src y en caso de encontrarlo se agrega a la lista de imágenes que se inicializó cuando el constructor creo el objeto parser.

Continuando con el bucle que recorre los archivos, se crea una copia del archivo que se va a modificar, además se crean dos listas vacías, una para almacenar los casos de éxito y otra para almacenar los casos de error.

Se crea un nuevo bucle que recorre cada una de las imágenes que el objeto parser encontró, dentro de este bucle se crea una ruta relativa en la cual debería estar la imagen, se llama a la clase imageconverter y se le pasa la ruta relativa de la imagen que se calculó. La clase imageconverter es un método estático, por lo tanto, no es necesario crear un objeto, dentro de esta clase en la función image_to_base64, se recibe la ruta de la imagen. Se abre el archivo en modo binario, lee los bytes de la imagen y los convierte a base64 para después convertirlo a cadena de texto y poder ponerlo en html. Finalmente se devuelve el data uri, o sea que se incrusta la cadena base64 al html. En caso de que haya algún error en este proceso se retorna una cadena vacía.
Se verifica si la ruta que se retornó está vacía o no, en caso de no estar vacía se reemplaza la ruta de la imagen por la cadena base64 y se almacena la ruta de la imagen en la lista que almacena los casos de éxito. En caso de que la ruta que se retornó esté vacía, se almacena la ruta de la imagen en la lista con los casos de error.

Finalmente se guarda el nuevo archivo sin sobre escribir el original, se guardan y se retornan los resultados de éxito y fallidos al flujo principal, donde se imprime la información en pantalla.
