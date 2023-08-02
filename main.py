from playwright.sync_api import sync_playwright
from datetime import datetime
from dataclasses import dataclass
from email.message import EmailMessage
import smtplib
import os
import time
import random
import logging

logging.basicConfig(level=logging.INFO)


def send_email(user_email, user_input, item):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Item in Stock - ' + item
        msg['From'] = 'BB Stock Tracker Bot'
        msg['To'] = user_email
        msg.set_content("Item is in stock! Link: " + user_input)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.environ.get('bbstockemail'),
                     os.environ.get('bbstockpass'))
        server.send_message(msg)
        server.quit()
    except:
        print("Error sending email")


def checker(url, email, item, cadence):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        found = False
        while not found:
            page.goto(url)
            state = page.wait_for_selector("button.add-to-cart-button").get_attribute(
                "data-button-state"
            )
            match state:
                case "SOLD_OUT":
                    logging.info("Out of stock at " +
                                 datetime.now().strftime("%H:%M:%S"))
                    time.sleep(random.gauss(mu=cadence, sigma=2))
                case "ADD_TO_CART":
                    logging.info(
                        f"🎉 Found {item} at {datetime.now().strftime('%H:%M:%S')}!!!")
                    send_email(email, url, item)
                    found = True
                case _:
                    raise Exception(
                        "Got unknown state " + state + " on page: " + page.content()
                    )
        browser.close()


if __name__ == "__main__":
    URL = input("Enter the Bestbuy link of the item you want to track: ")
    EMAIL = input("Enter the email you want to send the notification to: ")
    ITEM = input(
        "Enter the a short text of what the item is (email subjectline): ")
    CADENCE = 30
    checker(URL, EMAIL, ITEM, CADENCE)
