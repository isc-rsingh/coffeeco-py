# InterSystems IRIS Full Stack in **Python**

In this tutorial, you create the basic information management infrastructure for a small manufacturing company. In this case, the company will be roasting, packaging and selling delicious, freshly roasted coffee beans. Along the way, you’ll learn how the InterSystems IRIS data platform can serve as the backbone of your IT architecture.

The QuickStart is divided into three parts and introduces the processes that you, as a coffee manufacturer, follow to set up everything from inventorying raw coffee beans to selling them in an online portal.

- **Part 1:** Write SQL to create and populate databases.
- **Part 2:** Build a RESTful API to handle business functions using Python.
- **Part 3:** Build an online storefront to sell your artisan coffee beans using the popular JavaScript framework, Vue.js.

![the 3 steps of the QuickStart](https://gettingstarted.intersystems.com/wp-content/uploads/2021/03/IrisCoffee-Sketch1-01.png)

## Part 1: Create and populate databases with SQL

IRIS Coffee Company has three major divisions in the company:

- the warehouse stores the raw coffee bean inventory. Its data will be in the table ICO.inventory
- the roastery roasts the beans, and doesn’t need to store data
- the storefront, where the company sells the roasted coffee. Its data will be in the table ICO.catalog

### Database creation

Let’s use the SQL client built into the InterSystems IRIS Terminal to create those two tables using SQL CREATE statements:

1. Open the Sandbox IDE -- cannot display value - please provision a sandbox
2. From the InterSystems menu, select Web Terminal
3. Log in with username tech and password demo
4. You should see a USER > command line prompt.
5. Type `/sql`.
6. Paste the following SQL CREATE statement and hit return.

 ```sql
 CREATE TABLE ICO.inventory
 (
 vendor_id VARCHAR(128),
 vendor_product_code VARCHAR(128),
 quantity_kg DECIMAL(10,2),
 date_arrival DATE
 )
 ```

If your query is successful, you will see Nothing to display, as CREATE statements don’t return anything

7. Copy and paste the following SQL CREATE statement to create ICO.catalog table and hit return.

```sql
CREATE TABLE ICO.catalog
(
catalog_id BIGINT IDENTITY,
product_code VARCHAR(128),
quantity INTEGER,
price DECIMAL(10,2),
time_roasted DATETIME,
roasting_notes VARCHAR(2048),
img VARCHAR(2048)
)
```

8. You can test a bit more by running SELECT * FROM ICO.inventory and SELECT * FROM ICO.catalog and you should get back a table with no rows (yet).
9. Type `/sql` again to exit SQL mode in the InterSystems IRIS Terminal.

### Python data loading

We want to populate the database with raw coffee bean orders, simulating shipments of raw beans from vendors around the world. Assume that all the shipments are consolidated in a single order manifest in JSON format.
Our manifest can be found at `setup/order_manifest.json`.

Run: `irispython manifest_importer.py`

You should see the following output.

```
Inserting: INSERT INTO ICO.inventory (vendor_id, vendor_product_code, quantity_kg, date_arrival) VALUES ('ETRADER', 'ETHIOPA32', 200, '[year-month-day]')
Inserting: INSERT INTO ICO.inventory (vendor_id, vendor_product_code, quantity_kg, date_arrival) VALUES ('BRZ221', 'BRAZILPREM', 100, '[year-month-day]')
Inserting: INSERT INTO ICO.inventory (vendor_id, vendor_product_code, quantity_kg, date_arrival) VALUES ('GMLPROD', 'GUATEMALAALT30', 100, '[year-month-day]')
Inserting: INSERT INTO ICO.inventory (vendor_id, vendor_product_code, quantity_kg, date_arrival) VALUES ('DKE', 'SUMATRA2', 100, '[year-month-day]')
Inserting: INSERT INTO ICO.inventory (vendor_id, vendor_product_code, quantity_kg, date_arrival) VALUES ('DKE', 'SUMATRA3', 200, '[year-month-day]')
```

## Part 2: Build a RESTful API to handle business functions using Python


## Part 3: Online storefront with Vue.js.