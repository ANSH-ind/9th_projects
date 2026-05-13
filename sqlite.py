import sqlite3 

conn = sqlite3.connect("database_01.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS user_data(
name VARCHAR(15),
email VARCHAR(18),
user_name VARCHAR(15)
)""")
conn.commit()

def add_user(name,email,user_name):
	cursor.execute("""INSERT INTO user_data (name,email,user_name) VALUES (?,?,?)""",(name,email,user_name))
	conn.commit()
	return f"user {name} added successfully"
	
def show_users_data():
	cursor.execute("""SELECT * FROM user_data""")
	row = cursor.fetchall()
	for r in row:
		print(f"\n{list(r)}")
		
while True:
	command = input("command: ")
	if command.lower()=="add user":
		name = input("enter name: ")
		email = input("enter email: ")
		user_name = input("enter user name: ")
		add_user(name=name,email=email,user_name=user_name)
	elif command.lower() == "see user":
		show_users_data()
	elif command.lower()=="exit":
		break
	else:
		print("invalid command")
		
