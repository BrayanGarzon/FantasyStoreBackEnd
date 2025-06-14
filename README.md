# Fantasy Store Django

Django 3.2.24 + Postgres 11 + Dokku Config (Production Ready)

---

## 📁 Estructura del Proyecto

```
.
├── .gitattributes
├── .gitignore
├── app.json              # Configuración para despliegue con Dokku
├── docker-compose.yml    # Configuración del entorno de desarrollo
├── Dockerfile            # Dockerfile para construir la imagen
├── manage.py             # Script de utilidades de Django
├── Procfile              # Archivo de arranque (usado por Heroku/Dokku)
├── README.md             # Este archivo :)
├── requirements.txt      # Dependencias del proyecto
├── .idea/                # Archivos de configuración de PyCharm/IDEA
└── Fantasy Store/         # Directorio principal del proyecto Django
    ├── settings/
    │   ├── common.py         # Configuración común
    │   ├── development.py    # Configuración de desarrollo
    │   └── production.py     # Configuración de producción
    ├── static/               # Archivos estáticos
    ├── templates/            # Plantillas HTML
    ├── urls.py               # Rutas principales
    └── wsgi.py               # Entrada WSGI para producción
```

---

## 🛠️ Instalación

Clona el repositorio y entra al proyecto:

```bash
git clone https://github.com/tu_usuario/domi-express-django.git
cd domi-express-django
```

Si deseas cambiar el nombre del proyecto, puedes hacerlo manualmente o usar herramientas como `make` si tienes algo configurado.

---

## 🐳 Entorno de Desarrollo con Docker

Levanta la aplicación con:

```bash
docker-compose up
```

> Si es la primera vez, puede que la base de datos no esté lista al iniciar. Vuelve a ejecutar `docker-compose up` si falla la primera vez.

Accede a tu proyecto en [http://localhost:8000](http://localhost:8000)

---

### 🔁 Comandos útiles

- Reconstruir imágenes después de instalar nuevas dependencias:

```bash
docker-compose up --build
```

- Eliminar contenedores y la base de datos (útil si hay errores de migración):

```bash
docker-compose down
```

---

## 🔐 Acceso al Admin

La administración de Django está en:

```
http://localhost:8000/admin
```

Credenciales por defecto en desarrollo:

```
Usuario: admin
Contraseña: admin
```

Puedes modificar o eliminar estos fixtures en `fixtures/dev.json`.

---

## 🚀 Despliegue en Producción (Dokku)

### Servidor

1. Crea la app y la base de datos:

```bash
dokku apps:create Fantasy Store
dokku postgres:create Fantasy Store
dokku postgres:link Fantasy Store Fantasy Store
```

> Instala el plugin de Postgres si no lo tienes:

```bash
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
```

2. Establece las variables de entorno necesarias:

```bash
dokku config:set Fantasy Store ENVIRONMENT=production DJANGO_SECRET_KEY=tu_clave EMAIL_PASSWORD=tu_clave_email
```

Variables requeridas:

- `ENVIRONMENT`
- `DJANGO_SECRET_KEY`
- `EMAIL_PASSWORD`

---

### Local

1. Agrega el remoto de producción:

```bash
git remote add production dokku@<tu-servidor.com>:Fantasy Store
```

2. Sube el código:

```bash
git push production master
```

¡Y listo! Tu app se desplegará automáticamente 🚀

---

## 🔒 SSL (HTTPS) Opcional

Para habilitar HTTPS usando Let’s Encrypt:

```bash
dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku letsencrypt Fantasy Store
dokku letsencrypt:cron-job --add
```

---

## ⚙️ Configuración Nginx adicional

Puedes modificar parámetros como el tamaño máximo de archivos directamente en el servidor:

```
/home/dokku/<app>/nginx.conf.d/<app>.conf
```

---

## 📚 Más información

Para más detalles sobre Dokku:
👉 http://dokku.viewdocs.io/dokku/

---

🎉 ¡Proyecto listo para desarrollo y producción!

####
‣慆瑮獡卹潴敲慂正湅੤