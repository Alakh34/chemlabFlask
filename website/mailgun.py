import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


def sign_up_email(email, name):
    api_key = os.getenv('mailgun_api')
    return requests.post(
        "https://api.eu.mailgun.net/v3/alakh.codes/messages",
        auth=("api", api_key),
        data={"from": "Chemlab <chemlab@alakh.codes>",
              "to": f"{name} <{email}>",
              "subject": f"Welcome to chemlab!",
              "text": f'''Hi {name},

Thanks for signing up at chemlab!
              
You are given a balance of 100 to start with!
              
You may rent new item(s) at https://chemlab.alakh.codes/rent'''})


def invoice(email, name, order):
    api_key = os.getenv('mailgun_api')
    with open('website/static/packages/invoice.html', 'r') as f:
        html_string = f.read()
        html_string = html_string.format(amount=order.amount,
                                         name=order.user.first_name,
                                         order_no=order.order_id,
                                         date=datetime.today().strftime('%Y-%m-%d'),
                                         quantity=order.quantity,
                                         item=order.item.item_name,
                                         hours=order.hours,
                                         )
        return requests.post(
            "https://api.eu.mailgun.net/v3/alakh.codes/messages",
            auth=("api", api_key),
            data={"from": "Chemlab <chemlab@alakh.codes>",
                  "to": f"{name} <{email}>",
                  "subject": f"Your Invoice from Chemlab!",
                  "html": html_string
                  })
