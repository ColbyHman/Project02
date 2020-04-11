import InventorySystem_pb2
import InventorySystem_pb2_grpc

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
        return InventorySystem_pb2.Product(id = self.id, name = self.name,
        description = self.description, manufacturer = self.manufacturer,
        wholesale = self.wholesale, sale = self.sale, stock = self.stock)