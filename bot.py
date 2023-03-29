#importamos el token 
from config import * 
#manejo de API de Telegram 
import telebot
from telebot.types import ReplyKeyboardRemove
import requests
from bs4 import BeautifulSoup


#instanciar el bot de telegram 
bot= telebot.TeleBot(TOKEN)
ususarios ={}


#repuestas a comandos
@bot.message_handler(commands=["start", "ayuda", "help"])
def cmd_start(message):
    #username = message.chat.username
    username = message.from_user.username
    bot.reply_to(message, f"Hola @{username}! Bienvenido a EstaGen!")
    markup = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Usa el comando /buscar para hacer una consulta, referente a conceptos en el área de las estadísticas", reply_markup=markup)
    
    
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Bienvenida"),
        telebot.types.BotCommand("/buscar", "Pregunta"),
        
    ])


@bot.message_handler(commands=['buscar'])
def cmd_buscar(message):
    comando = message.text.split()[0]
    texto_buscar = " ".join(message.text.split()[1:])
    if not texto_buscar:
        if comando == '/busqueda': 
            texto= 'Debe introducir una búsqueda.\n'
            texto+= f'Ejemplo: <code>{comando} búsqueda</code>'
            bot.send_message(message.chat.id, texto, parse_mode="html")
        else:
            bot.send_message(message.chat.id, "Comando no reconocido, debe introducir una búsqueda con este formato /buscar búsqueda. Ejemplo /buscar moto")  # or replace with custom error message
        return 1
    else:
        print(f'Buscando en Economipedia: "{texto_buscar}"')
        url = f'https://economipedia.com/?s={texto_buscar.replace(" ", "+")}'
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36" 
        headers ={"user-agent": user_agent}
        #WEBSCRAPING
        # Enviar una petición HTTP GET a la URL especificada
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            # Cargar el contenido HTML de la respuesta en un objeto BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Buscar el elemento que contiene la definición
            definition = soup.find("div", {"class": "entry-content"})
            if definition is None:
                # Si no se encuentra la definición, enviar un mensaje al usuario
                bot.send_message(message.chat.id, text="Lo siento, no encontré información para esa búsqueda.")
            else:
                # Extraer el texto de la definición
                definition_text = definition.get_text()
                # Enviar la definición como respuesta a una consulta de un usuario
                bot.send_message(message.chat.id, text=definition_text)
                #bot.send_message(message.chat.id, href)
        except requests.exceptions.HTTPError as errh:
            print("Error HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
        except requests.exceptions.Timeout as errt:
            print("Error de tiempo de espera:", errt)
        except requests.exceptions.RequestException as err:
            print("Error:", err)


if __name__ == '__main__':
    print('Bot Iniciado')
    bot.infinity_polling()

