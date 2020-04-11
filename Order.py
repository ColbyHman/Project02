import InventorySystem_pb2
import InventorySystem_pb2_grpc

class Order():

    def __init__(self, id, destination, date, products, isPaid, isShipped):
        self.id = id
        self.destination = destination
        self.date = date
        self.products = products
        self.isPaid = isPaid
        self.isShipped = isShipped

    def addProduct(self, product, quantity):
        self.products.update({product: quantity})
    
    def removeProduct(self, product):
        self.products.remove(product)
    
    def changeDate(self, date):
        self.date = date

    def changeDestination(self, destination):
        self.destination = destination
    
    def setPaid(self):
        self.isPaid = True

    def setShipped(self):
        self.isShipped = True

    def returnOrder(self):
        return InventorySystem_pb2.Order(orderID = self.id, destination = self.destination,
        date = self.date, products=self.products, isPaid = self.isPaid, isShipped = self.isShipped)