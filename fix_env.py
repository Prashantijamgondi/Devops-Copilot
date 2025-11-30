
import os

def update_env():
    lines = []
    with open('.env', 'r') as f:
        lines = f.readlines()

    new_lines = []
    user = "postgres"
    password = "postgres" # Default assumption if not found, but we'll try to find it
    dbname = "store_db"

    # First pass to find values
    for line in lines:
        if line.strip().startswith('POSTGRES_USER='):
            user = line.strip().split('=')[1]
        if line.strip().startswith('POSTGRES_PASSWORD='):
            password = line.strip().split('=')[1]
        if line.strip().startswith('POSTGRES_DB='):
            dbname = line.strip().split('=')[1]

    print(f"Detected: User={user}, Pass={password}, DB={dbname}")
    
    # Construct new URL
    new_url = f"postgresql://{user}:{password}@postgres:5432/{dbname}"
    print(f"New URL: {new_url}")

    # Second pass to replace
    for line in lines:
        if line.strip().startswith('DATABASE_URL='):
            new_lines.append(f"DATABASE_URL={new_url}\n")
        else:
            new_lines.append(line)
            
    with open('.env', 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_env()
