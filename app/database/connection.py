from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Cria o engine de conexão com o PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG
)

# Fábrica de sessões — cada requisição recebe uma sessão isolada
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Classe base para todos os modelos do banco
class Base(DeclarativeBase):
    pass

# Dependency injection — fornece e fecha sessão automaticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()