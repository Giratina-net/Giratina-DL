import os
# postgres
POSTGRES_HOST = "localhost" if os.environ.get("POSTGRES_HOST") == None else os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = "5432" if os.environ.get("POSTGRES_PORT") == None else os.environ.get("POSTGRES_PORT")
POSTGRES_USERNAME = "postgres" if os.environ.get("POSTGRES_USERNAME") == None else os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = "postgres" if os.environ.get("POSTGRES_PASSWORD") == None else os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DATABASE = "postgres" if os.environ.get("POSTGRES_DATABASE") == None else os.environ.get("POSTGRES_DATABASE")
# GDL
GDL_API_KEY = os.environ.get("GDL_API_KEY")
# S3
S3_DOMAIN = os.environ.get("S3_DOMAIN")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
S3_REGION = "us-east-1" if os.environ.get("S3_REGION") == None else os.environ.get("S3_REGION")
S3_BUDGET_NAME = os.environ.get("S3_BUDGET_NAME")
S3_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY")
# kutt
KUTT_HOST = os.environ.get("KUTT_HOST")
KUTT_DOMAIN = os.environ.get("KUTT_DOMAIN")
KUTT_API_KEY = os.environ.get("KUTT_API_KEY")