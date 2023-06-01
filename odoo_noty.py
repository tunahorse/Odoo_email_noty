import xmlrpc.client
import ssl
from datetime import datetime, date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import configparser
from pprint import pprint


# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Odoo Configuration
url = config['odoo']['url']
db = config['odoo']['db']
username = config['odoo']['username']
password = config['odoo']['password']

# Email Configuration
email_smtp_server = config['email']['smtp_server']
email_smtp_port = int(config['email']['smtp_port'])  # Convert port number from string to integer
email_from_address = config['email']['from_address']
email_to_address = config['email']['to_address']
email_password = config['email']['email_password']

# SSL Context to allow connection to self-signed Odoo server
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Connect to Odoo server
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', allow_none=True, verbose=False, use_datetime=True, context=ctx)
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', allow_none=True, verbose=False, use_datetime=True, context=ctx)

# Authenticate
uid = common.authenticate(db, username, password, {})

# Get user input for date
date_input = input("Please enter a date in this format (YYYY-MM-DD), or leave empty for today's date: ")
if date_input:
    try:
        today = datetime.strptime(date_input, '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format entered. Using today's date.")
        today = date.today()
else:
    today = date.today()

# Get sales data
sales_data = models.execute_kw(
    db, uid, password, 'sale.order', 'search_read',
[[['date_order', '>=', today.strftime('%Y-%m-%d')], ['date_order', '<', (today + timedelta(days=1)).strftime('%Y-%m-%d')]]]
)

# Before creating the email, calculate summaries
total_orders = 0
total_order_amount = 0.0

for sale in sales_data:
    total_orders += 1
    total_order_amount += sale['amount_total']

# Create the email
msg = MIMEMultipart()
msg['From'] = email_from_address
msg['To'] = email_to_address
msg['Subject'] = 'Sales Report'

# Add summary to email body
body = 'Here is the sales data for today: \n\n'
body += f"Total Orders: {total_orders}\n"
body += f"Total Order Amount: {total_order_amount}\n\n"

# Rest of the code to add individual sale data to the body
for sale in sales_data:
    body += f"Order ID: {sale['name']}\n"
    body += f"Customer: {sale['partner_id'][1]}\n"
    body += f"Order Date: {sale['date_order']}\n"
    body += f"Order Amount: {sale['amount_total']}\n\n"

# Attach body to email
msg.attach(MIMEText(body, 'plain'))

# Connect to SMTP server and send the email
server = smtplib.SMTP(email_smtp_server, email_smtp_port)
server.starttls()
server.login(email_from_address, email_password)
server.sendmail(email_from_address, email_to_address, msg.as_string())
server.quit()
