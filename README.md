# Simple BB Stock Tracker

This is a simple tool for tracking stock availability at Best Buy. Follow the steps below to set it up and start using it.

## Requirements

Install the necessary Python packages by running the command below in your terminal:

```bash
pip install -r requirements.txt
playwright install
```

## Setup Email Client

You need to set up your email client by exporting your email address and app password as environment variables. Replace <your-email> and <your-email-app-password> with your actual email and password:

```bash
export bbstockemail=<your-email>
export bbstockpass=<your-email-app-password>
```

# Running the Tool
To run the tool, use the command below:


```bash
python main.py
```

After running the command, you will be prompted to:

- Specify the item URL
- Specify the email to which the in-stock notification will be sent
- Specify a short description for the email subject line
