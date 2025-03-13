from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel, Field
from pydantic import BaseModel

# Define the app
app = FastAPI()

# Connect to Redis
redis = get_redis_connection(
    host='redis-14467.c274.us-east-1-3.ec2.redns.redis-cloud.com',
    port=14467,
    decode_responses=True,
    username="default",
    password="hflUqyUQNjkYVbneX4D4TihchnI3k0Ss",
)

# Define Pydantic model for the response/requests
class ProductCreateRequest(BaseModel):
    name: str
    price: float
    quantity: int

class ProductResponse(BaseModel):
    name: str
    price: float
    quantity: int
    pk: str 

# Define the Redis-OM Product model
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis 


@app.get("/products", response_model=list[ProductResponse])
def all():
    pks = Product.all_pks()
    if pks:
        products = [Product.get(pk) for pk in pks]
        return [ProductResponse(name=product.name, price=product.price, quantity=product.quantity, pk=product.pk) for product in products]
    else:
        return {"message": "No products found"}

# FastAPI route to create a new product
@app.post("/products", response_model=ProductResponse)
def create(product: ProductCreateRequest):
    new_product = Product(name=product.name, price=product.price, quantity=product.quantity)
    new_product.save()
    return ProductResponse(name=new_product.name, price=new_product.price, quantity=new_product.quantity, pk=new_product.pk)

@app.delete('/products/{pk}')
def delete(pk:str):
    productss = Product.get(pk)
    return productss.delete(pk)
