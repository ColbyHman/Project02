import xmlrpc.client



# Setups the connection to the server. You can also do system.listMethods()
# Will be able to use getOrder, createOrder, and updateOrder


with xmlrpc.client.ServerProxy("") as proxy:
    print("You are connected to the server")
