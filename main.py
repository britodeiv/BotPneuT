import schedule
import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

# Configurações do bot telegram
TELEGRAM_BOT_TOKEN = '7241425492:AAHkGaR2hPRNv8UTNzDgML6PLN5N5LczdnQ'
CHAT_ID = '1444306011'

# Preço limite definido para alertas
PRECO_LIMITE = 180.00

# Função para fazer scraping dos sites
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.find_all('div', class_='promo')
    results = []
    for item in items:
        title = item.find('h2').text.strip()
        price = item.find('span', class_='price').text.strip()

        # Conversão de preço para float
        price_float = float(price.replace('200,00').replace('180,00').replace(',', '.').strip())
        if price_float <= PRECO_LIMITE:
            results.append(f"{title}: R$ {price}")
    return results

# Enviar mensagem no telegram
def send_telegram_message(message):
    bot = Bot(TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

# Verificar promoções em todos os sites
def check_promotions():
    all_promotions = []
    for site in websites:
        promotions = scrape_website(site)
        all_promotions.extend(promotions)
    return all_promotions

# Enviar alerta
def check_and_alert(): 
    promotions = check_promotions()
    if promotions:
        message = "\n".join(promotions)
    else:
        message = "Nenhuma promoção encontrada :/."
    send_telegram_message(message)

# Agendar verificações periódicas
def schedule_jobs():
    schedule.every().day.at("08:00").do(check_and_alert)
    schedule.every().day.at("12:00").do(check_and_alert)
    schedule.every().day.at("15:20").do(check_and_alert)
    schedule.every().day.at("19:00").do(check_and_alert)
    schedule.every().day.at("22:00").do(check_and_alert)

    while True:
        schedule.run_pending()
        time.sleep(1)

        # Lista de websites pra consulta
websites = [
    'https://shopee.com.br/search?keyword=pneu%20aro%2014',
    'https://www.magazineluiza.com.br/busca/pneu+aro+14+carro/',
    'https://www.americanas.com.br/busca/pneu-aro-14-carro',
    'https://www.casasbahia.com.br/pneu-aro-14/b',
    'https://lista.mercadolivre.com.br/pneu-de-carro-aro-14',
    'https://www.carrefour.com.br/pneus/aro-14'
]


# Inicializar e rodar o bot do Telegram
def main():
    schedule_jobs()

if __name__ == '__main__':
    main()
