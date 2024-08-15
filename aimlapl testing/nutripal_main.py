import mysql.connector as m
import requests
import json
import random
import os
import streamlit as st

#fix calories in prompt, veg and non veg option, preferences(ability to edit table)

API_KEY = 'a197bc47cee847cab2025571bfd8a501'

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
        cursor.execute("INSERT INTO users (acc_name, acc_age) VALUES (%s, %s);", (name, age))
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
    url = "https://api.aimlapi.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are my fitness coach who will provide me a diet routine for a week in the form of a table. Each of these has days labelled.\nIn diet, you will give me food items to consume per day in the week to achieve my body goals in a tangible time period. You will list the food items along with their protein and fat in grams in a simple format, without any extra text."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 256
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            text = result['choices'][0]['message']['content']
            st.markdown(f"```\n{text}\n```", unsafe_allow_html=True)
            if not os.path.exists("AIMLAPI"):
                os.mkdir("AIMLAPI")
            n = random.randint(1, 999999)
            with open(f"AIMLAPI/prompt-{n}.txt", "w") as f:
                f.write(text)
        else:
            st.error("Unexpected response format.")
    except requests.RequestException as e:
        if e.response and e.response.status_code == 429:
            st.error("Rate limit exceeded. Please wait and try again later.")
        else:
            st.error(f"Request failed: {e}")
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
        if st.button("Get Diet Plan"):
            if pref == "Cut":
                ai_prompt = f"I want to decrease my weight from {weight} to {goal} in a tangible time period. Give me a table for diet. In the table, list Indian food items along with their protein and fat in grams. The table has to be prepared as a weekly schedule. Also provide the expected amount of time in months and days. Do not put any text before or after the table, just the table itself."
            elif pref == "Bulk":
                ai_prompt = f"I want to increase my weight from {weight} to {goal} in a tangible time period. Give me a table for diet. In the table, list Indian food items along with their protein and fat in grams. The table has to be prepared as a weekly schedule. Also provide the expected amount of time in months and days. Do not put any text before or after the table, just the table itself."
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
