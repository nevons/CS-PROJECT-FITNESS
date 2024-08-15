#a197bc47cee847cab2025571bfd8a501

import csv
import openai
import random



system_content = "you are my fitness coach who will provide me a diet routine for a week in the form of a table. Each of these has days labelled.\nIn diet, you will list Indian food items to consume per day in the week to achieve my body goals in a tangible time period. You will list the food items along with their protein and fat in grams."
weight=input("Enter your current weight: ")
goal=input("Enter your desired weight: ")
user_content=f"I want to decrease my weight from {weight} to {goal} in a tangible time period. give me a table for diet. in the table for food list the Indian food items along with their protein and fat in grams. the table has to be prepared as a weekly schedule. also provide the expected amount of time in months and days. Do not put any text before or after the table, just the table itself."


client = openai.ChatCompletion.create(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    api_key="sk-ag4S2pLveRZn4OMjy9vIPSSFTRsFqoCW-UKfBCZBovT3BlbkFJftilpX0RNDk0XpdD1zisZ1_0mj6xwJHRLGPKHnDYgA",
    base_url="https://api.aimlapi.com",
)

chat_completion = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages=[
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ],
    temperature=0.7,
    max_tokens=128,
)

response = chat_completion.choices[0].message.content

n=random.randint(1,999999)
with open(f"prompt-{n}.csv","w") as f:
    csv.writer(response,f)

#print("AI/ML API:\n", response)