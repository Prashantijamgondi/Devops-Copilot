
import os

def read_env():
    env = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                env[k] = v
    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"POSTGRES_USER={env.get('POSTGRES_USER', 'Not Set')}")
    print(f"POSTGRES_PASSWORD={env.get('POSTGRES_PASSWORD', 'Not Set')}")
    print(f"DATABASE_URL={env.get('DATABASE_URL', 'Not Set')}")

if __name__ == "__main__":
    read_env()
