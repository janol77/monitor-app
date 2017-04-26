# Aplicación Monitoreo 

Aplicación de monitoreo utilizando MongoDB como base de datos

## Getting Started

Permite tener una versión inicial de la aplicación

### Prerequisites


```
mongoDB
npm
virtualenv

```

### Installing

Instalar bower

```
npm install -g bower
```
Instalar las librerias Js, correr el comando en la raiz del proyecto.


```
bower install
```

Generar el archivo de configuración de la aplicación


```
cp app/config.ini.template app/config.ini
```

Crear ambiente de la aplicación


```
mkvirtualenv flask-app
```

Instalar aplicación


```
python setup.py install
```

Inicializar la Base de datos


```
python manage.py init_db
```

Correr aplicación sin gunicorn


```
sh run.sh
```

Correr aplicación con gunicorn

```
gunicorn -w 4 -b 0.0.0.0:7000 --timeout 180 --error-logfile ../gunicorn_error.log --log-level info server:app

```

## Adicionales

Configuraciones adicionales en caso de ser necesarias

### Supervisord

Archivo de configuración para supervisord y se añade formula para utilizar con gunicorn

```
[program:flask-app.domain.com]
;command=/home/<user>/.virtualenvs/flask-app/bin/gunicorn -w 4 -b 0.0.0.0:7000 --timeout 180 --error-logfile /var/www/flask-app.domain.com/gunicorn_error.log --log-level info server:app
command=/home/<user>/.virtualenvs/flask-app/bin/python /var/www/flask-app.domain.com/app/server.py
autorestart=false
user=<user>
autostart=false
directory=/var/www/flask-app.domain.com/app/
logfile=/var/log/supervisor/flask-app.domain.com.log
redirect_stderr=true
stopasgroup=true
exitcodes=1

```

### Nginx

Archivo de configuración para nginx

```
server {
  listen   80;
  server_name  flask-app.domain.com;
  access_log  /var/log/nginx/flask-app.domain.com.access.log;
  error_log  /var/log/nginx/flask-app.domain.com.error.log notice;
  rewrite_log on;
  index index.php index.html;

  location / {
     client_max_body_size 50M;
     proxy_pass http://localhost:7000;
  }
  location /static/ {
      root /var/www/flask-app.domain.com/app;
      autoindex off;
  }

}

```

## Running the tests

```
python -m unittest2 -v tests.test_user
```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```



## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
