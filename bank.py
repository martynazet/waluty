import csv
import requests
from flask import Flask, render_template, request
app = Flask(__name__)


def get_data():
    response = requests.get("https://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()

    rates = data[0]['rates']
    fields = ['currency', 'code', 'bid', 'ask']
    currency_dict = {}

    for i in rates:
        currency_dict[i['currency']] = i['ask']

    with open('bank.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
        writer.writeheader()
        writer.writerows(rates)

    return currency_dict


@app.route('/converter', methods=['GET', 'POST'])
def converter():
    currency_dict = get_data()
    if request.method == 'POST':
        currency = request.form['currency']
        amount = float(request.form['amount'])
        currency_ask = currency_dict.get(currency)
        if currency_ask:
            converted_amount = round(float(currency_ask) * amount, 2)
            return render_template('converter.html', converted_amount=converted_amount, currencies=currency_dict.keys(), currency=currency, amount=amount)
    else:
        return render_template('converter.html', currencies=currency_dict.keys())


if __name__ == '__main__':
    app.run(debug=True)