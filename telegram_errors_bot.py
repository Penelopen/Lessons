from telegram.ext import Application, CommandHandler, MessageHandler
from telegram import Update
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text("Привет! Тут будут только сообщения об ошибках")

    while True:
        a = input('Введите первое число: ')
        if a in ('exit', 'учше'):
            break
        b = input('Введите второе число: ')
        if b in ('exit', 'учше'):
            break

        error_text = ''
        try:
            print(f'Результат: {int(a) / int(b)}')
        except ZeroDivisionError:
            error_text = 'Ошибка: Деление на ноль!'
            await update.message.reply_text(error_text)
        except ValueError:
            error_text = 'Ошибка ввода'
            await update.message.reply_text(error_text)
        except:
            error_text = 'Ошибка'
            await update.message.reply_text(error_text)
        print(error_text)

def main():
    token = "8397313311:AAGMVBmFuUqfRvUSGif7g3RoNLdkMwlfqy4"
    bot = Application.builder().token(token).build()
    bot.add_handler(CommandHandler("start", start))
    bot.run_polling()

if __name__ == '__main__':
    main()
