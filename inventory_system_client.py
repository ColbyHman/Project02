import argparse
import grpc
import InventorySystem_pb2
import InventorySystem_pb2_grpc


def getStock(stub):
    for response in stub.getStock(InventorySystem_pb2.Empty()): 
        print(response)

def createOrder(stub, destination, date, products):
    response = stub.createOrder(InventorySystem_pb2.Order(orderID="", destination=destination, 
    date=date, products=products, isPaid=False, isShipped=False)) 
    print(response) 

def getOrder(stub, orderID):
    response = stub.getOrder(InventorySystem_pb2.orderID(id=orderID))
    print(response)

def addProducts(stub, orderID, products):
    response = stub.updateOrderAddProducts(InventorySystem_pb2.AddProducts(orderID=orderID, products=products))
    print(response)

def removeProducts(stub, orderID, products):
    response = stub.updateOrderRemoveProducts(InventorySystem_pb2.RemoveProducts(orderID=orderID, products=products))
    print(response)

def changeDestination(stub, orderID, destination):
    response = stub.updateOrderChangeDestination(InventorySystem_pb2.ChangeDestination(orderID=orderID, destination=destination))
    print(response)

def changeDate(stub, orderID, date):
    response = stub.updateOrderChangeDate(InventorySystem_pb2.ChangeDate(orderID=orderID, date=date))
    print(response)



def main():

    """
    Important Notes
    """


    """
    Arg Parse Section - Grab the Host, Method name, and whatever else is needed from the user. 
    """
    parser = argparse.ArgumentParser(description="Inventory System Client")
    parser.add_argument("--host", help="Hostname for the server", default="localhost")
    parser.add_argument("--port", help="Port for the server", default="50051")

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
    hostname = args.host + ":" + args.port
    with grpc.insecure_channel(hostname) as channel:
        stub = InventorySystem_pb2_grpc.InventorySystemStub(channel)
        try:
            if args.cmd == 'getStock':
                getStock(stub)
            elif args.cmd == "createOrder":
                products = dict(item.split(":") for item in args.products.split(","))
                for item in products.items():
                    products.update({item[0]:int(item[1])})
                createOrder(stub, args.destination, args.date, products)
            elif args.cmd == "getOrder":
                getOrder(stub, args.orderID)
            elif args.cmd == "addProducts":
                products = dict(item.split(":") for item in args.products.split(","))
                for item in products.items():
                    products.update({item[0]:int(item[1])})
                addProducts(stub, args.orderID, products)
            elif args.cmd == "removeProducts":
                products = dict(item.split(":") for item in args.products.split(","))
                for item in products.items():
                    products.update({item[0]:int(item[1])})
                removeProducts(stub, args.orderID, products)
            elif args.cmd == "changeDestination":
                changeDestination(stub, args.orderID, args.destination)
            elif args.cmd == "changeDate":
                changeDate(stub, args.orderID, args.date)
        except grpc._channel._InactiveRpcError as error:
            print(error)

if __name__ == "__main__":
    main()