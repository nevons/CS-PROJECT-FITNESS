import mysql.connector as m
import webbrowser
import time

#db config
mydb=m.connect(passwd="heilhitler666",host="localhost",user="root",auth_plugin="mysql_native_password")
mycursor=mydb.cursor()

mycursor.execute("show databases;")
db_ls=mycursor.fetchall()
try:
    if ('nutripal_db',) not in db_ls:
        mycursor.execute("create database nutripal_db;")
        mycursor.execute("use nutripal_db;")
    else:
        mycursor.execute("use nutripal_db;")
except:
    print("Oops! An error occured...")

mycursor.execute('show tables;')
tb_ls=mycursor.fetchall()

if ('users',) not in tb_ls:
    mycursor.execute("create table users (acc_api_key varchar(100) primary key ,acc_name varchar(20) not null ,acc_age int not null);")
else:
    pass

def api_key_getter():
    global apikey
    print('Having an API key is essential to use NutriPal.\n Opening the OpenAI API key maker website..... \nIt may ask you to login.\n After you are done making a key, enter it in the prompt below...')
    print('Store your key in the same folder as NutriPal as you need it to log in...')
    time.sleep(2.5)
    webbrowser.open('https://platform.openai.com/settings/profile?tab=api-keys')
    api_key=input('enter your API key: ')
    return apikey

#account manager
print('---------ACCOUNTS-----------')
print("Log in to existing account or create a new one.....")
c1=int(input("Enter 1: Log in or 2: Create new account: "))

if c1==2:
    acc_name=input("Enter your name(no spaces in between): ")
    acc_age=int(input("Enter your age: "))
    #key maker for openai
    apikey=''
    conf=input('Do you have an OpenAI account(y/n)?: ')
    if conf=='y'or conf=='Y':
        conf_1=input('Do you have an API key(y/n)?: ')
        
        if conf_1=='n'or conf_1=='N':
            apikey=api_key_getter()
        elif conf_1=='y' or conf_1=='Y':
            apikey=input('enter your API key: ')
        else:
            print('Invalid input.')

    elif conf=='n'or conf=='N':
        print('Having an OpenAI account is mandatory to use NutriPal.\nRedirecting to OpenAI website...')
        print('After creating account, come back here.')
        time.sleep(2)
        webbrowser.open('https://platform.openai.com/signup')

        time.sleep(6)
        print('Lastly, you require an OpenAI API key.')
        apikey=api_key_getter()

    else:
        print('Invalid input.')
    acc_api_key=apikey

    mycursor.execute("insert into users values (%s,%s,%s);",(acc_api_key,acc_name,acc_age))
    mydb.commit()

elif c1==1:
    key_login=input('Enter your API key: ')
    mycursor.execute("select * from users")
    us_ls=mycursor.fetchall()

    try:
        for i in us_ls:
            if i[0]==key_login:
                print('Welcome,'+i[1]+'!')
            else:
                print('Account not found!')

    except:
        print('Oops! Something went wrong...')

else:
    print('Invalid option.')
mydb.close()