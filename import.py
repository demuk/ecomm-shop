import csv
import os

from kapsuchai import db
from kapsuchai.models import Products


def main():
    f = open("products.csv")
    reader = csv.reader(f)
    for name, price, description in reader:
        product = Products(name=name,price=price,description=description)
        db.session.add(product)
        print(f"Added product {name}, {price}, {description}")
    db.session.commit()


if __name__ == "__main__":
    main()
