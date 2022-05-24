##
# main.py
# 2022-05-25

from PySide6 import QtWidgets
from enum import Flag, auto

class ProductAttributes(Flag):
    DEFAULT = auto()
    VEGAN_OPTION = auto()
    VEGETARIAN_OPTION = auto()
    HAS_SUGAR = auto()

class Product():
    def __init__(self)

class KaiUI(QtWidgets.QMainWindow):
    def __init__(self, *args):
        super()._init__(*args)

        self.initUI()

    def initUI(self):
        ...
 

def main():
    app = QtWidgets.QApplication()
    main = KaiUI()

    main.show()
    app.exec()
# Onslow College is revamping the menu at the café. There will be a move to
# healthy options that reflect the diversity of the student body. This includes
# daily special items.

# More importantly, students will be able to order food via an app loaded on
# computers placed all around the school. The order will be sent to the café for
# the students to collect at either interval or lunch time.

# You will create the software for students to make orders.
# User interface

# The interface should display the following:

#     a list of products, divided by product category
#     information about the products
#         whether it is vegetarian-friendly or has vegetarian options
#         whether it is vegan-friendly or has vegetarian options
#         whether it contains added sugar
#         the country of origin (for special items)
#     the cost of the products
#     the current day (which should be selectable) that shows the special item of the day

# The interface will allow the user to do the following:

#     add an item to their order
#     remove an item from their order
#     calculate the total cost of the order
#     send the order to the café for processing

# You may lay the interface out however you like.
# Object-oriented programming

# You should create classes for the following aspects of the program:

#     Product: contains the information about the product
#     ProductCategory: contains the products by category
#     Order: contains the contents of the order

# Remember to create relevant properties, setters, and methods.
# Café information
# Products

# All products are divided into three categories:

#     sandwiches
#     sushi
#     drinks
#     special items of the day

# Sandwiches
# Item 	V option available 	VG option available 	Contains sugar 	Price
# Ham & egg sandwich 	  	  	  	$3.50
# Chicken mayo sandwich 	  	  	  	$3.50
# Egg sandwich 	✅ 	  	  	$3.00
# Beef sandwich 	  	  	  	$3.80
# Salad sandwich 	✅ 	✅ 	  	$3.20
# Sushi

# Item 	V option available 	VG option available 	Contains sugar 	Price
# Chicken (3pc) 	  	  	  	$4.50
# Tuna (3pc) 	  	  	  	$4.50
# Avocado sushi (3pc) 	✅ 	✅ 	  	$4.80
# Chicken rice bowl 	  	  	  	$5.50
# Vegetarian rice bowl 	✅ 	✅ 	  	$5.50
# Drinks
# Item 	V option available 	VG option available 	Contains sugar 	Price
# Soda can 	✅ 	✅ 	✅ 	$2.00
# Aloe vera drink 	✅ 	  	✅ 	$3.50
# Chocolate milk 	  	  	✅ 	$3.50
# Water bottle 	✅ 	✅ 	  	$2.50
# Instant hot chocolate 	✅ 	  	✅ 	$1.50
# Special items of the day

# The following items can only be ordered on specific days.
# Day 	Item 	V option available 	VG option available 	Contains sugar 	Price
# Monday 	Kale moa 	  	  	✅ 	$6.00
# Tuesday 	Potjiekos 	  	  	  	$6.00
# Wednesday 	Hangi 	✅ 	✅ 	  	$6.00
# Thursday 	Paneer tikka masala 	✅ 	  	✅ 	$6.00
# Friday 	Chow mein 	✅ 	✅ 	  	$6.00