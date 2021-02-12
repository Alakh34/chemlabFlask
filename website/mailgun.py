import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


def sign_up_email(user):
    api_key = os.getenv('mailgun_api')
    return requests.post(
        "https://api.eu.mailgun.net/v3/alakh.codes/messages",
        auth=("api", api_key),
        data={"from": "Chemlab <chemlab@alakh.codes>",
              "to": f"{user.first_name.capitalize()} {user.last_name.capitalize()} <{user.email}>",
              "subject": "Welcome to chemlab!",
              "text": f'''Hi {user.first_name.capitalize()},\n
Thanks for signing up at chemlab!\n
You are given a balance of 100 to start with!\n
You may rent new item(s) at https://chemlab.alakh.codes/rent'''})


def invoice(order):
    api_key = os.getenv('mailgun_api')
    with open('website/static/packages/invoice.html', 'r') as f:
        html_string = f.read()
        html_string = html_string.format(amount=order.amount,
                                         first_name=order.user.first_name.capitalize(),
                                         last_name=order.user.last_name.capitalize(),
                                         order_no=order.order_id,
                                         date=datetime.today().strftime('%d-%m-%Y'),
                                         quantity=order.quantity,
                                         item=order.item.item_name.capitalize(),
                                         hours=order.hours,
                                         )
        return requests.post(
            "https://api.eu.mailgun.net/v3/alakh.codes/messages",
            auth=("api", api_key),
            data={"from": "Chemlab <chemlab@alakh.codes>",
                  "to": f"{order.user.first_name.capitalize()} {order.user.last_name.capitalize()} <{order.user.email}>",
                  "subject": "Your Invoice from Chemlab!",
                  "html": html_string
                  })
