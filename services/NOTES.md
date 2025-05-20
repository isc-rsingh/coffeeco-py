/usr/irissys/httpd/bin/httpd -k restart

curl -d product_brazil_dark.json -H "Content-Type: application/json" -X POST "http://localhost:52773/api/coffeeco/catalog/catalogproduct"

