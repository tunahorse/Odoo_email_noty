# Odoo Sales Report Email Automation

This Python script pulls sales data from an Odoo server and sends an email containing the sales data report. The sales data are segmented between retail orders and distributor orders. The email includes a summary of total orders and total amounts for both segments, followed by the details of each order.

## Configuration

The script reads configuration parameters from a `.ini` file. The necessary parameters include Odoo server details (URL, database name, username, and password) and email settings (SMTP server, port, from address, to address, and email password).

## Usage

To run this script, use the following command:

\```bash
python3 /path/to/odoo_email.py
\```

Replace `/path/to/` with the actual path to the script.

## Scheduling with Cron

You can schedule this script to run at a specific time every weekday using cron. For example, to schedule the script to run at 2 PM every weekday, open the crontab file using the command `crontab -e`, then add the following line:

\```bash
0 14 * * 1-5 python3 /home/fabian/email_noty/odoo_email.py
\```

Save and close the crontab file to finish.

Note: This assumes that you have Python 3 installed and it's available in your system PATH. If the location of your Python 3 interpreter is different, specify the full path in the cron job.

