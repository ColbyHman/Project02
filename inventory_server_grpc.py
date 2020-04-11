import grpc
import InventorySystem_pb2
import InventorySystem_pb2_grpc
from Order import Order
from Product import Product
import pickle
from concurrent import futures
import uuid

class InventorySystem(InventorySystem_pb2_grpc.InventorySystemServicer):
    
    database = {}
    orders = {}

      ######################
     ####SERVER METHODS####
    ######################

    def fillStock(self):
        self.addProduct("Widget", "This is a Widget", "Widget & Co", "20.00", "3.50")
        self.addProduct("Gadget", "This is a Gadget", "Gadget & Co", "30.00", "5.50")
        self.addProduct("Trinket", "This is a Trinket", "Trinket & Co", "10.00", "0.50")
        self.addProduct("Widget", "This is a Widget", "Widget & Co", "20.00", "3.50")

    # Saves the database to a pickle file
    # TESTED
    def saveDatabaseToFile(self):
        with open('database.pickle', 'wb') as db_file:
            pickle.dump(self.database, db_file)

        with open('orders.pickle', 'wb') as order_file:
            pickle.dump(self.orders, order_file)

    # Loads the database from a pickle file
    # TESTED
    def loadDatabaseFromPickle(self):
        with open('database.pickle', 'rb') as db_file:
            self.database = pickle.load(db_file)

        with open('orders.pickle', 'rb') as order_file:
            self.orders = pickle.load(order_file)

    # Returns a product that matches a given ID, returns None if product does not exist
    # TESTED
    def getProductByID(self, id):
        for product in self.database.keys():
            if id == product[0]:
                return self.database.get(product)
        return None

    # Returns a product that matches a given name, returns None if product does not exist 
    # TESTED
    def getProductByName(self, name):
        for product in self.database.keys():
            if name == product[1]:
                return self.database.get(product)
        return None

    # Returns a product that matches a given manufacturer, returns None if product does not exist 
    # TESTED
    def getProductByManufacturer(self, manufacturer):
        for product in self.database.values():
            if product.getManufacturer == manufacturer:
                return product

    # Adds a product using given information, throws an error when product name already exists
    #TESTED
    def addProduct(self, name, description, manufacturer, wholesale, sale):
        if not self.checkNames(name):
            id_ = str(uuid.uuid4())
            product = Product(id_, name, description, manufacturer, wholesale, sale, 1)
            self.database.update({(id_, name): product})

    # Checks the names of all products and compares it to the given name to determine product existence
    #TESTED
    def checkNames(self, name):
        for product in self.database.values():
            if name == product.name:
                return True
        return False

    # Updates a product field
    # TESTED
    def updateProduct(self, product, field, value):
        if field == "description":
            product.description = value
        elif field == "manufacturer":
            product.manufacturer = value
        elif field == "wholesale":
            product.wholesale = value
        elif field == "sale":
            product.sale = value
        elif field == "stock":
            product.stock = value
        self.database.update({(product.name, product.id):product})

      ####################################
     ####CLIENT ACCESSISBLE METHODS######
    ####################################
    
    # Yield all products in stock - DONE
    #TESTED
    def getStock(self, request, context): 
        for product in self.database.values():
            if product.stock > 0:
                yield product.returnProduct()

    # Returns a new Order
    # TESTED
    def createOrder(self, request, context):
        orderID = str(uuid.uuid4())
        destination = request.destination
        date = request.date
        productsToAdd = request.products
        isPaid = request.isPaid
        isShipped = request.isShipped
        newOrder = Order(orderID, destination, date, {}, isPaid, isShipped)

        for item in productsToAdd.items():
            product, numOfProducts = item
            product = self.getProductByName(product)
            if numOfProducts <= product.stock:
                newOrder.addProduct(product.name, numOfProducts)
                self.updateProduct(product, "stock", (product.stock-numOfProducts))
            else:
                print("Could not add",product.name+": not enough in stock")

        self.orders.update({orderID : newOrder})
        print(newOrder.products)
        return newOrder.returnOrder()

    # Returns an order
    # NEEDS TO BE TESTED
    def getOrder(self, request, context):
        orderID = request.id
        order = self.orders.get(orderID)
        return order.returnOrder()

    # Returns order with added products
    # NEEDS TO BE TESTED
    def updateOrderAddProducts(self, request, context):
        orderID = request.order
        productsToAdd = request.products
        order = self.orders.get(orderID)
        for item in productsToAdd.items():
            product, numOfProducts = item
            product = self.getProductByName(product)
            if numOfProducts <= product.stock:
                order.addProduct(product, numOfProducts)
                self.updateProduct(product.name, stock, product.stock-numOfProducts)
            else:
                print("Could not add",product.name+": not enough in stock")
        return order

    # Returns order with removed products
    # NEEDS TO BE TESTED
    def updateOrderRemoveProducts(self, request, context):
        orderID = request.order
        productsToRemove = request.products
        order = self.orders.get(orderID)
        for item in productsToRemove:
            product, numOfProducts = item
            product = self.getProductByName(product)
            if numOfProducts <= product.stock:
                order.removeProduct(product, numOfProducts)
                self.updateProduct(product.name, stock, product.stock+numOfProducts)
        return order

    # Returns order with updated location
    # NEEDS TO BE TESTED
    def updateOrderChangeDestination(self, request, context):
        orderID = request.order
        destination = request.destination
        order = self.orders.get(orderID)
        order.changeDestination(destination)
        return order

    # Returns order with updated Date
    # NEEDS TO BE TESTED
    def updateOrderChangeDate(self, request, context): 
        orderID = request.order
        date = request.date
        order = self.orders.get(orderID)
        order.changeDate(date)
        return order

    # Returns order with updated shipping
    # NEEDS TO BE TESTED
    def updateOrderIsShipped(self, request, context):
        orderID = request.order
        isShipped = request.isShipped
        order = self.orders.get(orderID)
        order.setShipped(isShipped)
        return order

    # Returns order with updated payment
    # NEEDS TO BE TESTED
    def updateOrderIsPaid(self, request, context):
        orderID = request.order
        isPaid = request.isPaid
        order = self.orders.get(orderID)
        order.setPaid(isPaid)
        return order

def main():
    inventorySystem = InventorySystem()
    inventorySystem.fillStock()
    inventorySystem.saveDatabaseToFile()
    inventorySystem.loadDatabaseFromPickle()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    InventorySystem_pb2_grpc.add_InventorySystemServicer_to_server(inventorySystem, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        inventorySystem.saveDatabaseToFile()

if __name__ == "__main__":
    main()