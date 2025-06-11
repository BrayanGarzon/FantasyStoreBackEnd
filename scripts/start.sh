#!/bin/sh

# Si DATABASE_URL está definida, extraer los datos desde allí
if [ -n "$DATABASE_URL" ]; then
  echo "🌐 Entorno de producción detectado. Usando DATABASE_URL..."

  regex="^postgres://([^:]+):([^@]+)@([^:]+):([0-9]+)/(.+)$"
  if echo "$DATABASE_URL" | grep -Eq "$regex"; then
    DB_USER=$(echo "$DATABASE_URL" | sed -E "s#$regex#\1#")
    DB_PASSWORD=$(echo "$DATABASE_URL" | sed -E "s#$regex#\2#")
    DB_HOST=$(echo "$DATABASE_URL" | sed -E "s#$regex#\3#")
    DB_PORT=$(echo "$DATABASE_URL" | sed -E "s#$regex#\4#")
    DB_NAME=$(echo "$DATABASE_URL" | sed -E "s#$regex#\5#")
  else
    echo "❌ DATABASE_URL no tiene un formato válido."
    exit 1
  fi
else
  echo "🧪 Entorno local detectado. Usando variables de entorno..."

  DB_HOST=${DB_HOST:-db}
  DB_PORT=${DB_PORT:-5432}
  DB_USER=${DB_USER:-postgres}
  DB_PASSWORD=${DB_PASSWORD:-postgres}
  DB_NAME=${DB_NAME:-fantasystore}
fi

export PGPASSWORD="$DB_PASSWORD"

echo "⏳ Esperando a que la base de datos en $DB_HOST:$DB_PORT esté lista..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
  echo "Base de datos aún no disponible. Reintentando..."
  sleep 2
done

echo "✅ Base de datos lista. Agregando extensión PostGIS si no existe..."

psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "CREATE EXTENSION IF NOT EXISTS postgis;"

echo "✅ Extensión PostGIS instalada o ya existente."

echo "🚀 Ejecutando comando de desarrollo..."

exec /src/scripts/command-dev.sh
