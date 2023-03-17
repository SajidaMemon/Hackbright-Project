import os
import json
from random import choice, randint
from datetime import datetime
import requests

import crud
import model
import server

os.system("dropdb food_name")
os.system('createdb food_name')
model.connect_to_db(server.app)
server.app.app_context().push()

model.db.create_all()


    
customer = crud.create_customer(name="Jhon", email="jhon@hotmail.com", password="test", phone="567-767-6767", street="applause place", city="sf", state="CA", zipcode="98692")

model.db.session.add(customer)

model.db.session.commit()

# menu_item1 = crud.create_menu_item(name="burger", price=5,image="https://media.istockphoto.com/id/1206323282/photo/juicy-hamburger-on-white-background.jpg?s=612x612&w=0&k=20&c=K0DxyiChLwewXcCy8aLjjOqkc8QXPgQMAW-vwRCzqG4=")
# menu_item2 = crud.create_menu_item(name="chesseburge",price=5,image= "https://media.istockphoto.com/id/182744943/photo/burger.jpg?s=612x612&w=0&k=20&c=pi20IieXf8UNk6SeJy-cHxubaVD7L5Rnw2i0Qo8vNyM=")
url = "https://free-food-menus-api-production.up.railway.app/burgers"
response = requests.get(url)
data = response.json()
burgers = []
for burger in data:
    name,price,image= (
        burger["name"],
        burger["price"]/10,
        burger["img"]
    )
    menu_item = crud.create_menu_item(name,price,image)
    burgers.append(menu_item)
model.db.session.add_all(burgers)
model.db.session.commit()




# model.db.session.add(menu_item1)
# model.db.session.add(menu_item2)
# model.db.session.commit()

# order_item = crud.create_order_item(quantity=3, price=10)

# model.db.session.add(order_item)

# model.db.session.commit()






    

        

