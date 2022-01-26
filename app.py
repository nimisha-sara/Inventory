from flask import Flask, render_template, request

from datetime import date
today = date.today()

import functions  


app = Flask(__name__)
functions.createTable()

@app.route('/')
def index():
   details = functions.profits()
   return render_template("index.html", data=details)

@app.route("/products",methods = ['GET' , 'POST'])
def insert():
   if (request.method == 'POST') :
      if request.form.get("insert"):
         track_no = request.form["track-no"]
         from_name = request.form["from-name"].title()
         from_contact = request.form["from-contact"]
         from_address = request.form["from-address"]
         date = today.strftime("%B %d, %Y")
         ship_city = request.form["ship-city"].upper()
         reciever_name = request.form["reciever-name"].title()
         reciever_address = request.form["reciever-address"]
         reciever_contact = request.form["reciever-contact"]
         products_selling_price = request.form["products-selling-price"]
         products_cost_price = request.form["products-cost-price"]
         functions.insert(track_no, from_name, from_contact, from_address, date, ship_city, reciever_name,
                              reciever_address, reciever_contact, products_selling_price, products_cost_price)
   rows = functions.view()[::-1]
   return render_template('products.html', rows=rows)

@app.route('/products/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
   if (request.method == 'POST'):
      functions.delete(int(id))
   rows = functions.view()[::-1]
   return render_template("products.html", rows=rows)

@app.route('/products/print_multiple', methods=['GET', 'POST'])
def print_multiple():
   if (request.method == 'POST'):
      r = request.form.getlist('selected-items')
      r = [int(x) for x in r]
      if r != []:
         functions.printing_file(r)
   rows = functions.view()[::-1]
   return render_template("products.html", rows=rows)


@app.route('/index', methods=['GET', 'POST'])
def charts():
   pass


if __name__ == '__main__':
   app.run(debug = True)