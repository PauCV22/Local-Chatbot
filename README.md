# Local-Chatbot
# Explicación ordenada del proyecto: Chatbot Matemático RAG

Este proyecto consiste en el desarrollo de un chatbot matemático basado en una arquitectura RAG (Retrieval-Augmented Generation), capaz de responder preguntas a partir del contenido extraído de documentos PDF. Para construirlo correctamente, se siguió un proceso cronológico que va desde la creación inicial del repositorio hasta el despliegue final del servidor web y la integración completa del sistema de recuperación y generación de respuestas.

## 1. Creación del repositorio e inicio del proyecto

El proyecto comenzó desde cero con la creación de un directorio base y su vinculación con GitHub. En esta fase se configuró un repositorio remoto con licencia Apache 2.0 y un archivo `.gitignore` específico para Python, con el objetivo de mantener una buena organización desde el inicio y evitar subir archivos innecesarios al repositorio.

Después, mediante `git clone`, el repositorio se descargó en local para poder trabajar desde la terminal y asegurar que todos los cambios realizados en el entorno local quedaran sincronizados con la nube.

## 2. Estructura de carpetas y archivos

Una vez clonado el repositorio, se pasó a definir la arquitectura interna del proyecto utilizando VS Code como editor principal. Para automatizar esta parte, se ejecutó un script llamado `template.sh`, que contenía comandos `mkdir` para crear las carpetas necesarias, como `src` y `research`, además de los archivos correspondientes dentro de cada una.

Este script finalizaba con un comando `echo` para confirmar que la creación de la estructura se había realizado sin errores. Cuando todo estuvo generado correctamente, los cambios se guardaron en GitHub con la secuencia habitual de comandos:

sh template.sh
git add .
git commit -m "Estructura de proyecto creada correctamente"
git push origin main

## 3. Creación del entorno virtual e instalación de dependencias

Con la estructura base ya creada, el siguiente paso fue preparar un entorno controlado para trabajar de forma ordenada y evitar conflictos entre librerías. Para ello se utilizó Anaconda, creando un entorno virtual específico para el chatbot con Python 3.10.

Los comandos utilizados fueron:

conda create -n chatbot python=3.10 -y
conda activate chatbot

Antes de instalar dependencias, se prepararon dos archivos importantes: `setup.py`, que define la estructura del paquete, y `requirements.txt`, que contiene el listado exacto de librerías y versiones necesarias para ejecutar el proyecto. Después, se instalaron todas las dependencias con:

pip install -r requirements.txt

## 4. Configuración de variables de entorno, APIs y modelo de lenguaje

Una vez preparado el entorno, se creó un archivo `.env` para gestionar credenciales de forma segura. En este archivo se guardó la API de Pinecone, obtenida al crear el proyecto dentro de su plataforma.

Durante el diseño inicial se valoró utilizar la API de ChatGPT, pero esta opción fue descartada por sus limitaciones de tokens tras su debida comprovacin. En su lugar, el sistema se configuró para usar un modelo local con Ollama, lo que permite realizar consultas sin depender de restricciones externas de uso.

En esta etapa también se realizó la conexión entre la aplicación y Pinecone, además de la preparación del índice vectorial donde posteriormente se almacenarían los datos procesados.

Para poder vincular el chatbot correctamente junto al modelo de IA local debimos modificar el archivo requirements.txt y anadir el contenido necesario para ello. Una vez finalizado y ejecutado de nuevo deberiamos indicarle en el archivo trials en el archivo app.py el modelo que debemos usar procedente de Ollama y previamente configurado y descargado.

## 5. Entorno de pruebas con `trials.ipynb`

Antes de integrar todo el sistema final, se creó una libreta de Jupyter llamada `trials.ipynb` para comprobar que cada parte funcionara correctamente por separado. Esta libreta sirvió como entorno de validación técnica antes de pasar al desarrollo definitivo.

En esta fase se hicieron varias comprobaciones: primero, se ejecutaron comandos del sistema para verificar el directorio de trabajo y asegurar que el entorno virtual estuviera correctamente ubicado. Después, se importaron los módulos necesarios de LangChain, que eran esenciales para cargar y dividir archivos PDF.

A continuación, se probó la función `load_pdfs_files`, apuntando directamente a la carpeta de datos para validar que las rutas y las bibliotecas se ejecutaran sin errores. El resultado fue positivo: la libreta procesó correctamente el documento `Encyclopaedia in Mathematics.pdf`, extrayendo tanto su estructura general como conceptos matemáticos concretos. Entre ellos se identificaron reglas fundamentales de geometría como AAA, AAS, ASA, SAS y SSS.

## 6. Modularización del procesamiento de datos en `helper.py`

Tras comprobar que la extracción de información funcionaba bien, el código experimental se reorganizó en funciones reutilizables dentro del archivo `helper.py`. Este paso fue importante porque permitió transformar una prueba aislada en una parte estable y modular del proyecto.

En este archivo se definieron tres procesos principales:

Primero, la extracción y limpieza del contenido. Para ello se implementó la función `load_pdf_file`, que utiliza `PyPDFLoader` y `DirectoryLoader` para leer de forma masiva los documentos PDF dentro de la carpeta `data`. Después, la función `filter_to_minimal_docs` limpia los datos y conserva solo el texto útil y la ruta de origen, eliminando información innecesaria para optimizar el procesamiento.

Después se realizó la división del texto, también conocida como chunking. Para esta tarea se creó la función `text_split`, basada en `RecursiveCharacterTextSplitter`. Su función es dividir cada documento limpio en fragmentos pequeños de 200 caracteres, con una superposición de 20 caracteres entre fragmentos para no perder contexto entre partes consecutivas del texto.

Por último, se implementó la vectorización del contenido. La función `download_hugging_face_embeddings` carga el modelo `sentence-transformers/all-MiniLM-L6-v2` desde Hugging Face. Este modelo convierte cada fragmento de texto en un vector numérico o embedding, que más adelante se almacenará en Pinecone para facilitar la búsqueda semántica.

## 7. Definición del comportamiento del chatbot en `prompt.py`

Una vez preparada la información, fue necesario controlar cómo debía responder el modelo local. Para ello se creó el archivo `prompt.py`, donde se definió una variable llamada `system_prompt`.

Este prompt cumple la función de restringir y orientar el comportamiento del chatbot. Primero, le asigna un rol concreto: actuar como un asistente matemático especializado en preguntas y respuestas. Segundo, evita alucinaciones obligando al modelo a responder únicamente con la información recuperada desde los fragmentos de contexto. Si la respuesta no se encuentra dentro de ese contenido, el sistema debe admitir que no dispone de la información. Tercero, limita la extensión de las respuestas a un máximo de tres oraciones, lo que garantiza que las respuestas sean breves, precisas y directas.

## 8. Configuración del paquete en `setup.py`

Para que el proyecto estuviera correctamente empaquetado y fuera más fácil de instalar o reutilizar en otros entornos, se configuró el archivo `setup.py`. Este archivo define los metadatos principales del proyecto, incluyendo el nombre del paquete, su versión inicial `0.1.0` y la autoría, registrada a nombre de Pau Cortinas Vidal.

Además, se utilizó la función `find_packages()`, que permite localizar automáticamente todos los módulos de Python dentro del proyecto. Gracias a esto, carpetas como `src` pueden reconocerse como paquetes ejecutables sin necesidad de configurar rutas de manera manual.

## 9. Creación de la base de datos vectorial e ingesta de datos

Cuando todo el procesamiento previo ya estaba listo, se pasó a construir la base de conocimientos del chatbot. Para ello se creó un script específico encargado de conectar con Pinecone e insertar los vectores generados a partir de los documentos PDF.

Este archivo importa las funciones definidas en `helper.py` y carga de forma segura la clave API desde las variables de entorno. Después ejecuta de forma secuencial todo el flujo: extracción de PDFs desde `data/`, limpieza del texto, división en fragmentos y generación de embeddings.

Una vez preparado el contenido vectorial, el sistema se conecta a Pinecone y comprueba si el índice `mathbot` ya existe. Si no está creado, lo genera desde cero con una arquitectura de 384 dimensiones, una métrica de similitud del coseno y un despliegue serverless sobre AWS. Finalmente, todos los fragmentos de texto convertidos en vectores se insertan masivamente dentro de ese índice.

## 10. Despliegue de la aplicación principal en `app.py`

La última etapa del proyecto corresponde a la aplicación principal, que es la parte visible e interactiva del chatbot. Este archivo levanta un servidor web con Flask y actúa como núcleo del sistema RAG.

A diferencia de los scripts anteriores, `app.py` no procesa nuevos documentos. Su función es conectarse al índice `mathbot` ya creado en Pinecone y utilizarlo como retriever, configurado para recuperar los tres fragmentos más similares a la consulta del usuario.

Al mismo tiempo, se inicializa el modelo local `ChatOllama` usando `llama3.1` y ajustando la temperatura a `0`, una decisión técnica que garantiza respuestas deterministas, analíticas y centradas exclusivamente en los hechos recuperados.

Con esta configuración, se construye la cadena RAG completa, combinando tres elementos: el motor de búsqueda de Pinecone, el prompt del sistema y el modelo generativo de Ollama.

Para que el usuario pueda interactuar con el chatbot de manera sencilla, Flask define dos rutas principales. La ruta `/` carga la interfaz gráfica mediante el archivo `chat.html`, mientras que la ruta `/ask` recibe las preguntas del usuario por método POST, ejecuta la cadena RAG y devuelve la respuesta matemática generada por la inteligencia artificial.

De esta forma, el servidor permanece activo de forma continua en el puerto `8080`, permitiendo una interacción estable entre el usuario y el chatbot.

## Conclusión

En conjunto, este proyecto sigue una evolución lógica y ordenada: primero se crea la base del repositorio, después la estructura del proyecto, luego el entorno de trabajo, la configuración de dependencias, la preparación de datos, la vectorización, el almacenamiento en Pinecone y, finalmente, el despliegue del chatbot con Flask.

Gracias a esta organización, el resultado final es un sistema RAG funcional, modular y bien estructurado, capaz de responder preguntas matemáticas a partir de contenido real extraído de documentos PDF.
