from flask import Flask, render_template, request

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
        if request.form['direction'] == 'out':
            quantity *= -1
        conn = db.get_db_connection()
        # Before committing the change, we need to make sure that we have enough inventory
        stock = int(db.execute_query(
            conn=conn,
            query=constants.GET_INVENTORY_QTY_QUERY,
            args=(item_id,)
        ).fetchone()['quantity'])
        # If the user does not have enough inventory, close and terminate early
        if stock + quantity < 0:
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
        conn.commit()
        conn.close()
        return render_template('shipments/create.html', items=items, success="Shipment created successfully!")
    return render_template('shipments/create.html', items=items)


@app.route('/manage')
def manage():
    conn = db.get_db_connection()
    items = db.execute_query(
        conn=conn,
        query=constants.GET_ITEMS_QUERY
    ).fetchall()
    conn.close()
    return render_template('manage.html', items=items)


@app.route('/manage/create')
def manage_create():
    return render_template('manage/create.html')


@app.route('/manage/edit')
def manage_edit():
    return render_template('manage/edit.html')


@app.route('/manage/delete')
def manage_delete():
    return render_template('manage/delete.html')


if __name__ == '__main__':
    app.run()
