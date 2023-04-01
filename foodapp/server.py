
from flask import (Flask, render_template, flash, session, redirect,request)
                 
from model import connect_to_db, db

import os
import crud

app = Flask(__name__)
app.secret_key="dev12345"

# api_key = os.environ["API_KEY"]

# Replace this with routes and view functions!

@app.route('/', methods=['GET'])
def index():
    # url = "https://free-food-menus-api-production.up.railway.app/burgers"
    # response = requests.get(url)
    # data = response.json()
    # print(data)
    
    return render_template('index.html')


@app.route("/home")
def home():
    return redirect("/")



@app.route("/signin",methods= ["POST"])
def signin():
    user_email= request.form.get("email")
    user_password= request.form.get("password")
    customer= crud.get_customer_by_email(user_email)
    print(customer)
    if customer:
        if customer.password == user_password:
            session['customer_id'] = customer.customer_id
            print(f"{customer.email}'s test: user_id = {session['customer_id']}")
            flash("Logged In!")
        else:
            flash("Incorrect password! Try again.")
    else:
        flash("No account associated with email.")

    return redirect("/signin")
    


@app.route("/signin",methods= ["GET"])
def show_signin():
    return render_template("signin.html")



@app.route("/sign_up",methods= ["GET","POST"])
def sign_up():
    return render_template("sign_up.html")



@app.route("/users",methods= ["POST"] )
def create_user():
    name= request.form.get("name")
    email= request.form.get("email")
    password= request.form.get("password")
    street= request.form.get("street")
    phone= request.form.get("phone")
    city= request.form.get("city")
    state= request.form.get("state")
    zipcode= request.form.get("zipcode")
    new_customer = crud.create_customer(name,email,password,phone,street,city,state,zipcode)
    db.session.add(new_customer)
    db.session.commit()
    
    return render_template("home.html")



@app.route("/menu")
def view_menu():
    menu_items = crud.get_all_menu_item()
    return render_template("menu.html", menu_items=menu_items)



@app.route("/add_to_cart/<item_id>")
def add_to_cart(item_id):
   
    if "cart" in session:
        cart = session['cart']
        
        flash("item successfully added to cart.")
    else:
        cart = session['cart'] = {}
        
    cart[item_id] = cart.get(item_id, 0) + 1
    return "item successfully added to cart"



@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/cart")
def show_shopping_cart():
    # return render_template("cart.html")
    order_total = 0
    # cart_burgers = []
    cart = session.get("cart", {})
    burger_list = []
    total = 0
    for burger_id,quantity in cart.items():
        burger_object = crud.get_menu_item_id(burger_id)
        burger_object.quantity=quantity
        burger_object.cost=burger_object.price * quantity
        burger_list.append(burger_object)
        total += burger_object.price * quantity

    return render_template("cart.html",burger_list=burger_list,total=total)



@app.route("/checkout")
def check_out():
    if 'customer_id' not in session:
        flash("please sign in")
        return redirect("/signin")

    order_total = 0
    # cart_burgers = []
    cart = session.get("cart", {})
    burger_list = []
    total = 0
    for burger_id,quantity in cart.items():
        burger_object = crud.get_menu_item_id(burger_id)
        burger_object.quantity=quantity
        burger_object.cost=burger_object.price * quantity
        burger_list.append(burger_object)
        total += burger_object.price * quantity

    return render_template("checkout.html",burger_list=burger_list,total=total)



@app.route("/place_order", methods = ["POST"])
def place_order():
    
    card_number = request.form.get("card-number")
    if 'customer_id' not in session:
        flash("please sign in")
        return redirect("/signin")
    else:
        customer_id = session.get("customer_id")


    if crud.get_payment_by_card_number(card_number):
        payment_id = crud.get_payment_by_card_number(card_number).payment_id
    else:
        payment = crud.create_payment(card_number)
        db.session.add(payment)
        db.session.commit()
        payment_id = payment.payment_id

    order = crud.create_order(customer_id,payment_id)
    db.session.add(order)
    db.session.commit()
    order_id = order.order_id
    cart = session.get("cart",{})

    for burger_id,quantity in cart.items():
        burger_price = crud.get_price_of_menu_item(burger_id)
        order_item = crud.create_order_item(quantity, burger_price, order_id,  burger_id)
        db.session.add(order_item)
    db.session.commit()

    del session["cart"]
    flash("Order Placed")
    return redirect(f"/summery/{order_id}")



@app.route("/summery/<order_id>")
def ordersummery(order_id):
    order = crud.get_order_by_id(order_id)
    customer = order.customer
    order_items = order.order_item
    total = 0 
    for item in order_items:
        total += item.quantity * item.price


    return render_template("order_summery.html",order_id=order_id,name=customer.name,order_items=order_items,total=total)

    


@app.route("/contact",methods=["GET","POST"] )
def contact_us():
    if request.method =="POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        flash("Thank you for your message ")
        return redirect("/")
    
    return render_template("contact.html")






     
@app.route('/logout', methods=['POST', 'GET'])
def log_out():

    if session.get("customer_id",None):
        session.pop("user", None)
        session.pop("cart",None)
    return redirect('/')

        





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
