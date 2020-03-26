# Project02
Grocery Store

XML-RPC / gRPC Server Functions:

save_pickle_to_file()

load_pickle()

getProductByID(int ID)

getProductByName(string Name)

getProductsByManufacturer(string Manu)

addProduct(string Name)
	checkNames()

checkNames(string Name)
	if name in products.keys()

updateProduct(String name, String field)
	do 4 ifs for the different fields

getStock()
	return all products with non-null inventory values

createOrder(Destination, Date, dict[product, count], if_paid, if_shipped)

createOrderID()
	checkPreviousIDs

getOrder(orderID)

updateOrder()
	important - if order # of prods > stock, block that action


Client Functionality:

getOrder

createOrder

updateOrder


Server Variables:

Orders

Stock


Product Class:

ID, Name, Description, Manufacturer, Wholesale Cost, Sale cost

Order Class:(?)
	ASK JEFF


Important Notes:

Create a Product Object Class

Both servers run on single file

Two SEPARATE clients

USE A LOT OF ARGPARSE
	That code should be the same for both clients

For testing the run time, create a test pickle file that
will allow the database to start from the same state
	Each should last 15 seconds each
	Run each client 3 times, from the same source, and take the median of the times
	Make sure database is "quite full (100s of products)"
