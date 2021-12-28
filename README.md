# Instalar el proyecto
1. Clonar el repositorio del proyecto o descargar el zip 
    ````shell script
    git clone https://github.com/Anderson-Pozo/django-cdi.git
    ````
2. Crear entorno virtual en la ruta principal del proyecto
    ````shell script
    python -m venv venv
    ````
3. Activar entorno virtual
    ````shell script
    .\venv\Scripts\activate
    ````
4. Instalar dependencias
    ````shell script
    pip install -r .\requirements\requirements.txt
    ````
5. Si ya existe la db saltar al paso 10

6. Crear carpeta db en la raiz del proyecto
    ````shell script
    db/
    ````
7. Ejecutar migraciones
    ````shell script
    python manage.py makemigrations
    ````
8. Confirmar migraciones
    ````shell script
    python manage.py migrate
    ````
9. Cargar respaldo
    ````shell script
     python manage.py loaddata deploy/backup.json --exclude contenttypes
    ````
10. Incorporar librerias externas dentro del folder static/lib
    ````shell script
       Dentro de la ruta static crear la carpeta lib y dentro incluir todas las librerias externas
       adminlte-3.0.5
       bootstrap-4.3.1
       bootstrap-daterangepicker-3.0.5
       ...etc
    ````
11. Restaurar los archivos de media
    ````shell script
    En la ruta principal volver a copiar la carpeta media
    ````
12. Ejecutar el proyecto
    ````shell script
    python manage.py runserver
    ````