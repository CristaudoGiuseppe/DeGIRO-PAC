from os import write
import degiroapi
from degiroapi.product import Product
from degiroapi.order import Order
from degiroapi.utils import pretty_json
from datetime import date, datetime, timedelta
from discord_webhook import DiscordWebhook, DiscordEmbed
import matplotlib.pyplot as plt
import json, logging, csv, random
import sys

logger = logging.getLogger('')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('files/log.log', mode='a')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

import sys, ipdb, traceback

def info(type, value, tb):
    traceback.print_exception(type, value, tb)
    ipdb.pm()

#sys.excepthook = info

class DeGIRO_PAC():
    
    orders = {}
    degiro = degiroapi.DeGiro()
    
    def __init__(self):
        try:
            self.config = json.load(open('files/config.json'))
            logging.info('[' + str(date.today()) + '][CONFIG FILE SUCCESSFULLY OPENED]')
            self.username = self.config['account'][0]['username']
            self.password = self.config['account'][0]['password']
            self.amount = int(self.config['amount'])
            if self.username == "" or self.password == "":
                logging.warning('[' + str(date.today()) + '][MISSING USERNAME OR PASSWORD FROM CONFIG FILE]')
                self.send_webhook('ERROR', 'MISSING USERNAME OR PASSWORD FROM CONFIG FILE', 'ff0000')
                exit(-1)
            if self.config['webhook'] != "":
                self.webhook = DiscordWebhook(url=self.config['webhook'])
            else:
                logging.warning('[' + str(date.today()) + '][WEBHOOK NOT AVAILABLE]')
        except:
            logging.warning('[' + str(date.today()) + '][ERROR OPENING CONFIG FILE]')
            
    def login(self): # log into your account
        self.degiro.login(self.username, self.password)
        
    def get_product_data(self): # get info from the config file and update a dict with the wty to buy
        for product in self.config['ETF']:
            # check the amount dedicated to each ETF
            m = float(self.amount * float(product['percentile']) / 100)
            # get actual price
            realprice = self.degiro.real_time_price(str(product['id']), degiroapi.Interval.Type.One_Day)
            # get the amount of share to buy in respect to real time price
            to_buy = int(m/realprice[0]['data']['lastPrice'])
            # update the dict
            self.orders.update({product['id']:to_buy})
        # amount cash held on the account
        self.amount_on_broker  = float(str(self.degiro.getdata(degiroapi.Data.Type.CASHFUNDS)[0]).split(" ")[1])
        
    def buy_product(self):
        if self.amount_on_broker > self.amount:
            for order in self.orders:
                self.degiro.buyorder(Order.Type.MARKET, order, 3, int(self.orders.get(order)))
                logging.info('[' + str(date.today()) + '][BUY ORDER][ID: ' + order + '][QUANTITY: ' + str(self.orders.get(order)) + ']')

            # check if orders were successfull
            orders = self.degiro.orders(datetime.now() - timedelta(days = 1), datetime.now())
            i = len(self.onfig['ETF'])
            while (i != 0):
                if orders[-i]['status'] == 'CONFIRMED':
                    productID = orders[-i]['productId']
                    amountBought = orders[-i]['size']
                    name = self.degiro.product_info(productID)['name']
                    price = orders[-i]['price']
                    description = name + ' x ' + str(amountBought)
                    
                    logging.info('[' + str(date.today()) + '][ORDER CONFIRMED][ID: ' + productID + '][NAME: ' + name + '][QUANTITY: ' + str(amountBought) + ']')
                    with open('outcome/order_recap.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([str(date.today()), productID, name, amountBought, price, price * amountBought]) 
                    self.send_webhook('ORDER CONFIRMED', description, '008000')
                else:
                    logging.warning('[' + str(date.today()) + '][ORDER NOT CONFIRMED]')
                    self.send_webhook('ORDER FAILED',  orders[-i]['productId'], 'ff0000')
                i -= 1
        else:
            logging.warning('[' + str(date.today()) + '][NOT ENOUGHT MONEY TO START BUYING]')
            self.send_webhook('FAILED BUYING',  'NOT ENOUGHT MONEY TO START BUYING', 'ff0000')
            
    def portfolio_update(self):
        labels = []
        sizes = []
        colors = []
        portfolio = self.degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)
        with open('outcome/portfolio_status.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for data in portfolio:
                if data['id'] != 'FLATEX_EUR':
                    productID = data['id']
                    name = self.degiro.product_info(productID)['name']
                    writer.writerow([str(date.today()), productID, name, data['size'], data['value'], data['value']/data['price']])
                    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                    labels.append(name)
                    sizes.append(float(data['value']))
                    colors.append(color)
                
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.savefig('outcome/portfolio_status.png')
        #plt.show()
        
    def logout(self): # logout from de giro account
        self.degiro.logout() 
        
    def send_webhook(self, title, descriprion, color):
        embed = DiscordEmbed(title = title, description = descriprion, color = color)
        #embed.set_author(name='Criss', url='https://github.com/CristaudoGiuseppe')
        embed.set_footer(text='DEGIRO PAC V. 0.1')
        if hasattr(self, 'webhook'):
            self.webhook.add_embed(embed)
            try:
                self.webhook.execute()
            except:
                logging.warning('[' + str(date.today()) + '][ERROR SENDING WEBHOOK]')
        else:
                logging.warning('[' + str(date.today()) + '][ERROR SENDING WEBHOOK]')
            
    def run(self):
        self.login()
        self.get_product_data()
        self.buy_product()
        self.portfolio_update()
        self.logout()



PAC = DeGIRO_PAC()
PAC.run()


    










                 
                    




