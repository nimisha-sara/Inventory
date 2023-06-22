from flask import Flask, render_template, request

import database

from datetime import date
today = date.today()

app = Flask(__name__)
database.createTable()
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def dash():
    return render_template("dashboard.html")


@app.route("/sales", methods=['GET', 'POST'])
def sales():
    print(f"\n\n{request.form}\n\n")
    if (request.method == 'POST') and 'delete' in request.form:
        customer = int(request.form["id"])
        database.delete(customer)
    elif (request.method == 'POST'):
        _id = int(request.form["id"])
        customer = request.form["customer-name"].title()
        address = request.form["address"].title()
        contact = request.form["contact"]
        products = [request.form[f"prod-{i}"] for i in range(1, 11) if request.form[f"prod-{i}"] != '']
        product_count = len(products)

        quantity = [int(request.form[f"quant-{i}"]) for i in range(1, 11) if request.form[f"prod-{i}"] != 0]
        rates = [int(request.form[f"rate-{i}"]) for i in range(1, 11) if request.form[f"prod-{i}"] != 0]
        print(quantity, rates, [quantity[i] * rates[i] for i in range(0, 10)])
        total = sum([(quantity[i] * rates[i]) for i in range(0, 10)])

        products, quantity, rates = "$$".join(products), ','.join(map(str, quantity)), ','.join(map(str, rates))

        date = today.strftime("%B %d, %Y")
        city_state = request.form["city-state"].title()

        if 'add-sale' in request.form:
            database.insert(customer, address, contact, products,
                            quantity, rates, total, product_count, date,
                            city_state)
        if 'edit-sale' in request.form:
            database.update(_id, customer=customer, address=address, contact=contact, products=products, quantity=quantity, rates=rates, total=total, product_count=product_count, city_state=city_state)
    rows = database.view()[::-1]
    customers = database.get_customers()
    addresses = database.get_address()
    contacts = database.get_contact()
    return render_template('sales.html', rows={"data": rows,
                                               "customers": customers,
                                               "addresses": addresses,
                                               "contacts": contacts})


if __name__ == '__main__':
    app.run(debug=True)
