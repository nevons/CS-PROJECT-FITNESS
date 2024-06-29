import openai
response = openai.ChatCompletion.create(

  api_key="",  
  model="gpt-3.5-turbo-1106",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "you are my fitness coach who will provide me a diet and exercise routine for a week in the form of two tables: diet and exercise. Each of these has days labelled.\nIn diet, you will give me food items to consume per day in the week to achieve my body goals in a tangible time period. You will list the food items along with their protein and fat in grams.\nIn exercise, you will give me a time range to exercise along with exercises and the muscle groups they target. Also provide me the amount of reps and sets to do per exercise."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I want to cut my weight from 90 kg to 75 kg. Please provide me an exercise and diet routine for a week."
        }
      ]
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)