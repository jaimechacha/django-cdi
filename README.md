# Instalar el proyecto
1. Clonar el repositorio del proyecto o descargar el zip 
    ````shell script
    git clone https://github.com/Anderson-Pozo/django-cdi.git
    ````
2. Crear entorno virtual en la ruta principal del proyecto
    ````shell script
    python -m venv venv
    ````
3. Crear archivo .env en la ruta principal del proyecto y agregar lo siguiente
    ````shell script
      DB_NAME=YOUR_DB_NAME
      DB_USER=YOUR_DB_USER
      DB_PASSWORD=YOUR_USER_PASSWORD
      DB_HOST=localhost
    
      BACKEND_EMAIL=django.core.mail.backends.smtp.EmailBackend
      HOST_EMAIL=smtp.something.com
      USER_EMAIL=myawesomeemail@test.com
      USER_PASSWORD=my_awesome_password
      PORT_EMAIL=587
    ````
4. Activar entorno virtual
    ````shell script
    .\venv\Scripts\activate
    ````
5. Instalar dependencias
    ````shell script
    pip install -r .\requirements\requirements.txt
    ````
6. Si ya existe la db saltar al paso 10

7. Crear carpeta db en la raiz del proyecto
    ````shell script
    db/
    ````
8. Ejecutar migraciones
    ````shell script
    python manage.py makemigrations
    ````
9. Confirmar migraciones
    ````shell script
    python manage.py migrate
    ````
10. Cargar respaldo
     ````shell script
      python manage.py loaddata deploy/backup.json --exclude contenttypes
     ````
11. Incorporar librerias externas dentro del folder static/lib
    ````shell script
       Dentro de la ruta static crear la carpeta lib y dentro incluir todas las librerias externas
       adminlte-3.0.5
       bootstrap-4.3.1
       bootstrap-daterangepicker-3.0.5
       ...etc
    ````
12. Restaurar los archivos de media
    ````shell script
    En la ruta principal volver a copiar la carpeta media
    ````
13. Ejecutar el proyecto
    ````shell script
    python manage.py runserver
    ````