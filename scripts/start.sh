#!/bin/sh

DB_HOST="dpg-d0gego2dbo4c73balfs0-a.oregon-postgres.render.com"
DB_PORT="5432"
DB_USER="example_v761_user"

echo "Esperando a que la base de datos en $DB_HOST:$DB_PORT esté lista..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
  echo "Base de datos aún no disponible. Reintentando..."
  sleep 2
done

echo "✅ Base de datos lista. Ejecutando comando de desarrollo..."

exec /scripts/command-dev.sh
