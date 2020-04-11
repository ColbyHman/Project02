import grpc
import InventorySystem_pb2
import InventorySystem_pb2_grpc

with grpc.insecure_channel('localhost:50051') as channel: 
    stub = InventorySystem_pb2_grpc.InventorySystemStub(channel) 
    for response in stub.getStock(InventorySystem_pb2.Empty()): 
        print(response)

with grpc.insecure_channel('localhost:50051') as channel: 
    stub = InventorySystem_pb2_grpc.InventorySystemStub(channel) 
    response = stub.createOrder(InventorySystem_pb2.Order(orderID="1", destination="Wyckoff", 
    date="04-15-20", products={"Widget":1,"Trinket":10000}, isPaid=True, isShipped=True)) 
    print(response) 

with grpc.insecure_channel('localhost:50051') as channel: 
    stub = InventorySystem_pb2_grpc.InventorySystemStub(channel) 
    reponse = stub.getOrder(InventorySystem_pb2.orderID(id='0fda5d3c-f326-4df5-b5a7-2088989b46f8'))
    print(response)