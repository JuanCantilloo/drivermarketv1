import os
from urllib.parse import quote_plus, unquote, urlparse, parse_qs

from dotenv import load_dotenv


load_dotenv(encoding="utf-8")


def get_database_url():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    user = quote_plus(os.getenv("DB_USER", "postgres"))
    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "todoen1unos")
    sslmode = os.getenv("DB_SSLMODE")
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    if sslmode:
        url = f"{url}?sslmode={quote_plus(sslmode)}"
    return url


def get_psycopg2_params():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        parsed = urlparse(database_url.replace("postgresql+psycopg2://", "postgresql://", 1))
        params = {
            "host": parsed.hostname,
            "user": unquote(parsed.username or ""),
            "password": unquote(parsed.password or ""),
            "dbname": unquote(parsed.path.lstrip("/") or "postgres"),
            "port": parsed.port or 5432,
        }
        query = parse_qs(parsed.query)
        sslmode = query.get("sslmode", [os.getenv("DB_SSLMODE")])[0]
        if sslmode:
            params["sslmode"] = sslmode
        return params

    params = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
        "dbname": os.getenv("DB_NAME", "todoen1unos"),
        "port": int(os.getenv("DB_PORT", "5432")),
    }
    if os.getenv("DB_SSLMODE"):
        params["sslmode"] = os.getenv("DB_SSLMODE")
    return params
