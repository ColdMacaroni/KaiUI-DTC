##
# main.py
# 2022-05-25

from PySide6 import QtWidgets, QtCore
from enum import Flag, Enum, auto

class SushiType(Enum):
    PIECES = auto()
    BOWL = auto()

class ProductAttribute(Flag):
    NONE = auto()
    VEGAN = auto()
    VEGETARIAN = auto()
    HAS_SUGAR = auto()

class Day(Flag):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()

class Product:
    def __init__(self, name: str, price: float, attributes: ProductAttribute = ProductAttribute.NONE):
        self.attributes = attributes | ProductAttribute.NONE
        self.name = name
        self.price = price
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new):
        if not isinstance(new, str):
            raise ValueError("Name must be type string")
        self._name = new

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new):
        if not isinstance(new, float):
            raise ValueError("Price must be type float")
        self._price = new

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, new):
        if not isinstance(new, ProductAttribute):
            raise ValueError("Attribute must be type ProductAttribure")
        self._attributes = new
    
class Sandwich(Product):
    pass

class Sushi(Product):
    def __init__(self, type_: SushiType, *args, pieces: int = 0):
        super().__init__(*args)
        self.type = type_

        if self.type is SushiType.PIECES:
            self.pieces = pieces

class Drink(Product):
    pass

class Special(Product):
    def __init__(self, day: Day, country: str, *args):
        super().__init__(*args)
        self.day = day

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, new):
        if not isinstance(new, Day):
            raise ValueError("Day must be type Day")
        self._day = new

class ProductInfo(QtWidgets.QWidget):
    def __init__(self, product: Product, *args):
        super().__init__(*args)
        
        # Im not gonna bother with a setter because i think its better if it just doesnt change
        assert isinstance(product, Product), f"{product} should be type an instance of Product"
        self.product = product
        self.type = type(product)
        
        # TODO: Image label
        # self.img_label = QtWidgets.QLabel()
        self.name_label = QtWidgets.QLabel(self)
        self.price_label = QtWidgets.QLabel(self)
        self.vegetarian_label = QtWidgets.QLabel(self)
        self.vegan_label = QtWidgets.QLabel(self)
        self.has_sugar_label = QtWidgets.QLabel(self)
        self.initUI()


    def initUI(self):
        self.name_label.setText(self.product.name)
        self.name_label.setStyleSheet("font-size: 15pt")
        
        self.price_label.setText(f"${self.product.price:.02f}")
        
        self.vegetarian_label.setText(f"Vegetarian: {'✅' if self.product.attributes & ProductAttribute.VEGETARIAN else '❎'}")

        self.vegan_label.setText(f"Vegan: {'✅' if self.product.attributes & ProductAttribute.VEGAN else '❎'}")

        self.has_sugar_label.setText(f"Sugar: {'✅' if self.product.attributes & ProductAttribute.HAS_SUGAR else '❎'}")

        vbox = QtWidgets.QVBoxLayout()
        vbox.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.price_label)
        vbox.addWidget(self.vegetarian_label)
        vbox.addWidget(self.vegan_label)
        vbox.addWidget(self.has_sugar_label)
        
        self.setLayout(vbox)
        self.show()

class KaiUI(QtWidgets.QMainWindow):
    # Which keys the products dict can have, also used for creating the tabs
    _ACCEPTABLE_KEYS = ["sandwiches", "sushi", "drinks", "specials"]

    @classmethod
    @property
    def ACCEPTABLE_KEYS(cls) -> list[str]:
        """
        This getter is here to avoid accidentally changing the const. It's a list
        so things can get messy. Actually its not that it'd change much.
        It should probably return a .copy() but idk about creating so many lists.
        It just doesnt sit right, you know?
        """
        return cls._ACCEPTABLE_KEYS

    def __init__(self, products: dict[str, list[Sandwich | Sushi | Drink | Special]], *args):
        """
        This init only creates the objects needed for the ui, method initUI creates the layouts and
        actually fits everything together.
        """
        # Do the thing
        super().__init__(*args)
        
        # 'Declare' the private one to avoid any possible issues with the setter
        self._products = {}
        self.products = products

        self.products_tab = QtWidgets.QTabWidget(self)
        
        # A QWidget for every possible tab
        self.products_tab_widgets = {
            key: QtWidgets.QWidget()
            for key in self.ACCEPTABLE_KEYS
        }

        self.initUI()

    def setup_tab_widget(self, key):
        """
        Adds all the necessary widgets from the products dict to the products tab QWidget
        that has the same key
        """
        # TODO
        ...


    def initUI(self):
        self.setWindowTitle("Kai")
        
        # Make it a *nice* window size
        self.setGeometry(QtCore.QRect(200, 100, 800, 600))
 
        # Set tab names, and add a tab to the thing
        for name, widg in self.products_tab_widgets.items():
            self.products_tab.addTab(widg, name.capitalize())

        # Setting up central widget things
        self.setCentralWidget(QtWidgets.QWidget(self))
        # Main layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.products_tab)        

        self.centralWidget().setLayout(vbox)
        
    ## Setters/Setters
    @property
    def products(self):
        return self._products
    
    @products.setter
    def products(self, products: dict[str, list[Sandwich | Sushi | Drink | Special]]):
        # NOTE: This is probably better done with a ProductCategory class but whatever
        for key in products.keys():
            assert key in self.ACCEPTABLE_KEYS, f"'{key}' is an unacceptable key."
            
        # All goods
        self._products = products


def main():

    # NOTE: This is probably better done with a ProductCategory class but whatever
    sandwiches = [
        Sandwich("Ham & egg sandwich", 3.50),
        Sandwich("Chicken mayo sandwich", 3.50),
        Sandwich("Egg sandwich", 3.00, ProductAttribute.VEGETARIAN),
        Sandwich("Beef sandwich", 3.80),
        Sandwich("Salad sandwich", 3.20, ProductAttribute.VEGAN | ProductAttribute.VEGETARIAN),
    ]

    sushi = [
        Sushi(SushiType.PIECES, "Chicken", 4.5, pieces=3),
        Sushi(SushiType.PIECES, "Tuna", 4.5, pieces=3),
        Sushi(SushiType.PIECES, "Avocado", 4.8, ProductAttribute.VEGAN | ProductAttribute.VEGETARIAN, pieces=3),
        Sushi(SushiType.BOWL, "Chicken rice", 5.5, pieces=3),
        Sushi(SushiType.BOWL, "Vegetarian rice", 5.5, ProductAttribute.VEGAN | ProductAttribute.VEGETARIAN)
    ]

    drinks = [
        Drink("Soda can", 2.00, ProductAttribute.VEGAN | ProductAttribute.VEGETARIAN | ProductAttribute.HAS_SUGAR),
        Drink("Aloe vera drink", 3.50, ProductAttribute.VEGETARIAN | ProductAttribute.HAS_SUGAR),
        Drink("Chocolate Milk", 3.50, ProductAttribute.HAS_SUGAR),
        Drink("Water Bottle", 2.50, ProductAttribute.VEGAN | ProductAttribute.VEGETARIAN),
        Drink("Instant hot chocolate", 1.50, ProductAttribute.VEGETARIAN | ProductAttribute.HAS_SUGAR)
    ]

    specials = [
        Special(Day.MONDAY,    "Samoa", "Kale moa",             6.00, ProductAttribute.HAS_SUGAR),
        Special(Day.TUESDAY,   "South Africa", "Potjiekos",     6.00, ProductAttribute.NONE),
        Special(Day.WEDNESDAY, "New Zealand (Māori)", "Hangi",  6.00, ProductAttribute.VEGETARIAN | ProductAttribute.VEGAN),
        Special(Day.THURSDAY,  "India", "Paneer tikka masala",  6.00, ProductAttribute.VEGETARIAN | ProductAttribute.HAS_SUGAR),
        Special(Day.FRIDAY,    "China", "Chow mein",            6.00, ProductAttribute.VEGETARIAN | ProductAttribute.VEGAN)
    ]

    app = QtWidgets.QApplication()
    main = KaiUI({
        "sandwiches": sandwiches, "sushi": sushi, "drinks": drinks, "specials": specials})

    main.show()
    app.exec()
    
if __name__ == "__main__":
    main()
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