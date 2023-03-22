"""CRUD operations."""

from model import db, Customer,Payment, Order,OrderItem, MenuItem, connect_to_db


def create_customer(name,email,password,phone,street,city,state,zipcode):
    """Create and return a new customer."""

    customer = Customer(name=name, email=email, password=password, phone=phone, street=street, city=city, state=state, zipcode=zipcode)
    return customer

def get_customers():
    """Return all customers."""

    return Customer.query.all()

def get_customer_by_id(customer_id):
    """Return a customer by primary key."""

    return Customer.query.get(customer_id)


def get_customer_by_email(email):
    """Return a customer by email."""

    return Customer.query.filter(Customer.email == email).first()





def create_payment(card_number,orders):
    payment = Payment(card_number=card_number,orders=orders)
    return payment

def get_payment():
    """Return all payment."""

    return Payment.query.all()

def get_payment_by_id(payment_id):
    """Return a payment by primary key."""

    return Payment.query.get(payment_id)



    
def create_order(customer_id,payment_id = None):
    order = Order(customer_id=customer_id, payment_id=payment_id)
    return order


def get_order():
    """Return all order."""

    return Order.query.all()


def get_order_by_id(order_id):
    """Return a order by primary key."""

    return Order.query.get(order_id)





def create_order_item(quantity, price, order_id,  item_id):
    order_item = OrderItem(quantity=quantity, price=price, order_id=order_id,  item_id=item_id)
    return order_item


def create_menu_item(name,price,image):
    menu_item = MenuItem(name=name, price=price,image=image)
    return menu_item


def get_menu_item_id(item_id):
    menu_item =MenuItem.query.get(item_id)
    return menu_item




def get_all_menu_item():
    menu_items = db.session.query(MenuItem).all()
    return menu_items


if __name__ == '__main__':
    from server import app
    connect_to_db(app)