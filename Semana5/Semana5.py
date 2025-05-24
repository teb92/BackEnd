import psycopg2


connection = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="postgres",
    dbname="postgres",
)
print("Connected to the database")

cursor = connection.cursor()
cursor.execute("SELECT id, full_name, email, password FROM lyfter_duad.users;")

print("Query executed successfully")

results = cursor.fetchall()
print(results)


