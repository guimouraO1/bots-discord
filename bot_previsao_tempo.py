import requests
from bs4 import BeautifulSoup
import discord

def make_request():
    url = "https://www.cpa.unicamp.br/cepagri/previsao"

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        hoje_div = soup.find("div", class_="hoje active") or soup.find("div", class_="amanha active") or soup.find("div", class_="depois active")

        if hoje_div:
            lista_elementos = hoje_div.text.strip().split()
            data_hoje = " ".join(lista_elementos[0:2])
            minima, maxima, previsao = lista_elementos[3], lista_elementos[2], " ".join(lista_elementos[4:])
            return f"{data_hoje}\nMáxima: **{maxima}**\nMínima: **{minima}**\n{previsao}"

        else:
            raise Exception("Erro, não há dias disponíveis")

    except requests.exceptions.RequestException as error:
        print(f"Erro na solicitação: {error}")

    except Exception as error:
        print(f"Ocorreu um erro: {error}")

    return None

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
    # Verifica se o autor da mensagem é o bot
    if message.author == client.user:
        return

    conteudo = message.content
    l_conteudo = conteudo.lower()

    if l_conteudo.startswith('!tempo'):
        previsao_tempo = make_request()
        nome_usuario = message.author.display_name
        await message.channel.send(
            f'Olá, {nome_usuario}\nA previsão do tempo é \n{previsao_tempo}')

client.run(TOKEN)
