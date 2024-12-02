import mysql.connector as m
import random
import os
import streamlit as st
import openai

# Your OpenRouter API Key
API_KEY = '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'

def initialize_db():
    db = m.connect(passwd="heilhitler666", host="localhost", user="root", auth_plugin="mysql_native_password")
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES;")
    db_list = cursor.fetchall()
    if ('nutripal_db',) not in db_list:
        cursor.execute("CREATE DATABASE nutripal_db;")
    cursor.execute("USE nutripal_db;")
    cursor.execute("SHOW TABLES;")
    table_list = cursor.fetchall()
    if ('users',) not in table_list:
        cursor.execute("""
            CREATE TABLE users (
                acc_name VARCHAR(20) PRIMARY KEY,
                acc_age INT NOT NULL
            );
        """)
    return db, cursor

def user_exists(cursor, name):
    cursor.execute("SELECT * FROM users WHERE acc_name = %s;", (name,))
    return cursor.fetchone() is not None

def create_account(cursor, db, name, age):
    if user_exists(cursor, name):
        st.error("Account with this name already exists!")
    else:
        cursor.execute("INSERT INTO users (acc_api_key,acc_name, acc_age) VALUES (%s,%s, %s);", (API_KEY,name, age))
        db.commit()
        st.success("Account created successfully! Welcome!...")

def login_account(cursor, name):
    if user_exists(cursor, name):
        st.success('Welcome, ' + name + '!')
        return True
    else:
        st.error('Account not found!')
        return False

def ai(prompt):
    from openai import OpenAI
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY,
    )
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are my fitness coach who will provide me a diet routine for a week in the form of a table. Each of these has days labelled.\nIn diet, you will give me food items to consume per day in the week to achieve my body goals in a tangible time period. You will list the food items along with their protein and fat in grams in a simple format, without any extra text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        text = response.choices[0].message.content
        st.markdown(f"```\n{text}\n```", unsafe_allow_html=True)
        if not os.path.exists("AIMLAPI"):
            os.mkdir("AIMLAPI")
        n = random.randint(1, 999999)
        with open(f"AIMLAPI/prompt-{n}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    st.title("Account Management")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    db, cursor = initialize_db()

    if st.session_state.logged_in:
        st.subheader("Dashboard")
        pref = st.radio("What is your body goal:", ("Cut", "Bulk"))
        weight = st.text_input("Enter your current weight: ")
        goal = st.text_input("Enter your desired weight: ")
        veg_diet_pref=st.checkbox("Vegetarian")
        if st.button("Get Diet Plan"):
            if pref == "Cut":
                if veg_diet_pref==True:
                    ai_prompt = f"I want to decrease my weight from {weight} to {goal} in a tangible time period. Give me a table for diet. In the table, list Indian food items along with their protein and fat in grams. The table has to be prepared as a weekly schedule. Also provide the expected amount of time in months and days. Do not put any text before or after the table, just the table itself. Only give vegetarian foods, exclude non-vegetarian foods."
                else:
                    ai_prompt = f"I want to decrease my weight from {weight} to {goal} in a tangible time period. Give me a table for diet. In the table, list Indian food items along with their protein and fat in grams. The table has to be prepared as a weekly schedule. Also provide the expected amount of time in months and days. Do not put any text before or after the table, just the table itself. Include non-vegetarian foods alongside vegetarian foods."
            elif pref == "Bulk":
                if veg_diet_pref==True:
                    ai_prompt = f"I want to decrease my weight from {weight} to {goal} in a tangible time period. Give me a table for diet. In the table, list Indian food items along with their protein and fat in grams. The table has to be prepared as a weekly schedule. Also provide the expected amount of time in months and days. Do not put any text before or after the table, just the table itself. Only give vegetarian foods, exclude non-vegetarian foods."
                else:
                    ai_prompt = f"I want to decrease my weight from {weight} to {goal} in a tangible time period. Give me a table for diet. In the table, list Indian food items along with their protein and fat in grams. The table has to be prepared as a weekly schedule. Also provide the expected amount of time in months and days. Do not put any text before or after the table, just the table itself. Include non-vegetarian foods alongside vegetarian foods."
                
            else:
                st.error("Invalid input")
                return
            ai(ai_prompt)
    else:
        option = st.radio("Choose an option", ("Log in", "Create new account"))

        if option == "Create new account":
            acc_name = st.text_input("Enter your name (no spaces in between): ")
            acc_age = st.number_input("Enter your age:", min_value=1)
            if st.button("Create Account"):
                create_account(cursor, db, acc_name, acc_age)

        elif option == "Log in":
            acc_name = st.text_input('Enter your name:')
            if st.button("Log In"):
                if login_account(cursor, acc_name):
                    st.session_state.logged_in = True

    db.close()

if __name__ == "__main__":
    main()