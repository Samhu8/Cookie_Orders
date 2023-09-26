from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.cookie import Cookie


@app.route('/')
def all_orders():
    all_orders = Cookie.all_orders()
    return render_template("index.html", orders= all_orders)

@app.route('/cookie/new_order')
def order_page():
    return render_template('new_order.html')

@app.route('/cookie/new_order', methods=["POST"])
def new_order():
    if not Cookie.validate_order(request.form):
        return redirect('/cookie/new_order')
    data = {
        "customer_name" : request.form["customer_name"],
        "cookie_type" : request.form["cookie_type"],
        "number_of_boxes" : request.form["number_of_boxes"]
    }
    Cookie.save(data)
    print(data)
    return redirect('/')

@app.route('/cookie/edit_order/<int:id>')
def update_order(id):
    order_edit = Cookie.one_order(id)
    return render_template('edit_order.html', update = order_edit)


@app.route('/cookie/edit_order/<int:id>', methods=["POST"])
def edit_order(id):
    if not Cookie.validate_order(request.form):
        return redirect(f"/cookie/edit_order/{request.form['id']}")
    data = {
        "customer_name" : request.form["customer_name"],
        "cookie_type" : request.form["cookie_type"],
        "number_of_boxes" : request.form["number_of_boxes"],
        "id" : id
    }
    return redirect('/')