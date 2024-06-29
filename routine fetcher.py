#routine fetcher
import openai

API_key=open('python api project key.txt','r').read()
print(API_key)
exit()

openai.api_key=API_key

def prompt():
    pass


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages = [
        #{"role": "system","content":"You are a companion of the user who helps them to achieve their body goals like weight loss and gain. You provide them with a meal plan as well as an exercise plan."}
        {"role": "user", "content" : prompt()  }])


print(response)