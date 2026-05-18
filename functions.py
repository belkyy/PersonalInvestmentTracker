import requests

def get_live_prices():

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin,ethereum,solana,ripple,binancecoin",
        "vs_currencies": "usd"
    }

    try:

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        return {

            "BTC": data["bitcoin"]["usd"],

            "ETH": data["ethereum"]["usd"],

            "SOL": data["solana"]["usd"],

            "XRP": data["ripple"]["usd"],

            "BNB": data["binancecoin"]["usd"]

        }

    except:

        return {

            "BTC": 0,
            "ETH": 0,
            "SOL": 0,
            "XRP": 0,
            "BNB": 0

        }
    
def calculate_portfolio(
    investments,
    prices
):

    investment_list = []

    worst_asset = None
    worst_percentage = 0

    total_balance = 0
    total_initial_value = 0
    total_current_value = 0

    for inv in investments:

        current_price = prices.get(
            inv["coin"],
            0
        )

        # VALUES
        initial_value = (
            inv["amount"]
            * inv["buy_price"]
        )

        current_value = (
            inv["amount"]
            * current_price
        )

        # PROFIT LOSS
        profit_loss = (
            current_value
            - initial_value
        )

        # PERCENTAGE
        if initial_value > 0:

            percentage = (
                (
                    current_value
                    - initial_value
                )
                /
                initial_value
            ) * 100

        else:

            percentage = 0

        # TOTALS
        total_balance += current_value

        total_initial_value += initial_value

        total_current_value += current_value

        # WORST ASSET
        if percentage < worst_percentage:

            worst_percentage = percentage
            worst_asset = inv["coin"]

        investment_list.append({

            "id": inv["id"],

            "coin": inv["coin"],

            "amount": round(
                inv["amount"],
                4
            ),

            "buy_price": inv["buy_price"],

            "current_price": current_price,

            "position_value": round(
                current_value,
                2
            ),

            "profit_loss": round(
                profit_loss,
                2
            ),

            "percentage": round(
                percentage,
                2
            )

        })

    # TOTAL %
    if total_initial_value > 0:

        portfolio_percentage = (
            (
                total_current_value
                - total_initial_value
            )
            /
            total_initial_value
        ) * 100

    else:

        portfolio_percentage = 0

    return {

        "investments": investment_list,

        "total_balance": round(
            total_balance,
            2
        ),

        "total_invested": round(
            total_initial_value,
            2
        ),

        "portfolio_percentage": round(
            portfolio_percentage,
            2
        ),

        "worst_asset": worst_asset,

        "worst_percentage": round(
            worst_percentage,
            2
        )

    }