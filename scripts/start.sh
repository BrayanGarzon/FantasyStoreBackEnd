#!/bin/sh

DB_HOST="dpg-d14dj2ripnbc73f9f1r0-a.oregon-postgres.render.com"
DB_PORT="5432"
DB_USER="fantansy"

echo "Esperando a que la base de datos en $DB_HOST:$DB_PORT esté lista..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
  echo "Base de datos aún no disponible. Reintentando..."
  sleep 2
done

echo "✅ Base de datos lista. Ejecutando comando de desarrollo..."

exec /src/scripts/command-dev.sh
