from graphene import ObjectType, String, Int, Float

class Product(ObjectType):
    id = Int()
    name = String()
    sku = String()
    price = Float()
    quantity = Int()