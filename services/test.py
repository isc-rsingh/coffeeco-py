import iris
from flask import Flask, jsonify

is_fresh = 1
MAXAGE = 5
product_id = 18
quantity = 4433

sql = "SELECT * FROM ICO.catalog WHERE catalog_id = "+str(product_id)
res = iris.sql.exec(sql)
for idx, item in enumerate(res):
    if item[0] < 1:
        print("No id: "+str(product_id))
    else:
        print("Found id: "+str(product_id))
        if (quantity > item[2]):
            print("You tried to get "+str(quantity)+" bags, but we only have "+str(item[2])+" available.")
