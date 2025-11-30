from app.models.incident import Base
from app.services.database import engine
from sqlalchemy import inspect

print("Checking existing tables...")
inspector = inspect(engine)
existing_tables = inspector.get_table_names()
print(f"Existing tables: {existing_tables}")

print("\nCreating/updating database tables...")
Base.metadata.create_all(bind=engine)

print("\nVerifying tables...")
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"✅ Tables created: {tables}")

if 'incidents' in tables:
    print("✅ SUCCESS! Database is ready to use!")
else:
    print("❌ ERROR: Tables not created properly")
