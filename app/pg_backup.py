import subprocess
from datetime import datetime

CONTAINER_NAME = "pollux_postgres"   # 👈 your postgres container name
DB_NAME = "pollux_db"
DB_USER = "pollux_user"

def export_db():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"safe_backup_{timestamp}.sql"

        command = [
            "docker", "exec", "-t",
            CONTAINER_NAME,
            "pg_dump",
            "-U", DB_USER,
            "-d", DB_NAME,
            "--column-inserts"
        ]

        # Write output to file
        with open(output_file, "w", encoding="utf-8") as f:
            subprocess.run(command, stdout=f, check=True)

        print(f"✅ Backup created: {output_file}")

    except subprocess.CalledProcessError as e:
        print("❌ Export failed:", e)

if __name__ == "__main__":
    export_db()