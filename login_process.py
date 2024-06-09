import mysql.connector as m
import webbrowser
import time

#db config
mydb=m.connect(passwd="heilhitler666",host="localhost",user="root",auth_plugin="mysql_native_password")
mycursor=mydb.cursor()

mycursor.execute("show databases;")
db_ls=mycursor.fetchall()
print(db_ls)
try:
    if ('nutripal_db',) not in db_ls:
        mycursor.execute("create database nutripal_db;")
        mycursor.execute("use nutripal_db;")
    else:
        mycursor.execute("use nutripal_db;")
except:
    print("Oops! An error occured...")

#key maker for openai
conf=input('Do you have an OpenAi account(y/n)?: ')
if conf=='y'or'Y':
    conf_1=input('Do you have an API key(y/n)?: ')
    if conf_1=='n'or'N':
        print('Having an API key is essential to use NutriPal.\n Opening the OpenAI website..... \nIt may ask you to login.\n After you are done making a key, enter it in the prompt below...')
        time.sleep(2.5)
        webbrowser.open('https://platform.openai.com/settings/profile?tab=api-keys')
        api_key=input('enter your API key: ')

#account manager
print("Log in to existing account or create a new one.....")
c1=int(input("Enter 1:Log in or 2:Create new account: "))

if c1==2:
    acc_name=input("Enter your name(no spaces in between): ")
    acc_age=int(input("Enter your age: "))
    acc_api_key=api_key

    acc_tuple=tuple(acc_api_key,acc_name,acc_age)

    mycursor.execute("create table user_%s %s ",(acc_name,acc_tuple))



mydb.close()