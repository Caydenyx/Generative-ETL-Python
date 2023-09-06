import pandas as pd
import requests
import json
import openai

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'
ler_csv = pd.read_csv('clientes.csv')
user_ids = ler_csv['UserID'].tolist()

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

usuarios = [user for id in user_ids if (user := get_user(id)) is not None]

# openai_api_key = 'COLOQUE SUA KEY AQUI'
 
openai.api_key = openai_api_key

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model= "gpt-3.5-turbo",
    messages=[
      {
          "role": "system",
          "content": "Você é um Consultor de Vendas da Mitsubishi ."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para o {user['name']} Sobre os novos carros da Mitsubishi 2023 Manaus e principalmente sobre a nova L200 (máximo de 100 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')

for user in usuarios:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://static-00.iconduck.com/assets.00/mitsubishi-icon-2048x1756-rqbhpxte.png",
      "description": news
  })
def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in usuarios:
  success = update_user(user)
  print(f"ÚSUARIO {user['name']} ATUALIZOU? {success}!")