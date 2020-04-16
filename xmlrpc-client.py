import xmlrpc.client
import argparse




##################
##Server Methods##
##################

def getStock(server):
    for response in server.getStock():
        print(response)
    

def createOrder(server, destination, date, products):
    print("Function called")
    print(server)
    response = server.createOrder(destination, date, products, False, False) 
    print(response) 

def getOrder(server, orderID):
    response = server.getOrder(orderID)
    print(response)

def addProducts(server, orderID, products):
    response = server.updateOrderAddProducts(orderID, products)
    print(response)

def removeProducts(server, orderID, products):
    response = server.updateOrderRemoveProducts(orderID, products)
    print(response)

def changeDestination(server, orderID, destination):
    response = server.updateOrderChangeDestination(orderID, destination)
    print(response)

def changeDate(server, orderID, date):
    response = server.updateOrderChangeDate(orderID, date)
    print(response)



def main():
    ###################################
    ###Client Accessisble Methods######
    ###################################

    """
    Arg Parse Section - Grab the Host, Method name, and whatever else is needed from the user. 
    """
    parser = argparse.ArgumentParser(description="Inventory System Client")
    parser.add_argument("--host", help="Hostname for the server", default="localhost")
    parser.add_argument("--port", help="Port for the server", default="50052")

    subparser = parser.add_subparsers(title="method", dest="cmd", required=True)
    subparser.add_parser(name='getStock', description="Retrieves the current stock from the server")

    create_order = subparser.add_parser(name="createOrder", description="Create an order in the system")
    create_order.add_argument("destination", help="The destination of the order")
    create_order.add_argument("date", help="The date in which you wish the order to be shipped")
    create_order.add_argument("products", help="List of products you wish to order\nList them in the following fashion: \"<Name>\":<number of items>,\"<Name>\":<number of items>")

    get_order = subparser.add_parser(name="getOrder", description="Retrieve an order from the system")
    get_order.add_argument("orderID", help="The ID of the Order you wish to retrieve")

    add_products = subparser.add_parser(name="addProducts", description="Add products to an existing order")
    add_products.add_argument("orderID", help="The ID of the Order you wish to add products to")
    add_products.add_argument("products", help="List of products you wish to order\nList them in the following fashion: \"<Name>\":<number of items>,\"<Name>\":<number of items>")

    remove_products = subparser.add_parser(name="removeProducts", description="Remove products from an existing order")
    remove_products.add_argument("orderID", help="The ID of the Order you wish to remove products from")
    remove_products.add_argument("products", help="List of products you wish to remove\nList them in the following fashion: \"<Name>\":<number of items>,\"<Name>\":<number of items>")

    change_destination = subparser.add_parser(name="changeDestination", description="Change the destination of an order")
    change_destination.add_argument("orderID", help="The ID of the Order you wish to change the destination of")
    change_destination.add_argument("destination", help="The desired destination you wish to set for your order")

    change_date = subparser.add_parser(name="changeDate", description="Change the date of an order")
    change_date.add_argument("orderID", help="The ID of the Order you wish to change the date of")
    change_date.add_argument("date", help="The desired date you wish to set for your order")

    args = parser.parse_args()
    hostname = "http://" + args.host + ":" + args.port + "/"
    server = xmlrpc.client.ServerProxy(hostname)
    with server:
        print("You are connected to the server")
        try:
            if args.cmd == 'getStock':
                getStock(server)
            elif args.cmd == "createOrder":
                products = dict(item.split(":") for item in args.products.split(","))
                for item in products.items():
                    products.update({item[0]:int(item[1])})
                createOrder(server, args.destination, args.date, products)
            elif args.cmd == "getOrder":
                getOrder(server, args.orderID)
            elif args.cmd == "addProducts":
                products = dict(item.split(":") for item in args.products.split(","))
                for item in products.items():
                    products.update({item[0]:int(item[1])})
                addProducts(server, args.orderID, products)
            elif args.cmd == "removeProducts":
                products = dict(item.split(":") for item in args.products.split(","))
                for item in products.items():
                    products.update({item[0]:int(item[1])})
                removeProducts(server, args.orderID, products)
            elif args.cmd == "changeDestination":
                changeDestination(server, args.orderID, args.destination)
            elif args.cmd == "changeDate":
                changeDate(server, args.orderID, args.date)
        except xmlrpc.client.ProtocolError as e:
            print(e.errmsg)
            
if __name__ == "__main__":
    main()