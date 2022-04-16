GET_INVENTORY_QUERY = "SELECT id, name, description, quantity, price FROM inventory, items WHERE id = item_id;"

GET_SHIPMENTS_QUERY = """SELECT shipments.id as shipment_id, item_id, name, quantity, time_created
                         FROM shipments, items
                         WHERE item_id = items.id
                         ORDER BY time_created DESC;"""

GET_ITEMS_QUERY = "SELECT * FROM items;"

CREATE_SHIPMENT_QUERY = "INSERT INTO shipments (item_id, quantity, time_created) VALUES (?, ?, CURRENT_TIMESTAMP)"

CREATE_ITEM_QUERY = "INSERT INTO items (name, description, price) VALUES (?, ?, ?);"

EDIT_ITEM_QUERY = "UPDATE items SET name = ?, description = ?, price = ? WHERE id = ?;"

DELETE_ITEM_QUERY = "DELETE FROM items WHERE id = ?;"

MODIFY_INVENTORY_QUERY = "UPDATE inventory SET quantity = ? WHERE item_id = ?;"
