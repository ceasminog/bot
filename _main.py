from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import urllib
import urllib.request as requests
from bs4 import BeautifulSoup  # Для обработки HTML


# global best_offers - Рекомендации
# global all_pizza - Весь асортимент пиццы
# global all_food - Весь асортимент

# gets site by url
def get_site():
    url = 'https://www.delivery-club.ru/srv/Siti_Pizza/#Voroncovskaja/'
    html = urllib.request.urlopen(url).read()
    # Теперь записываешь файл
    f = open('my_file.html', 'wb')
    f.write(html)
    f.close()


# parses site
def processing():
    print('site received')
    get_site()
    f = open('my_file.html', 'rb')
    soup = BeautifulSoup(f, 'html.parser')
    subtree = soup.script
    subtree.extract()
    food_list = soup.findAll('h3')
    price_list = soup.findAll('strong')
    for j in range(len(price_list)):
        price_list[j] = str(price_list[j]).replace('<strong><span>', '').replace(
            '</span> <span class="ptrouble">у</span></strong>', '').replace(
            '<strong id="delivery-diff">', '').replace('</strong>', '')
    pizza30_list = []
    pizza30_price = []
    count = 1
    best_var = []
    for j in range(len(food_list)):
        food_list[j] = str(food_list[j]).replace('<h3 class="product_title"><span itemprop="name">', '').replace(
            '</span></h3>', '')
        if food_list[j].count('30') == 1:
            food_list[j] = food_list[j].replace('30 см', '')
            pizza30_list.append(str(count) + ' ' + food_list[j] + ' ' + str(price_list[j]))
            pizza30_price.append(str(price_list[j]))
            best_var.append(str(price_list[j]) + ' ' + food_list[j].replace('30 см', ''))
            count += 1
        food_list[j] = '{} - {} руб. '.format(food_list[j], str(price_list[j]))
    global all_food
    all_food = 'Весь асортимент:\n {}'.format('\n'.join(food_list))
    global all_pizza
    all_pizza = 'Весь асортимент пиццы:\n {}'.format('\n'.join(pizza30_list))
    best_var.sort()
    for i in range(len(best_var)):
        a = best_var[i].split()
        a.append('- ' + a[0] + ' руб.')
        del a[0]
        best_var[i] = ' '.join(a)
    best_var = best_var[0:6]
    global best_offers
    best_offers = 'Сегодня рекомендую:\n {}'.format('\n'.join(best_var))
    f.close()
    print('site parsed')


# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# bot's commands:
'''''
/best - See best offers for today
/pizza - See full list of prices for pizza
/all - Got tired of pizza? See other offers
/pay - Chose already? Then proceed to payment
'''


def start(bot, update):
    update.message.reply_text('What do you want to command? \nClick on /best to see best offers for today.')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('read above')


def best(bot, update):
    update.message.reply_text(
        best_offers + '\n\nClick on /pizza to see all pizzas you can command\nChose already? Then proceed to payment /pay')


def pizza(bot, update):
    update.message.reply_text(
        all_pizza + '\n\nGot tired of pizza? Click on /all to see other offers.\nChose already? Then proceed to payment /pay')


def all(bot, update):
    update.message.reply_text(all_food + '\n\nChose already? Then proceed to payment /pay')


def pay(bot, update):
    update.message.reply_text(
        'Made a choise? Then go to \nhttps://www.delivery-club.ru/srv/Siti_Pizza/#Voroncovskaja/\n to command your best pizza')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    update.message.reply_text('Что-то пошло не так. Сейчас всё исправим)')
    logger.warning('Update "%s" caused error "%s"', update, error)


def invalid_command(bot, update):
    update.message.reply_text('There is no such command(')


def main():
    processing()
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("598435796:AAG82ExaA4becnKtGeko6g3DyWm_fYs15FE")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("best", best))
    dp.add_handler(CommandHandler("pizza", pizza))
    dp.add_handler(CommandHandler("all", all))
    dp.add_handler(CommandHandler("pay", pay))

    # on noncommand i.e message -  ignores  the message on Telegram
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, invalid_command))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
