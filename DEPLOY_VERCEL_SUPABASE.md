# Deploy en Vercel con base de datos Supabase

## 1. Crear la base en Supabase

1. Crea un proyecto en Supabase.
2. Ve a **Project Settings > Database > Connection string**.
3. Para Vercel usa preferiblemente **Transaction pooler** o **Supavisor transaction mode**.
4. Copia la URL y agrega `?sslmode=require` si no viene incluido.

Formato esperado:

```text
postgresql+psycopg2://postgres.PROJECT_REF:DB_PASSWORD@POOLER_HOST:6543/postgres?sslmode=require
```

## 2. Migrar el SQL

Desde tu equipo, con `psql` instalado:

```powershell
$env:PGPASSWORD="TU_PASSWORD_SUPABASE"
psql "postgresql://postgres.PROJECT_REF:TU_PASSWORD_SUPABASE@POOLER_HOST:6543/postgres?sslmode=require" -f todoen1unos_pg.sql
psql "postgresql://postgres.PROJECT_REF:TU_PASSWORD_SUPABASE@POOLER_HOST:6543/postgres?sslmode=require" -f migrations/2026-05-20_fix_vehiculos_columns.sql
```

Si Supabase te da una URL directa `db.PROJECT_REF.supabase.co:5432`, úsala para migraciones solo si tu red soporta IPv6 o tienes el add-on IPv4. Para Vercel, deja la app usando el pooler.

## 3. Variables de entorno en Vercel

En **Vercel > Project > Settings > Environment Variables**, agrega:

```text
APP_SECRET_KEY
DATABASE_URL
MAIL_SERVER
MAIL_PORT
MAIL_USE_TLS
MAIL_USERNAME
MAIL_PASSWORD
CLOUDINARY_URL
SUPABASE_URL
SUPABASE_KEY
SUPABASE_SERVICE_ROLE_KEY
```

`DATABASE_URL` debe apuntar al pooler de Supabase y usar SSL:

```text
postgresql+psycopg2://postgres.PROJECT_REF:DB_PASSWORD@POOLER_HOST:6543/postgres?sslmode=require
```

## 4. Desplegar

Con Vercel CLI:

```powershell
npm i -g vercel
vercel login
vercel
vercel --prod
```

También puedes conectar el repositorio desde el dashboard de Vercel. La entrada serverless está en `api/index.py`.

## 5. Notas importantes

- Vercel no ofrece almacenamiento persistente para archivos subidos. Usa Cloudinary para imágenes.
- Las cargas de vehículos ya usan `/tmp` como temporal en Vercel y luego Cloudinary. Antes de producción, migra también perfiles, documentos, comprobantes y promos a Cloudinary o Supabase Storage.
- No subas `.env` a Vercel ni al repositorio; usa `.env.example` como guía.
- Este proyecto usa `vercel.json` para redirigir todas las rutas Flask a `api/index.py`.
- La versión Python está fijada en `.python-version` como `3.12`.
