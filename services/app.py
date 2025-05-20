from flask import Flask, jsonify, request
import iris

app = Flask(__name__)
# Number of days since roasting for the coffee to be considered "stale"
MAXAGE = 5

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Coffee Company Tutorial! :)"

@app.route('/inventory/listbeans', methods=['GET'])
def list_raw_beans():
    itemsarray = []
    sqlquery = "SELECT ID, vendor_product_code, date_arrival, SUM(quantity_kg) AS quantity_kg FROM ICO.inventory GROUP BY vendor_product_code ORDER BY date_arrival"
    rset = iris.sql.exec(sqlquery) 
    for row in rset:
        itemsarray.append(
            {
                "id": row[0],
                "vendor_product_code": row[1],
                "date_arrival": row[2],
                "quantity_kg": row[3]
            }
        )
    itemsobj = {
        "rowcount": len(itemsarray),
        "items": itemsarray
    }
    return jsonify(itemsobj)

@app.route('/catalog/catalogproduct', methods=['POST'])
def catalog_product():
    # Get HTTP POST content as JSON (with error handling)
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return jsonify({'msg': 'Content type is not supported.: '+content_type}), 403
    
    json_data = request.json
    if not json_data:
        return jsonify({'error': 'No JSON body in request'}), 400
    
    # Here you would typically process the incoming data and add a new product to the catalog
    # Construct a new ICO.catalog object and populate it from the input
    fieldnamesql = "INSERT INTO ICO.catalog (product_code, quantity, price, time_roasted, roasting_notes, img)"
    try:
        valsql = fieldnamesql + " VALUES ("
        valsql += "'" + json_data["product_code"] + "', "
        valsql += str(json_data["quantity"]) + ", "
        valsql += str(json_data["price"]) + ", "
        valsql += "TO_TIMESTAMP('" + json_data["time_roasted"] + "', 'YYYY-MM-DD hh:mi:ss'), "
        valsql += "'" + json_data["roasting_notes"] + "', "
        valsql += "'" + json_data["img"] + "')"
        iris.sql.exec(valsql) 
    except Exception as exp:
        return jsonify({'error': exp}), 400

    return jsonify({"message": "Product added to catalog", "data": json_data}), 201

@app.route('/catalog/getproducts', defaults={'is_fresh': 1}, methods=['GET'])
@app.route('/catalog/getproducts/<int:is_fresh>', methods=['GET'])
def get_products(is_fresh):
    sqlquery = "SELECT catalog_id, product_code, quantity, price, time_roasted, roasting_notes, img FROM ICO.catalog"
    # set the WHERE clause based on whether we want fresh or not (the -? will be replaced by MAXAGE)
    if is_fresh==1:
        sqlquery = sqlquery + " WHERE time_roasted > DATEADD('day',-" + str(MAXAGE) + ",CURRENT_DATE)"
    else:
        sqlquery = sqlquery + " WHERE time_roasted <= DATEADD('day',-" + str(MAXAGE) + ",CURRENT_DATE)"
    # if nothing is left, exclude from the response
    sqlquery = sqlquery + " AND quantity > 0"
    # run the query
    rset = iris.sql.exec(sqlquery)
    itemsarray = []
    # iterate over the results and build a dynamic array
    for row in rset:
        itemsarray.append(
            {
                "catalog_id": row[0],
                "product_code": row[1],
                "quantity": row[2],
                "time_roasted": row[4],
                "roasting_notes": row[5],
                "img": row[6],
                "price": row[3]
            }
        )
    itemsobj = {
        "rowcount": len(itemsarray),
        "items": itemsarray
    }
    return jsonify(itemsobj)

@app.route('/catalog/sellproduct/<string:catalog_id>/<int:quantity>', methods=['GET'])
def sell_product(catalog_id, quantity):

    try:
        sql = "SELECT COUNT(catalog_id) FROM ICO.catalog WHERE catalog_id = "+str(catalog_id)
        res = iris.sql.exec(sql)
        for idx, row in enumerate(res):
            # does the ID exist?
            if row[0] < 1:
                return jsonify({'error': "No id: "+str(catalog_id)}), 404
            # do we have enough quantity?
            else:
                sql = "SELECT * FROM ICO.catalog WHERE catalog_id = "+str(catalog_id)
                res = iris.sql.exec(sql)
                for idx, item in enumerate(res):
                    if (quantity > item[2]):
                        return jsonify({"error": "You tried to get "+str(quantity)+" bags, but we only have "+str(item[2])+" available."}),400
                    else:
                        # decrement the database and return the new quantity
                        sql = "UPDATE ICO.catalog SET quantity=(quantity-"+str(quantity)+") WHERE catalog_id = "+str(catalog_id)
                        res = iris.sql.exec(sql)
                        # return new record
                        sql = "SELECT * FROM ICO.catalog WHERE catalog_id = "+str(catalog_id)
                        res = iris.sql.exec(sql)
                        x = []
                        for idx, item in enumerate(res):
                            x.append({
                                "catalog_id": item[0],
                                "product_code": item[1],
                                "quantity": item[2],
                                "price": item[3], 
                                "time_roasted": item[4], 
                                "roasting_notes": item[5], 
                                "img": item[6]
                            })
                        return jsonify(x), 200
    except Exception as exp:
        return jsonify({'error': exp}), 400

if __name__ == '__main__':
    app.run(debug=True)