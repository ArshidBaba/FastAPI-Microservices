from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host="redis-17583.c281.us-east-1-2.ec2.cloud.redislabs.com",
    port=17583,
    password="6MqaklaHYtFncGaKfW79Ka0z4U6G9aFM",
    decode_responses=True,
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
    }


@app.post("/products")
def create(product: Product):
    return product.save()


@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)


@app.delete("/products/{pk}")
def delete(pk: str):
    return Product.delete(pk)
