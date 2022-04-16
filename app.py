from flask import Flask, render_template, request, redirect, url_for

import constants
import db

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
def index():
    conn = db.get_db_connection()
    inventory = db.execute_query(
        conn=conn,
        query=constants.GET_INVENTORY_QUERY
    ).fetchall()
    conn.close()
    return render_template('index.html', inventory=inventory)


@app.route('/shipments')
def shipments():
    conn = db.get_db_connection()
    shipments_data = db.execute_query(
        conn=conn,
        query=constants.GET_SHIPMENTS_QUERY
    ).fetchall()
    conn.close()
    return render_template('shipments.html', shipments=shipments_data)


@app.route('/shipments/create', methods=['GET', 'POST'])
def shipments_create():
    conn = db.get_db_connection()
    items = db.execute_query(
        conn=conn,
        query=constants.GET_ITEMS_QUERY
    ).fetchall()
    conn.close()
    if request.method == 'POST':
        # On shipment submission, first check for form validity (also done client-side; just in case)
        try:
            item_id = int(request.form['id'])
            quantity = int(request.form['quantity'])
            if request.form['direction'] not in ('in', 'out'):
                raise ValueError
        except ValueError:
            # Shouldn't happen unless someone is messing with the form!
            return render_template('shipments/create.html', items=items,
                                   error="Invalid form input; check your POST data.")
        if request.form['direction'] == 'in':
            quantity *= -1
        conn = db.get_db_connection()
        # Before committing the change, we need to make sure that we have enough inventory
        stock = int(db.execute_query(
            conn=conn,
            query=constants.GET_INVENTORY_QTY_QUERY,
            args=(item_id,)
        ).fetchone()['quantity'])
        # If the user does not have enough inventory, close and terminate early
        if stock - quantity < 0:
            conn.close()
            return render_template('shipments/create.html', items=items,
                                   error=f"You don't have enough inventory to do that! ({stock} available)")
        # Otherwise, commit both the shipment and the inventory change
        db.execute_query(
            conn=conn,
            query=constants.CREATE_SHIPMENT_QUERY,
            args=(item_id, quantity)
        )
        db.execute_query(
            conn=conn,
            query=constants.UPDATE_INVENTORY_QUERY,
            args=(quantity, item_id)  # Has to be flipped due to SQL syntax; see constants.py
        )
        conn.close()
        return render_template('shipments/create.html', items=items, success="Shipment created successfully!")
    return render_template('shipments/create.html', items=items)


@app.route('/shipments/advanced', methods=['GET', 'POST'])
def shipments_advanced():
    conn = db.get_db_connection()
    inventory = db.execute_query(
        conn=conn,
        query=constants.GET_INVENTORY_QUERY
    ).fetchall()
    conn.close()
    if request.method == 'POST':
        item_updates = []
        # Need to follow ACID: Fail one, fail all
        for item_key in request.form.keys():
            try:
                item_id = int(item_key.split('-')[0])
                quantity = int(request.form[item_key])
            except ValueError:
                return render_template('shipments/advanced.html', inventory=inventory,
                                       error="Invalid form input; check your POST data.")
            if quantity == 0:
                continue
            # Instead of re-querying, search for the item in the inventory variable
            # Can possibly be optimized by using a dictionary instead of a list
            for item in inventory:
                # Check if we have enough stock to fulfill the request
                if int(item['id']) == item_id and int(item['quantity']) - quantity < 0:
                    return render_template('shipments/advanced.html', inventory=inventory,
                                           error=f"You don't have enough inventory to do that!\n"
                                                 f"Failed for item {item['name']}: {item['quantity']} available,"
                                                 f"{quantity} requested")
                # Save the item_id and quantity for later
            item_updates.append((item_id, quantity))
        # If there were no changes, then we can just return
        if len(item_updates) == 0:
            return render_template('shipments/advanced.html', inventory=inventory,
                                   warning="No changes were made to inventory.")
        # If we made it this far, we can commit the changes
        conn = db.get_db_connection()
        db.execute_many(
            conn=conn,
            query=constants.CREATE_SHIPMENT_QUERY,
            args=item_updates
        )
        db.execute_many(
            conn=conn,
            query=constants.UPDATE_INVENTORY_QUERY,
            args=[(update[1], update[0]) for update in item_updates]
        )
        # Update displayed inventory
        inventory = db.execute_query(
            conn=conn,
            query=constants.GET_INVENTORY_QUERY
        ).fetchall()
        conn.close()
        return render_template('shipments/advanced.html', inventory=inventory,
                               success=f"{len(item_updates)} shipments created successfully!")
    return render_template('shipments/advanced.html', inventory=inventory)


@app.route('/manage')
def manage():
    conn = db.get_db_connection()
    items = db.execute_query(
        conn=conn,
        query=constants.GET_ITEMS_QUERY
    ).fetchall()
    conn.close()
    return render_template('manage.html', items=items)


@app.route('/manage/create', methods=['GET', 'POST'])
def manage_create():
    if request.method == 'POST':
        name, description, price = request.form['name'], request.form['description'], request.form['price']
        try:
            price = float(price)
            if not all((name, description, price)):
                return render_template('manage/create.html', error="Please fill out all fields.",
                                       name=name, description=description, price=price)
        except ValueError:
            return render_template('manage/create.html', error="Price must be a number.",
                                   name=name, description=description, price=price)
        conn = db.get_db_connection()
        cur = db.execute_query(
            conn=conn,
            query=constants.CREATE_ITEM_QUERY,
            args=(name, description, price)
        )
        db.execute_query(
            conn=conn,
            query=constants.CREATE_INVENTORY_QUERY,
            args=(cur.lastrowid,)
        )
        conn.close()
        return render_template('manage/create.html', success=f"Item {name} created successfully!")
    return render_template('manage/create.html')


@app.route('/manage/edit', methods=['GET', 'POST'])
def manage_edit():
    conn = db.get_db_connection()
    items = db.execute_query(
        conn=conn,
        query=constants.GET_ITEMS_QUERY
    ).fetchall()
    conn.close()
    if request.method == 'POST':
        if len(request.form) == 0:
            return render_template('manage/edit.html', items=items, warning="Please select an item to edit.")
        return redirect(url_for('manage_edit_item', item_id=request.form['edit']))
    return render_template('manage/edit.html', items=items)


@app.route('/manage/edit/<int:item_id>', methods=['GET', 'POST'])
def manage_edit_item(item_id):
    conn = db.get_db_connection()
    item = db.execute_query(
        conn=conn,
        query=constants.GET_ITEM_QUERY,
        args=(item_id,)
    ).fetchone()
    conn.close()
    if request.method == 'POST':
        try:
            name, description, price = request.form['name'], request.form['description'], float(request.form['price'])
            if not all((name, description, price)):
                return render_template('manage/edit_details.html', item=item, error="Please fill out all fields.")
        except ValueError:
            return render_template('manage/edit_details.html', item=item, error="Price must be a number.")
        conn = db.get_db_connection()
        db.execute_query(
            conn=conn,
            query=constants.UPDATE_ITEM_QUERY,
            args=(name, description, price, item_id)
        )
        item = db.execute_query(
            conn=conn,
            query=constants.GET_ITEM_QUERY,
            args=(item_id,)
        ).fetchone()
        conn.close()
        return render_template('manage/edit_details.html', item=item, success="Item details updated successfully!")
    return render_template('manage/edit_details.html', item=item)


@app.route('/manage/delete', methods=['GET', 'POST'])
def manage_delete():
    conn = db.get_db_connection()
    items = db.execute_query(
        conn=conn,
        query=constants.GET_ITEMS_QUERY
    ).fetchall()
    conn.close()
    if request.method == 'POST':
        if len(request.form) == 0:
            return render_template('manage/delete.html', items=items, warning="No changes were made to the items list.")
        try:
            item_deletes = [(key.split('-')[0],) for key in request.form]
        except ValueError:
            return render_template('manage/delete.html', items=items, error="Invalid form input; check your POST data.")
        print(item_deletes)
        conn = db.get_db_connection()
        db.execute_many(
            conn=conn,
            query=constants.DELETE_ITEM_QUERY,
            args=item_deletes
        )
        items = db.execute_query(
            conn=conn,
            query=constants.GET_ITEMS_QUERY
        ).fetchall()
        conn.close()
        if len(item_deletes) > 1:
            return render_template('manage/delete.html', items=items,
                                   success=f"Deleted {len(item_deletes)} items successfully!")
        else:
            return render_template('manage/delete.html', items=items,
                                   success=f"Deleted item successfully!")
    return render_template('manage/delete.html', items=items, warning="Be careful! This action is irreversible. "
                                                                      "If there are any inventory or shipment entries "
                                                                      "for this item, they will be deleted as well.")


if __name__ == '__main__':
    app.run()
    # app.run('0.0.0.0')  # For Replit
