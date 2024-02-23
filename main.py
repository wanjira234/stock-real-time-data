import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_APIKEY = "UT7CTFBKRTJBONB2"
NEWS_APIKEY = "ac62640140ec4317b1a1bc78fd2b1d0b"
TWILIO_SID = "AC1cc2689706b2f540a0c794273d59e3b1"
TWILIO_AUTH_TOKEN = "4b05eb0d885081f6df54e1603bc9fc8f"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [
# new_value for (key, value) in dictionary.items()]

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_APIKEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]

stock_prices = [value for (key, value) in data.items()]
yesterdays_data = stock_prices[0]
yesterdays_closing_prices = yesterdays_data["4. close"]
print(f"closing stock price was {yesterdays_closing_prices}")
print(data)
# - Get the day before yesterday's closing stock price
day_before_yesterday = stock_prices[1]
day_before_yesterday_closing_price = day_before_yesterday["4. close"]
print(f" price was {day_before_yesterday_closing_price}")
# -Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint:
# https://www.w3schools.com/python/ref_func_abs.asp

difference = abs(float(yesterdays_closing_prices) - float(day_before_yesterday_closing_price))
print(f"abs is {difference}")
# - Work out the percentage difference in price between closing price yesterday and closing price the day before
# yesterday.
diff_percentage = difference / float(yesterdays_closing_prices) * 100
print(diff_percentage)

# - If TODO4 percentage is greater than 5 then print("Get News").
# STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if diff_percentage > 1:
    news_params = {
        "apikey": NEWS_APIKEY,
        "qInTitle": COMPANY_NAME
    }
    my_stock_news = requests.get(NEWS_ENDPOINT, news_params)
    articles = my_stock_news.json()["articles"]

    # T - Use Python slice operator to create a list that contains the first 3 articles. Hint:
    # https://stackoverflow.com/questions/509211/understanding-slice-notation

    three_articles = articles[:3]
    print(three_articles)
    # STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    # - Create a new list of the first 3 articles headline and description using list comprehension.
    formatted_article = [f"Headline{article['title']} .\n brief: {article['description']}" for article in
                         three_articles]

    #  - Send each article as a separate message via Twilio.

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_article:
        message = client.messages.create(
            body=article,
            from_='+12512835189',
            to='+254703687201'
        )

    # Optional Format the message like this:
"""TSLA: 🔺2% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey have 
gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings 
show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash. 
or "TSLA: 🔻5% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey 
have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F 
filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus 
market crash. """
