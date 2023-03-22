
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


class Customer(db.Model):
    """A Customer."""
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    street = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)

    orders = db.relationship("Order", back_populates="customer")


    def __repr__(self):
        return f"<Customer customer_id={self.customer_id} name={self.name} email={self.email}>"



class Payment(db.Model):
    """A Payment."""
    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_number =db.Column(db.String(50), unique=True, nullable=False)

    orders = db.relationship("Order", back_populates="payment")

    def __repr__(self):
        return f"<Payment payment_id={self.payment_id}>"




class Order(db.Model):
    """A Order."""
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"))
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.payment_id"))

    customer = db.relationship("Customer", back_populates="orders")
    payment = db.relationship("Payment", back_populates="orders")
    order_item = db.relationship("OrderItem", back_populates="orders")

    def __repr__(self):
        return f"<Order order_id={self.order_id}>"




class OrderItem(db.Model):
    """A OrderItem."""
    __tablename__ = "order_items"

    order_item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"))
    item_id = db.Column(db.Integer, db.ForeignKey("menu_items.item_id"))
    quantity= db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(6,2),  nullable=False)

    orders = db.relationship("Order", back_populates="order_item")
    menu_item = db.relationship("MenuItem", back_populates="order_item")


    def __repr__(self):
        return f"<OrderItem order_item_id={self.order_item_id}>"



class MenuItem(db.Model):
    """A Menu_item."""
    __tablename__ = "menu_items"


    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(6,2), nullable=False)
    image= db.Column(db.String(600), nullable=False)

    order_item = db.relationship("OrderItem", back_populates="menu_item")
    

    def __repr__(self):
        return f"<MenuItem manu_item_id={self.item_id}>"
    




def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///food_name"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Connected to db!")


if __name__ == "__main__":
    from server import app 
    
    connect_to_db(app)


        


