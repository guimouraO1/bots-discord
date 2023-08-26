import requests
from bs4 import BeautifulSoup
import discord

# Função para fazer a requisição HTTP e obter a previsão do tempo
def make_request(cidade):
    # api do site openweather
    api_key = ''
    city_name = cidade
    link = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&lang=pt_br'

    request = requests.get(link)
    requisicao_dic = request.json()

    descricao = requisicao_dic['weather'][0]['description']
    temperatura = requisicao_dic['main']['temp'] - 273.15
    
    return descricao, temperatura

# Substitua 'seu_token_aqui' pelo token real do seu bot - - --  token discord
TOKEN = ''

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
        
        conteudo = l_conteudo
        cidade = conteudo.replace('!tempo ', '')
        
        try:
            descricao, temperatura  =  make_request(cidade)
            nome_usuario = message.author.display_name
            await message.channel.send(f'Olá, {nome_usuario}\nA previsão do tempo da cidade {cidade} \nDescrição: {descricao}\nTemperatura: {temperatura:.2f}°C')
        except:
            nome_usuario = message.author.display_name
            await message.channel.send(f'Olá, {nome_usuario}\nA previsão do tempo da cidade {cidade} não é aceita, sentimos muito :(')
    
client.run(TOKEN)
