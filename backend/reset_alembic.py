from app.services.database import engine
from sqlalchemy import text

# Drop alembic_version table if it exists
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))
    conn.commit()
    print("✅ Alembic version table dropped")
