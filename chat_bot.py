import dotenv
import os
dotenv.load_dotenv()
from openai import OpenAI
import tiktoken
import time

class chat_bot:
    def __init__(self):
        self.llm=OpenAI(api_key=os.getenv('GROQ_API_KEY'),base_url='https://api.groq.com/openai/v1')
        self.messages=[{'role':'system','content':'You are a helpful assistant.Your name is Neon_bot.Introduce yourself in the first message.Give short and helful answers'}]
        self.total_tokens=0
        self.input_tokens=0
        self.output_tokens=0
        self.iteration = 0
    def trim_messages(self,max_number=4):
        if len(self.messages)<max_number:
            return
        system_messages=[m for m in self.messages if m['role']=='system']
        other_messages=[m for m in self.messages if m['role']!='system']
        trimmed_messages=other_messages[-max_number:]
        self.messages=[*system_messages,*trimmed_messages]
    def summarize_messages(self):
        if self.iteration%5!=0:
            return
        system_messages=[m for m in self.messages if m['role']=='system']
        other_messages=[m for m in self.messages if m['role']!='system']
        early_messages,last_messages=(other_messages[0:5],other_messages[5:])
        response=self.llm.chat.completions.create(model='openai/gpt-oss-120b',messages=[{'role':'system','content':'summarize these messages concisely,keeping key facts and descion'},*early_messages])
        summarized_messages={'role':'system','content':f''' The summary of first 5 early messages:{response.choices[0].message.content}'''}
        self.messages= [*system_messages,summarized_messages,*last_messages]
    def bot(self,message):
        self.messages.append({'role':'user','content':message})
        response=self.llm.chat.completions.create(model='openai/gpt-oss-120b',messages=self.messages,stream=True)
        response_text=''
        for chunk in response:
            if chunk.choices:
                delta=chunk.choices[0].delta.content
                if delta:
                    print(delta,end='',flush=True)
                    response_text+=delta
                    time.sleep(0.05)
            if chunk.usage:
                self.messages.append({'role':'assistant','content':response_text})
                self.total_tokens=self.total_tokens+chunk.usage.total_tokens
                self.input_tokens=self.total_tokens+chunk.usage.prompt_tokens
                self.output_tokens=self.total_tokens+chunk.usage.completion_tokens
        print()
       
        self.trim_messages()
        # self.summarize_messages()
        return response_text
    def chat(self):
     encoding=tiktoken.get_encoding('cl100k_base')
     while True:
      self.iteration+=1
      user_input=input('Ask Someting...:(type "q" to terminate):').strip().lower()
      if user_input=='q':
          print("Good Luck")
          break
          #Length of token
      token_cnt=len(encoding.encode(user_input))
      print(f'Consumed tokens:{token_cnt}')
      #How tokens are send as numeric values
      print(encoding.encode(user_input))
      self.bot(user_input)
    #   print(bot_answer) 
    def report(self):
        for message in self.messages:
            print(message)
        print(f'Consumed Tokens:{self.total_tokens}')
        print(f'${(self.input_tokens*0.04+self.output_tokens*0.08)/1_000_000}')
def main():
    BotChat=chat_bot()
    BotChat.chat()
    BotChat.report()
if __name__=="__main__":
    main()