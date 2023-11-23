import json
from flask import render_template, request, redirect, session, jsonify
from flask_session import Session
# from models.machine import Inserttable, db
# from services.user_service import insert_logic, create_logic

# Save these products in database
####
products = [{'id': 1,
             'name': 'Robo Dog',
             'image': 'toy1.png',
             'rating': 4, 
             'selling_price': 900,
             'marked_price': 1000,
             'status': 'For Sale'
             },{'id': 2,
             'name': 'Alza',
             'image': 'toy2.png',
             'rating': 5, 
             'selling_price': 1900,
             'marked_price': 2000,
             'status': 'For Sale'
             },{'id': 3,
             'name': 'Electric Toy Car',
             'image': 'toy3.png',
             'rating': 5, 
             'selling_price': 2900,
             'marked_price': 3000,
             'status': 'For Sale'
             },{'id': 4,
             'name': 'Lego house',
             'image': 'toy4.png',
             'rating': 4, 
             'selling_price': 500,
             'marked_price': 1000,
             'status': 'For Sale'
             },{'id': 5,
             'name': 'Toy car',
             'image': 'toy5.png',
             'rating': 4, 
             'selling_price': 900,
             'marked_price': 1000,
             'status': 'For Sale'
             },{'id': 6,
             'name': 'Plane',
             'image': 'toy6.png',
             'rating': 5, 
             'selling_price': 1900,
             'marked_price': 2000,
             'status': 'For Sale'
             },{'id': 7,
             'name': 'Crane',
             'image': 'toy7.png',
             'rating': 5, 
             'selling_price': 2900,
             'marked_price': 3000,
             'status': 'Not For Sale'
             },{'id': 8,
             'name': 'Truck',
             'image': 'toy8.png',
             'rating': 4, 
             'selling_price': 500,
             'marked_price': 1000,
             'status': 'Not For Sale'
             },
                
]

def index():
    if not session.get("user_id"):
        return redirect("/login")
    # Get products from database using services
    ##########
    return render_template('dashboard/dashboard.html', products= products, user_id=session.get('user_id'))
    
def login():
    if request.method == "POST":
        # Check here for login using the services
        session["user_id"] = request.form.get("email")
        print("Session name", request.form.get("email"))
        return redirect("/")
    return render_template("login/login.html")

def logout():
    session["user_id"] = None
    session["orders"] = None
    session["cart"] = None
    return redirect("/")

def order():
    # Get the value of the 'name' parameter from the URL
    productId = request.args.get('id')
    selectedProduct = None 
    for product in products:
        if product['id'] == int(productId):
            selectedProduct = product

    ###### Stop IDOR
    if selectedProduct['status'] == 'Not For Sale':
        return redirect('/')    
    return render_template("order/order.html", product=selectedProduct)

def addAddress():
   return redirect("/")

def addToCart():
    data = request.json

    ### Secure the website by taking important data such as price from server side only
    data['product_id']
    for product in products:
        if product['id'] == int(data['product_id']):
            selectedProduct = product
    
    data['price'] = selectedProduct['selling_price']
    data['total'] = selectedProduct['selling_price'] * data['quantity']
    data['name'] = selectedProduct['name']
    data['image'] = 'static/images/' + selectedProduct['image']

    # Retrieve the current cart from the session or initialize an empty cart
    cart = session.get('cart', [])

    if( not cart):
        cart = []
        
    # Add the new item to the cart
    cart.append(data)

    # Update the cart in the session
    session['cart'] = cart

    print("Cart Data:", cart)

    data = { 
            "message" : "Data Structures and Algorithms", 
        } 
  
    return jsonify(data) 

def cart():
    # Retrieve the current cart from the session or initialize an empty cart
    cart = session.get('cart', [])
    totalPrice = 0
    if (cart):
        totalPrice = sum(item['total'] for item in cart)

    
    return render_template("cart/cart.html", cart = cart, totalPrice = totalPrice)

def placeOrder():
    cart = session.get('cart', [])
    session['cart'] = []

    # Place order for now storing them in orders
    orders = session.get('orders', [])
    if(not orders):
        orders = []
    orders.append(cart)

    session['orders'] = orders
    
    print("placed order for ", cart)

    return redirect("/")

def profile():
    orders = session.get('orders', [])
    print("orders", orders)
    return render_template("profile/profile.html", orders = orders, user_id=session.get('user_id'))

    