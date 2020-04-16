class Product():

    def __init__(self, id_, name, description, manufacturer, wholesale, sale, stock):
        self.id = id_
        self.name = name
        self.description = description
        self.manufacturer = manufacturer
        self.wholesale = wholesale
        self.sale = sale
        self.stock = stock


    def updateManufacturer(self, manufacturer):
        self.manufacturer = manufacturer

    def updateWholesale(self, wholesale):
        self.wholesale = wholesale

    def updateSale(self, sale):
        self.sale = sale

    def returnProduct(self):
        return Product(id_ = self.id, name = self.name, description = self.description, manufacturer = self.manufacturer, wholesale = self.wholesale, sale = self.sale, stock = self.stock)

    def productToString(self):
        return "ID:{id}\nName:{name}\nDescription:{description}\nManufacturer:{manufacturer}\nWholesale:{wholesale}\nSale:{sale}\nStock:{stock}\n".format(id = self.id, name = self.name, description = self.description, manufacturer = self.manufacturer, wholesale = self.wholesale, sale = self.sale, stock = self.stock)





