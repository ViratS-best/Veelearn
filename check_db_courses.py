import pymysql
import os
import sys

# Try to load from .env, but don't fail if it doesn't exist
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

AIVEN_CONFIG = {
    "charset": "utf8mb4",
    "connect_timeout": 10,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": os.getenv("AIVEN_DB", "defaultdb"),
    "host": os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "password": os.getenv("AIVEN_PASSWORD", ""),
    "read_timeout": 10,
    "port": int(os.getenv("AIVEN_PORT", "26399")),
    "user": os.getenv("AIVEN_USER", "avnadmin"),
    "write_timeout": 10,
}

def check_courses():
    try:
        connection = pymysql.connect(**AIVEN_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title FROM courses")
            courses = cursor.fetchall()
            print("--- Existing Courses ---")
            for course in courses:
                print(f"ID: {course['id']} | Title: {course['title']}")
            print("------------------------")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if not AIVEN_CONFIG["password"]:
        print("ERROR: AIVEN_PASSWORD not set")
    else:
        check_courses()
