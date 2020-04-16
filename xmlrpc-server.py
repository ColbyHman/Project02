from xmlrpc.server import SimpleXMLRPCServer
from Order import Order
from Product import Product
import random
import pickle
import uuid
import os


class InventorySystem():


    database = {}
    orders = {}

    ##################
    ##Server Methods##
    ##################

    def __init__(self):
        # if os.path.exists("database.pickle"):
        #     self.loadDatabaseFromPickle()
        # else:
        #     self.fillStock()
        self.fillStock()
        print(self.database)



    def fillStock(self):
            self.addProduct("Widget", "This is a Widget", "Widget & Co", "20.00", "3.50",300)
            self.addProduct("Gadget", "This is a Gadget", "Gadget & Co", "30.00", "5.50",300)
            self.addProduct("Trinket", "This is a Trinket", "Trinket & Co", "10.00", "0.50",300)
            self.addProduct("Widget", "This is a Widget", "Widget & Co", "20.00", "3.50",300)


    def saveDatabseToFile(self):
        with open('database.pickle', 'wb') as db_file:
            pickle.dump(self.database, db_file)

        with open('orders.pickle', 'wb') as order_file:
            pickle.dump(self.orders, order_file)

        
    def loadDatabaseFromPickle(self):
        with open('database.pickle', 'rb') as db_file:
            self.database = pickle.load(db_file)

        with open('orders.pickle', 'rb') as order_file:
            self.orders = pickle.load(order_file)
        

    def getProductByName(self, name):
            for product in self.database.keys():
                if name == product[1]:
                    return self.database.get(product)
            return None


    def getProductByID(self, id):
            for product in self.database.keys():
                if id == product[0]:
                    return self.database.get(product)
            return None


    def getProductByManufacturer(self, manufacturer):
            for product in self.database.values():
                if product.getManufacturer == manufacturer:
                    return product


    def addProduct(self, name, description, manufacturer, wholesale, sale, stock):
            if not self.checkNames(name):
                id_ = str(uuid.uuid4())
                product = Product(id_, name, description, manufacturer, wholesale, sale, stock)
                self.database.update({(id_, name): product})


    def checkNames(self, name):
            for product in self.database.values():
                if name == product.name:
                    return True
            return False


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


   



    ###################################
    ###Client Accessisble Methods######
    ###################################


    def getStock(self): 
            for product in self.database.values():
                if product.stock > 0:
                    yield product.productToString()

    def createOrder(self, destination, date, productsToAdd, isPaid, isShipped):
        print(destination)
        orderID = str(uuid.uuid4())
        newOrder = Order(orderID, destination, date, {}, isPaid, isShipped)
        print("Order Created")
        for item in productsToAdd.items():
            product, numOfProducts = item
            product = self.getProductByName(product)
            if numOfProducts <= product.stock:
                newOrder.addProduct(product.name, numOfProducts)
                self.updateProduct(product, "stock", (product.stock-numOfProducts))
            else:
                print("could not add")
        print("Products added")
        self.orders.update({orderID : newOrder})
        print("Order databse updated")
        return newOrder.orderToString()

    def getOrder(self, orderID):
            order = self.orders.get(orderID)
            return order.orderToString()

    def updateOrderAddProducts(self, orderID, productsToAdd):
            order = self.orders.get(orderID)
            for item in productsToAdd.items():
                product, numOfProducts = item
                product = self.getProductByName(product)
                if numOfProducts <= product.stock:
                    order.addProduct(product.name, numOfProducts)
                    self.updateProduct(product, "stock", (product.stock-numOfProducts))
                else:
                    print("Could not add " + product.name + ": not enough in stock")
            self.orders.update({orderID : order})
            return order.orderToString() 

    def updateOrderRemoveProducts(self, orderID, productsToRemove):
            order = self.orders.get(orderID)
            for item in productsToRemove.items():
                product, numOfProducts = item
                product = self.getProductByName(product)
                if product.name in order.products.keys():
                    order.removeProduct(product.name, numOfProducts)
                    self.updateProduct(product, "stock", (product.stock+numOfProducts))
                else:
                    print("Could not remove "+product.name+": not in your order")
            self.orders.update({orderID : order})
            return order.orderToString()

    def updateOrderChangeDestination(self, orderID, destination):
            order = self.orders.get(orderID)
            order.changeDestination(destination)
            return order.orderToString()

    def updateOrderChangeDate(self, orderID, date): 
            order = self.orders.get(orderID)
            order.changeDate(date)
            return order.orderToString()
            
    def updateOrderIsShipped(self, orderID, isShipped):
            order = self.orders.get(orderID)
            order.setShipped(isShipped)
            return order.orderToString()

    def updateOrderIsPaid(self, orderID, isPaid):
            order = self.orders.get(orderID)
            order.setPaid(isPaid)
            return order.orderToString()


def main():

    ####
    # The part below sets up the server and make sure it runs forever until you close it. 
    ####

    with SimpleXMLRPCServer(("localhost", 50052)) as server:
        inventorySystem = InventorySystem()
        server.register_instance(inventorySystem)
        server.register_multicall_functions()

        # server.register_function(InventorySystem.getStock)
        # server.register_function(InventorySystem.createOrder)
        # server.register_function(InventorySystem.getOrder)
        # server.register_function(inventorySystem.updateOrderAddProducts)
        # server.register_function(inventorySystem.updateOrderRemoveProducts)
        # server.register_function(inventorySystem.updateOrderChangeDestination)
        # server.register_function(inventorySystem.updateOrderChangeDate)
        # server.register_function(inventorySystem.updateOrderIsShipped)
        # server.register_function(inventorySystem.updateOrderIsPaid)
        while True:
            try:
                server.handle_request()
            except KeyboardInterrupt:
                inventorySystem.saveDatabseToFile()
                exit(0)
            

if __name__ == "__main__":
    main()