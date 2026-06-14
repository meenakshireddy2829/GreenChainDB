
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Dashboard
@app.route('/')
def dashboard():
    return render_template('index.html')


# Collection Centers
@app.route('/centers', methods=['GET', 'POST'])
def centers():
    conn = sqlite3.connect('greenchain.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        center_name = request.form['center_name']
        location = request.form['location']

        cursor.execute(
            "INSERT INTO CollectionCenter (center_name, location) VALUES (?, ?)",
            (center_name, location)
        )

        conn.commit()

    cursor.execute("SELECT * FROM CollectionCenter")
    centers = cursor.fetchall()

    conn.close()

    return render_template('centers.html', centers=centers)


# Waste Collection
@app.route('/waste', methods=['GET', 'POST'])
def waste():
    conn = sqlite3.connect('greenchain.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        center_id = request.form['center_id']
        waste_type = request.form['waste_type']
        quantity = request.form['quantity']
        collection_date = request.form['collection_date']

        cursor.execute("""
            INSERT INTO WasteCollection
            (center_id, waste_type, quantity, collection_date)
            VALUES (?, ?, ?, ?)
        """, (center_id, waste_type, quantity, collection_date))

        conn.commit()

    cursor.execute("""
        SELECT wc.collection_id,
               cc.center_name,
               wc.waste_type,
               wc.quantity,
               wc.collection_date
        FROM WasteCollection wc
        JOIN CollectionCenter cc
        ON wc.center_id = cc.center_id
    """)

    waste_records = cursor.fetchall()

    cursor.execute("SELECT * FROM CollectionCenter")
    centers = cursor.fetchall()

    conn.close()

    return render_template(
        'waste.html',
        waste_records=waste_records,
        centers=centers
    )


# Recycling Plants
@app.route('/plants', methods=['GET', 'POST'])
def plants():
    conn = sqlite3.connect('greenchain.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        plant_name = request.form['plant_name']
        location = request.form['location']
        capacity = request.form['capacity']

        cursor.execute("""
            INSERT INTO RecyclingPlant
            (plant_name, location, capacity_per_day)
            VALUES (?, ?, ?)
        """, (plant_name, location, capacity))

        conn.commit()

    cursor.execute("SELECT * FROM RecyclingPlant")
    plants = cursor.fetchall()

    conn.close()

    return render_template('plants.html', plants=plants)


# Recycling Records
@app.route('/recycling', methods=['GET', 'POST'])
def recycling():
    conn = sqlite3.connect('greenchain.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        collection_id = request.form['collection_id']
        plant_id = request.form['plant_id']
        recycled_quantity = request.form['recycled_quantity']
        recycling_date = request.form['recycling_date']

        cursor.execute("""
            INSERT INTO RecyclingRecord
            (collection_id, plant_id, recycled_quantity, recycling_date)
            VALUES (?, ?, ?, ?)
        """, (
            collection_id,
            plant_id,
            recycled_quantity,
            recycling_date
        ))

        conn.commit()

    cursor.execute("""
        SELECT rr.recycle_id,
               wc.waste_type,
               rp.plant_name,
               rr.recycled_quantity,
               rr.recycling_date
        FROM RecyclingRecord rr
        JOIN WasteCollection wc
        ON rr.collection_id = wc.collection_id
        JOIN RecyclingPlant rp
        ON rr.plant_id = rp.plant_id
    """)

    records = cursor.fetchall()

    cursor.execute("""
        SELECT collection_id, waste_type
        FROM WasteCollection
    """)

    waste_records = cursor.fetchall()

    cursor.execute("""
        SELECT plant_id, plant_name
        FROM RecyclingPlant
    """)

    plants = cursor.fetchall()

    conn.close()

    return render_template(
        'recycling.html',
        records=records,
        waste_records=waste_records,
        plants=plants
    )


if __name__ == '__main__':
    app.run(debug=True)
