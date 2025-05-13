import os

from dotenv import load_dotenv
from minio import Minio

load_dotenv()


class Settings:

    @staticmethod
    def app_config() -> dict:
        app_name = os.environ.get("APP_NAME")
        api_version = os.environ.get("API_VERSION")

        return {
            'app_name': app_name,
            'api_version': api_version,
        }

    @staticmethod
    def postgres_db_url() -> str:
        db_host = os.getenv('POSTGRES_DB_HOST')
        db_port = os.getenv('POSTGRES_DB_PORT')
        db_user = os.getenv('POSTGRES_DB_USER')
        db_password = os.getenv('POSTGRES_DB_PASSWORD')
        db_name = os.getenv('POSTGRES_DB_NAME')

        return f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    @staticmethod
    def jwt_config() -> dict:
        secret_key = os.getenv('SECRET_KEY')
        algorithm = os.getenv('ALGORITHM')
        access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

        return {
            'secret_key': secret_key,
            'algorithm': algorithm,
            'access_token_expire_minutes': access_token_expire_minutes
        }

    @staticmethod
    def get_minio_client() -> Minio:
        return Minio(
            endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
            secure=os.getenv("MINIO_SECURE", "False").lower() == "true"
        )


settings = Settings()
