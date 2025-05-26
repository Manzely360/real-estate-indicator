from flask import Flask, render_template, request
from roi import calculate_roi

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    roi = None
    if request.method == 'POST':
        try:
            purchase_price = float(request.form['purchase_price'])
            renovation_cost = float(request.form['renovation_cost'])
            annual_rent = float(request.form['annual_rent'])
            annual_expenses = float(request.form['annual_expenses'])
            roi = calculate_roi(purchase_price, renovation_cost, annual_rent, annual_expenses)
        except (KeyError, ValueError):
            roi = 'Invalid input'
    return render_template('index.html', roi=roi)


if __name__ == '__main__':
    app.run(debug=True)
