class Order():

    def __init__(self, id, destination, date, products, isPaid, isShipped):
        self.id = id
        self.destination = destination
        self.date = date
        self.products = products
        self.isPaid = isPaid
        self.isShipped = isShipped

    def addProduct(self, product, quantity):
        if product in self.products:
            quantity += self.products.get(product)
        self.products.update({product: quantity})


    def removeProduct(self, product, quantity):
        orderQuantitiy = self.products.get(product)
        print(quantity,orderQuantitiy)
        if quantity >= orderQuantitiy:
            self.products.pop(product)
            print("Removed Completely")
        else:
            self.products.pop(product)
            self.products.update({product:orderQuantitiy - quantity})
            print("Removed Partially")

    def changeDate(self, date):
        self.date = date

    def changeDestination(self, destination):
        self.destination = destination

    def setPaid(self):
        self.isPaid = True

    def setShipped(self):
        self.isShipped = True

    def returnOrder(self):
        return Order(id = self.id, destination = self.destination, date = self.date, products=self.products, isPaid = self.isPaid, isShipped = self.isShipped)

    def orderToString(self):
        return "Order ID:{id}\nDestination:{destination}\nDate:{date}\nProducts:{products}\nisPaid:{isPaid}\nisShipped:{isShipped}\n".format(id = self.id, destination = self.destination, date = self.date, products=self.products, isPaid = self.isPaid, isShipped = self.isShipped)

        