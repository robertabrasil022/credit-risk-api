from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Banco de dados
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # API
    API_VERSION: str
    DEBUG: bool

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = {"env_file": ".env"}

# Instância global — importada por todo o projeto
settings = Settings()