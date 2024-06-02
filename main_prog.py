import mysql.connector as m

#db config
mydb=m.connect(passwd="heilhitler666",host="localhost",user="root",auth_plugin="mysql_native_password")
mycursor=mydb.cursor()

mycursor.execute("show databases;")
db_ls=mycursor.fetchall()
print(db_ls)
try:
    if ('nutripal_user_db',) not in db_ls:
        mycursor.execute("create database nutripal_user_db;")
        mycursor.execute("use nutripal_user_db;")
    else:
        mycursor.execute("use nutripal_user_db;")
except:
    print("Oops! An error occured...")

def acc_code_maker():
    tb_ls=mycursor.execute("show tables;")
    code_ls=[]
    for i in tb_ls:
        mycursor.execute("select code from %s",i)


#account manager
print("Log in to existing account or create a new one............")
c1=int(input("Enter 1:Log in or 2:Create new account: "))

if c1==2:
    acc_name=input("Enter your name: ")
    acc_age=int(input("Enter your age: "))
    acc_code=acc_code_maker()
    mycursor.execute("create table user_%s () ")

mydb.close()