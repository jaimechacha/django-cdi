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
5. Ejecutar migraciones
    ````shell script
    python manage.py makemigrations
    ````
6. Confirmar migraciones
    ````shell script
    python manage.py migrate
    ````
7. Cargar respaldo
    ````shell script
     python manage.py loaddata deploy/backup.json --exclude contenttypes
    ````
8. Incorporar librerias externas dentro del folder static/lib
    ````shell script
    Dentro de la ruta static crear la carpeta lib y dentro incluir todas las librerias externas
   adminlte-3.0.5
   bootstrap-4.3.1
   bootstrap-daterangepicker-3.0.5
   ...etc
    ````
9. Restaurar los archivos de media
    ````shell script
    En la ruta principal volver a copiar la carpeta media
    ````
10. Ejecutar el proyecto
    ````shell script
    python manage.py runserver
    ````