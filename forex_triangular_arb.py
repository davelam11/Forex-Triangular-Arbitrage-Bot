import requests
import itertools

def calculate_profit(currencies, exchange_rates, commission):
    a, b, c = currencies
    profit = (exchange_rates[a][b] * exchange_rates[b][c] * exchange_rates[c][a]) - 1
    profit -= commission * 2
    return profit * 10000


def execute_trade(currencies, exchange_rates, units, commission):
    a, b, c = currencies
    first_pair = "{}_{}".format(a, b)
    second_pair = "{}_{}".format(b, c)
    third_pair = "{}_{}".format(c, a)

    url = "https://api-fxtrade.oanda.com/v3/accounts/<your-account-id>/orders"

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    # Place first trade to buy currency 'b' using currency 'a'
    data = {
        "order": {
            "units": units,
            "instrument": first_pair,
            "timeInForce": "FOK",
            "type": "MARKET",
            "side": "buy"
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 201:
        print("Failed to execute first trade. Error code: {}".format(response.status_code))
        return

    # Place second trade to sell currency 'b' and buy currency 'c'
    data = {
        "order": {
            "units": units,
            "instrument": second_pair,
            "timeInForce": "FOK",
            "type": "MARKET",
            "side": "sell"
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 201:
        print("Failed to execute second trade. Error code: {}".format(response.status_code))
        return

    # Place third trade to sell currency 'c' and buy back currency 'a'
    data = {
        "order": {
            "units": units,
            "instrument": third_pair,
            "timeInForce": "FOK",
            "type": "MARKET",
            "side": "sell"
        }
    }


def triangular_arbitrage(currencies, exchange_rates, units, commission, threshold):
    for currency_triple in itertools.permutations(currencies, 3):
        a, b, c = currency_triple
        profit = (exchange_rates[a][b][1] * exchange_rates[b][c][1] * exchange_rates[c][a][0]) - 1
        profit -= commission * 2
        if profit >= threshold:
            execute_trade(currency_triple, exchange_rates, units, commission)


def fetch_bid_ask_prices(access_token, instruments):
    prices = {}
    for instrument in instruments:
        url = "https://api-fxtrade.oanda.com/v3/instruments/{}/candles".format(instrument)

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        }

        params = {
            "count": 1,
            "price": "BA"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            bid = data["candles"][0]["bid"]["c"]
            ask = data["candles"][0]["ask"]["c"]
            prices[instrument] = (bid, ask)
        else:
            print("Failed to retrieve data for {}. Error code: {}".format(instrument, response.status_code))

    return prices


def main():
    access_token = "<your-oanda-api-token>"
    instruments = ["EUR_USD", "USD_JPY", "EUR_GBP"]
    commission = 5 / 100000 # 5 USD per 100,000 units
    threshold = 0.0005 # 0.5 pips
    units = 100000

    bid_ask_prices = fetch_bid_ask_prices(access_token, instruments)
    exchange_rates = {}

    for instrument in instruments:
        exchange_rates[instrument] = {}
        for other_instrument in instruments:
            if instrument != other_instrument:
                bid, ask = bid_ask_prices[other_instrument]
                exchange_rates[instrument][other_instrument] = bid
                exchange_rates[instrument][other_instrument] = ask

    triangular_arbitrage(instruments, exchange_rates, units, commission, threshold)


if __name__ == "__main__":
    main()
