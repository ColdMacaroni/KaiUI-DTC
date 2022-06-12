##
# main.py
# 2022-05-25
# A cool shop in Qt6 :D
# Please read every single line of code.

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
    def __init__(
        self,
        name: str,
        price: float,
        attributes: ProductAttribute = ProductAttribute.NONE,
    ):
        self.attributes = attributes | ProductAttribute.NONE
        self.name = name
        self.price = price

    @property
    def pretty_name(self):
        return self.name

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
    
    @property
    def pretty_name(self):
        if self.type is SushiType.BOWL:
            return f"{self.name} bowl"
        elif self.type is SushiType.PIECES:
            return f"{self.name} sushi ({self.pieces} pcs)"


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


class ProductInfo(QtWidgets.QFrame):
    def __init__(self, product: Product, *args):
        super().__init__(*args)

        # Im not gonna bother with a setter because i think its better if it just doesnt change
        assert isinstance(
            product, Product
        ), f"{product} should be type an instance of Product"
        self.product = product
        self.type = type(product)

        # Use a central widget of sorts so that the frame occupies the full width
        self.main_widget = QtWidgets.QWidget()

        # TODO: Image label

        self.name_label = QtWidgets.QLabel(self.main_widget)
        self.price_label = QtWidgets.QLabel(self.main_widget)
        self.vegetarian_label = QtWidgets.QLabel(self.main_widget)
        self.vegan_label = QtWidgets.QLabel(self.main_widget)
        self.has_sugar_label = QtWidgets.QLabel(self.main_widget)
        
        self.add_button = QtWidgets.QPushButton(self.main_widget)
        self.remove_button = QtWidgets.QPushButton(self.main_widget)
        
        self.initUI()
    
    def set_add_button_clicked(self, func):
        """ this function connects the buttons signal to the one given
        sends this objects product as an argument"""
        self.add_button.clicked.connect(lambda: func(self.product))

    def set_remove_button_clicked(self, func):
        self.remove_button.clicked.connect(lambda: func(self.product))

    def initUI(self):
        self.setFrameStyle(QtWidgets.QFrame.StyledPanel)

        # If the top margin is 1, it just disappears for some reason
        # Setting it to 5 makes it constistently appear
        self.setContentsMargins(1, 5, 1, 1)
        # self.setLineWidth(2)

        # Set up labels
        # self.name_label.setText(self.product.name)
        self.name_label.setText(self.product.pretty_name)
        self.name_label.setStyleSheet("font-size: 15pt")

        self.price_label.setText(f"${self.product.price:.02f}")

        self.vegetarian_label.setText(
            # f"Vegetarian: {'✅' if self.product.attributes & ProductAttribute.VEGETARIAN else '❎'}"
            f"Vegetarian: {'Yes' if self.product.attributes & ProductAttribute.VEGETARIAN else 'No'}"
        )

        self.vegan_label.setText(
            # f"Vegan: {'✅' if self.product.attributes & ProductAttribute.VEGAN else '❎'}"
            f"Vegan: {'Yes' if self.product.attributes & ProductAttribute.VEGAN else 'No'}"
        )

        self.has_sugar_label.setText(
            # f"Sugar: {'✅' if self.product.attributes & ProductAttribute.HAS_SUGAR else '❎'}"
            f"Has sugar: {'Yes' if self.product.attributes & ProductAttribute.HAS_SUGAR else 'No'}"
        )

        main_hbox = QtWidgets.QHBoxLayout()

        # Shove em all into a layout
        vbox_info = QtWidgets.QVBoxLayout()

        # These keeps them all compact and stops them from being stretched
        vbox_info.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        vbox_info.addWidget(self.name_label)
        vbox_info.addWidget(self.price_label)
        vbox_info.addWidget(self.vegetarian_label)
        vbox_info.addWidget(self.vegan_label)
        vbox_info.addWidget(self.has_sugar_label)

        main_hbox.addLayout(vbox_info)
        main_hbox.addStretch(1)

        vbox_buttons = QtWidgets.QVBoxLayout()
        self.add_button.setText("Add")
        self.remove_button.setText("Remove")

        # Signals will be connected to a function in the main window
        vbox_buttons.addWidget(self.add_button)
        vbox_buttons.addWidget(self.remove_button)

        main_hbox.addLayout(vbox_buttons)

        # This is the central widget
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.main_widget)

        self.main_widget.setLayout(main_hbox)
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
    
    def update_order_info(func):
        """This decorator calls the function and then updates the listview and price label"""
        def f(self, *args, **kwargs):
            func(self, *args, **kwargs)

            self.update_order_listwidget()
            self.update_price_label()
            
    def __init__(
        self, products: dict[str, list[Sandwich | Sushi | Drink | Special]], *args
    ):
        """
        This init only creates the objects needed for the ui, method initUI creates the layouts and
        actually fits everything together.
        """
        # Do the thing
        super().__init__(*args)

        # This will use the product item as they key and the value will be how many of those
        self.order = dict()

        # 'Declare' the private one to avoid any possible issues with the setter
        self._products = {}
        self.products = products

        self.products_tab = QtWidgets.QTabWidget(self)

        # A QWidget for every possible tab
        self.products_tab_widgets = {
            key: QtWidgets.QScrollArea(self) for key in self.ACCEPTABLE_KEYS
        }

        self.order_info_main_widget = QtWidgets.QWidget(self)

        self.order_info_order_listwidget = QtWidgets.QListWidget()
        self.order_info_order_listwidget
        self.order_info_price_label = QtWidgets.QLabel(self)
        self.order_info_order_button = QtWidgets.QPushButton(self)

        self.initUI()
    
    def add_to_order(self, product: Product):
        # This epic one liner will set the value to 1 if the key doesnt exist or increase it by 1 if it does
        self.order[product] = self.order.get(product, 0) + 1

    def order_button_clicked(self):
        # TODO: Export to json or smth, not my problem
        self.order.clear()

    def product_button_add_clicked(self, product: Product):
        self.add_to_order(product)
        self.update_order_listwidget()
        self.update_price_label()
    
    def product_button_remove_clicked(self, product: Product):
        # Nothing to do
        if product not in self.order:
            return

        # Remove one
        self.order[product] -= 1  

    def update_order_listwidget(self):
        idx = self.order_info_order_listwidget.currentRow()
        self.order_info_order_listwidget.clear()
        
        # Add them in alphabetical order
        for key, val in self.order.items():
            # Only accept natural numbers
            if not val > 0:
                continue
            
            self.order_info_order_listwidget.addItem(f"{key.pretty_name} x{val}")
            
        self.order_info_order_listwidget.setCurrentRow(idx)
            

    def update_price_label(self):
        price = 0
        for product, num in self.order.items():
            price += product.price * num

        self.order_info_price_label.setText(f"Total: ${price:.02f}")

    def setup_tab_widget(self, key):
        """
        Adds all the necessary widgets from the products dict to the products tab QWidget
        that has the same key
        """
        tab_widg = self.products_tab_widgets[key]
        tab_widg.setWidgetResizable(True)

        container_widget = QtWidgets.QWidget(tab_widg)

        sub_products = self.products[key]
        vbox = QtWidgets.QVBoxLayout()

        for p in sub_products:
            widg = ProductInfo(p, container_widget)
            
            # Connect Add and Remove button signals
            # This is done inside the object itself because on a for loop with a lambda function, the lambda
            # would always call the connected function with the loop's last value. Not what we want.
            # Doing it this way avoids that.
            widg.set_add_button_clicked(self.product_button_add_clicked)
            widg.set_remove_button_clicked(self.product_button_remove_clicked)
            # widg.add_button.clicked.connect(lambda: self.product_button_add_clicked(widg.product))
            # widg.remove_button.clicked.connect(lambda: self.product_button_remove_clicked(widg.product))

            vbox.addWidget(widg)
            
        container_widget.setLayout(vbox)
        tab_widg.setWidget(container_widget)

    def initUI(self):
        self.setWindowTitle("Kai")

        # Make it a *nice* window size
        self.setGeometry(QtCore.QRect(200, 100, 800, 600))

        # Set tab names, and add a tab to the thing
        for name, widg in self.products_tab_widgets.items():
            self.products_tab.addTab(widg, f"{name.capitalize()}")

            # This puts the actual objects into it
            self.setup_tab_widget(name)

        # Setting up central widget things
        self.setCentralWidget(QtWidgets.QWidget(self))

        # Main layout
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.products_tab)
        
        # This will make the product tabs occupy two thirds of the window width by default
        # and then grow more than the list widget
        hbox.setStretch(0, 2)        

        # Layout of sidebar
        order_vbox = QtWidgets.QVBoxLayout()
        self.order_info_main_widget.setLayout(order_vbox)

        # Add stretch at the beggining to offset the stretch before the button
        order_vbox.addStretch(1)
        
        order_vbox.addWidget(self.order_info_order_listwidget)
        
        self.update_price_label()
        order_vbox.addWidget(self.order_info_price_label)

        # I want the button at the bottom
        order_vbox.addStretch(1)

        self.order_info_order_button.setText("Order")
        order_vbox.addWidget(self.order_info_order_button)

        hbox.addWidget(self.order_info_main_widget)
        self.centralWidget().setLayout(hbox)

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
    # TODO: Put all of this into a json, its giving me a headache just looking at it
    # fmt:off
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
    # fmt:on

    app = QtWidgets.QApplication()
    main = KaiUI(
        {
            "sandwiches": sandwiches,
            "sushi": sushi,
            "drinks": drinks,
            "specials": specials,
        }
    )

    main.show()
    app.exec()


if __name__ == "__main__":
    main()
