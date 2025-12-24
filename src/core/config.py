import os

from dotenv import load_dotenv

load_dotenv()


# ---- Project ----
PROJECT_NAME = os.getenv("PROJECT_NAME")


# ---- Elasticsearch ----
ELASTIC_HOST = os.getenv("ELASTIC_HOST")
ELASTIC_INDEX = os.getenv("ELASTIC_INDEX")


# ---- Redis ----
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB=0


# ---- Cache ----
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS"))