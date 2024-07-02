# Scrape the E-commerce Website
import requests
from bs4 import BeautifulSoup

def get_product_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Example selector, modify based on actual website structure
    price = soup.find('span', class_='product-price').text
    return float(price.replace('$', ''))

url = 'https://example-ecommerce-website.com/product-page'
current_price = get_product_price(url)
print(f"Current price: ${current_price}")
#Store the Data
product_data = {
    'url': url,
    'desired_price': 100.0,  # Example desired price
    'current_price': current_price
}
# Check for Price Drops
import schedule
import time

def check_price_drop():
    product_data['current_price'] = get_product_price(product_data['url'])
    if product_data['current_price'] <= product_data['desired_price']:
        send_notification(product_data)

schedule.every(1).hour.do(check_price_drop)

while True:
    schedule.run_pending()
    time.sleep(1)
#Send Notifications
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    from_email = "your-email@example.com"
    from_password = "your-email-password"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

def send_notification(product_data):
    subject = "Price Drop Alert!"
    body = f"The price of the product at {product_data['url']} has dropped to ${product_data['current_price']}."
    to_email = "user@example.com"
    send_email(subject, body, to_email)

# To send an SMS, you could use Twilio like this:
# from twilio.rest import Client

# def send_sms(body, to_number):
#     account_sid = 'your_twilio_account_sid'
#     auth_token = 'your_twilio_auth_token'
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         body=body,
#         from_='+1234567890',  # Your Twilio number
#         to=to_number
#     )

# def send_notification(product_data):
#     body = f"The price of the product at {product_data['url']} has dropped to ${product_data['current_price']}."
#     to_number = '+0987654321'
#     send_sms(body, to_number)
