# Constants and SQL queries used for the project

GET_INVENTORY_QUERY = "SELECT id, name, description, quantity, price FROM inventory, items WHERE id = item_id;"

CREATE_INVENTORY_QUERY = "INSERT INTO inventory (item_id, quantity) VALUES (?, 0);"

GET_SHIPMENTS_QUERY = """SELECT shipments.id as shipment_id, item_id, name, quantity, time_created
                         FROM shipments, items
                         WHERE item_id = items.id
                         ORDER BY time_created DESC;"""

GET_ITEMS_QUERY = "SELECT * FROM items;"

GET_ITEM_QUERY = "SELECT * FROM items WHERE id = ?;"

GET_INVENTORY_QTY_QUERY = "SELECT quantity FROM inventory WHERE item_id = ?;"

CREATE_SHIPMENT_QUERY = "INSERT INTO shipments (item_id, quantity, time_created) VALUES (?, ?, CURRENT_TIMESTAMP)"

CREATE_ITEM_QUERY = "INSERT INTO items (name, description, price) VALUES (?, ?, ?);"

UPDATE_ITEM_QUERY = "UPDATE items SET name = ?, description = ?, price = ? WHERE id = ?;"

DELETE_ITEM_QUERY = "DELETE FROM items WHERE id = ?;"

UPDATE_INVENTORY_QUERY = "UPDATE inventory SET quantity = quantity - ? WHERE item_id = ?;"
