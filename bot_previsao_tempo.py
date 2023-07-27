import requests
from bs4 import BeautifulSoup
import discord


def make_request():
  url = "https://www.cpa.unicamp.br/cepagri/previsao"

  try:
    # Faz a solicitação GET
    response = requests.get(url)

    # Verifica se a solicitação foi bem-sucedida (status code 200)
    if response.status_code == 200:

      # Obtemos o conteúdo da página
      page = response.text

      # Utilizando o BeautifulSoup para analisar o HTML
      soup = BeautifulSoup(page, "html.parser")

      # Procurar a div com a classe "hoje active" para obter o conteúdo dentro dela
      hoje_div = soup.find("div", class_="hoje active")

      # Extrai o conteúdo dentro da div "hoje active"
      conteudo_hoje = hoje_div.text.strip()

      # Remove os espaços em branco e a formatação
      conteudo_hoje = conteudo_hoje.replace('\n',
                                            '').replace('\r', '').replace(
                                                '\t', '').strip()

      # Separa cada elemento em uma lista
      lista_elementos = conteudo_hoje.split()

      # data de hoje
      data_hoje = " ".join(lista_elementos[0:2])

      # Previsão do tempo
      previsao = " ".join(lista_elementos[4:])

      minima = " ".join(lista_elementos[3])
      minima = minima.replace(' ', '')

      maxima = " ".join(lista_elementos[2])
      maxima = maxima.replace(' ', '')

      previsao_total = data_hoje + '\n' + 'Máxima: ' + f'**{maxima}**' + '\n' + 'Mínima: ' + f'**{minima}**' + '\n' + previsao
      # Pritnado Previsão do tempo

      return str(previsao_total)

    else:
      print(f"Erro na solicitação. Status code: {response.status_code}")

  except requests.exceptions.RequestException as error:
    return print(f"Erro na solicitação: {error}")


make_request()

# Substitua 'seu_token_aqui' pelo token real do seu bot
TOKEN = 'Coloque o token aqui'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f'{client.user} está online!')


@client.event
async def on_message(message):

  conteudo = message.content
  l_conteudo = conteudo.lower()

  if message.author == client.user:
    return

  if l_conteudo.startswith('!tempo'):
    previsao_tempo = make_request()
    await message.channel.send(
        f'Olá, @{message.author} \nA previsão do tempo é  \n{previsao_tempo}')


client.run(TOKEN)
