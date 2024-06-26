import openai
import os
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime
import requests
import json


load_dotenv()

news_api_key = os.environ.get("NEWS_API_KEY")
client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"


def get_news(topic):
    url = (
        f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}&pageSize=5"
    )

    try:
        response = requests.get(url)
        if response.status_code == 200:
            news = json.dumps(response.json(), indent=4)
            news_json = json.loads(news)

            data = news_json

            # Variablen setzen
            status = data["status"]
            total_results = data["totalResults"]
            articles = data["articles"]
            final_news = []

            # Durch alle Infos loopen
            for article in articles:
                source_name = article["source"]["name"]
                author = article["author"]
                title = article["title"]
                description = article["description"]
                url = article["url"]
                content = article["content"]
                title_description = f"""
                   Title: {title}, 
                   Author: {author},
                   Source: {source_name},
                   Description: {description},
                   URL: {url}
            
                """
                final_news.append(title_description)

            return final_news
        else:
            return []

    except requests.exceptions.RequestException as e:
        print("Error occured during API Request", e)



   
def main():
        news = get_news("bitcoin")
        print(news)


class AssistantManager:
     thread_id = None
     assistant_id = None

     def __init__(self, model: str = model):
          self.client = client
          self.model = model
          self.assistant = None,
          self.thread = None,
          self.run = None
          self.summary = None
          
          if AssistantManager.assistant_id:
               self.assistant_id = self.client.beta.assistants.retrieve(
                    assistant_id=AssistantManager.assistant_id
               )
          if AssistantManager.thread_id:
               self.thread_id = self.client.beta.threads.retrieve(
                    thread_id=AssistantManager.thread_id
               )
     def create_assistant(self, name, instructions, tools):
          if not self.assistant:
               assistant_obj = self.client.beta.assistants.create(
                    name=name,
                    instructions=instructions,
                    tools=tools,
                    model=self.model
               )
               AssistantManager.assistant_id = assistant_obj.id
               self.assistant = assistant_obj
               print(f"AssisID:::: {self.assistant.id}")
  
     def create_thread(self):
          if not self.thread:
               thread_obj = self.client.beta.thread.create()
               AssistantManager.thread_id = thread_obj.id
               self.thread = thread_obj
               print(f"ThreadID::: {self.thread_id}")

     def add_message_to_thread(self, role, content):
            if self.thread:
                self.client.beta.thread.messages.create(
                    thread_id=self.thread.id,
                    role=role,
                    content=content
                )

     def run_assistant(self,instructions):
          if self.thread and self.assistant:
               self.run = self.client.beta.threads.runs.create(
                    thread_id=self.thread.id,
                    assistant_id=self.assistant.id,
                    instructions=instructions
                )
     def process_message(self):
          if self.thread:
               messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id
               )
               summary = []
               last_message = messages.data[0]
               role = last_message.role
               response = last_message.content[0].text.value

               

          
               

     
     

if __name__ == "__main__":
    main()


