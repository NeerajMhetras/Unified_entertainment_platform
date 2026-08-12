from app.database.database import Base, engine

# Import models so SQLAlchemy registers them
from app.models import entertainment
from app.models import movie
from app.models import series
from app.models import game
from app.models import book
from app.models import entertainment_log
from app.models import user


print("Tables known to SQLAlchemy:")
print(Base.metadata.tables.keys())

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Database tables recreated successfully.")