import json, csv, requests
from flask import Flask, render_template, request
app = Flask(__name__)

response = requests.get("https://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

rates = data[0]['rates']
fields = ['currency', 'code', 'bid', 'ask']

file_path = "C:/Users/User/Desktop/Kodilla/Python/Flask/bank.csv"
with open(file_path, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
    writer.writeheader()
    writer.writerows(rates)


with open(file_path, 'r') as read_file:
    reader = csv.reader(read_file, delimiter=';')
    line_count = 0
    currencies = []
    currency_dict = {}
    for row in reader:
        if line_count == 0:
            print(f'Nazwy kolumn to {''.join(row)}')
            line_count += 1
        else:
            currencies.append(row[0])
            currency_dict[row[0]] = row[3]
      


@app.route('/converter', methods=['GET','POST'])
def converter():
    currency = request.form['currency']
    amount = float(request.form['amount'])
    currency_ask = currency_dict.get(currency)
    
    if request.method == 'POST':
        if currency_ask:      
            converted_amount = round(float(currency_ask) * amount, 2)
            return render_template('converter.html', converted_amount=converted_amount, currencies=currencies, currency=currency, amount=amount)
    else:
        return render_template('converter.html', currencies=currencies)

    

if __name__ == '__main__':
    app.run(debug=True)