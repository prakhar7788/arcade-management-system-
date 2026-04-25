import mysql.connector as conn

db1 = conn.connect(host="localhost", user="root", passwd="*****")
if db1.is_connected():
    print("Connection successful")
cur1 = db1.cursor()

def createDB():
    try:
        sql1 = "create database arcade"
        cur1.execute(sql1)
        print("Database created successfully")
    except:
        print("")

createDB()

def activateDB():
    try:
        x = "use arcade "
        cur1.execute(x)
        print("Database activated")
    except:
        print("Dead")

activateDB()

def createT1():
    y = "CREATE TABLE player(playerid int(4) primary key, playername varchar(30), age int(6), gender char(1));"
    try:
        cur1.execute(y)
        print("Table created successfully")
    except:
        print("Table already exists")

createT1()

def createT2():
    z = "CREATE TABLE games(sno int(2) primary key, gamename varchar(30), price int(6));"
    try:
        cur1.execute(z)
        print("Table created successfully")
    except:
        print("Table already exists")

createT2()

def createT3():
    sql = "CREATE TABLE card_balance(playerid int(4) primary key, balance int(10));"
    try:
        cur1.execute(sql)
        print("Table created successfully")
    except:
        print("Table already exists")

createT3()

def createT4():
    sql = "CREATE TABLE transactions(transaction_id int(4) primary key AUTO_INCREMENT, playerid int(4), amount int(10), transaction_date datetime, FOREIGN KEY (playerid) REFERENCES player(playerid));"
    try:
        cur1.execute(sql)
        print("Table created successfully")
    except:
        print("Table already exists")

createT4()

def addrec1():
    try:
        playerid = int(input("Enter id number: "))
        playername = input("Enter name: ")
        age = int(input("Enter age: "))
        gender = input("Enter gender (M/F/O): ")
        balance = int(input("Enter initial card balance: "))
        h = f"insert into player values('{playerid}','{playername}','{age}','{gender}')"
        cur1.execute(h)

        cur1.execute(f"INSERT INTO card_balance(playerid, balance) VALUES ('{playerid}', '{balance}')")

        db1.commit()
        print("Record added")
    except:
        print("Record was not added")

def addrec2():
    try:
        sno = int(input("Enter serial number: "))
        gamename = input("Enter name of the game: ")
        price = int(input("Enter price of the game: "))
        j = f"insert into games values('{sno}','{gamename}','{price}')"
        cur1.execute(j)
        db1.commit()
        print("Record added")
    except:
        print("Record was not added")

def displayer():
    try:
        k = "select * from player;"
        cur1.execute(k)
        players = cur1.fetchall()
        for player in players:
            print("Player ID:", player[0])
            print("Name:", player[1])
            print("Age:", player[2])
            print("Gender:", player[3])

            cur1.execute(f"SELECT balance FROM card_balance WHERE playerid = '{player[0]}'")
            balance = cur1.fetchone()
            if balance:
                print("Card Balance:", balance[0])
            else:
                print("Card Balance: N/A")

            cur1.execute(f"SELECT SUM(amount) FROM transactions WHERE playerid = '{player[0]}'")
            total_money_used = cur1.fetchone()[0]
            if total_money_used:
                print("Total Money Used:", total_money_used)
            else:
                print("Total Money Used: N/A")

            print("----------")
    except:
        print("Table could not be displayed")

def play_basketball(player_id):
    try:
        cur1.execute(f"SELECT * FROM player WHERE playerid = '{player_id}'")
        player = cur1.fetchone()
        if not player:
            print("Player not found.")
            return

        cur1.execute(f"SELECT balance FROM card_balance WHERE playerid = '{player_id}'")
        balance = cur1.fetchone()
        if not balance or balance[0] < 150:
            print("Insufficient balance to play basketball.")
            return

        new_balance = balance[0] - 150
        cur1.execute(f"UPDATE card_balance SET balance = '{new_balance}' WHERE playerid = '{player_id}'")
        db1.commit()

        cur1.execute(f"INSERT INTO transactions(playerid, amount, transaction_date) VALUES ('{player_id}', '-150', NOW())")
        db1.commit()

        print("Basketball played. 150 rupees deducted.")
    except:
        print("An error occurred while playing basketball.")

print("_____________________________Arcade Management System________________________________________")
print("1: Add records in player table")
print("2: Add records in game table")
print("3: Display player table and play basketball")
ch = int(input("Enter choice (1/2/3): "))

if ch == 1:
    addrec1()
elif ch == 2:
    addrec2()
elif ch == 3:
    displayer()
    player_id = input("Enter the player ID to play basketball: ")
    play_basketball(player_id)
else:
    print("Invalid choice")
