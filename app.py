from flask import Flask, request, jsonify, make_response
import mysql.connector
import xmltodict

app = Flask(__name__)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="bicycle_rental"
)
cursor = db.cursor(dictionary=True)

# Helper Functions
def to_xml(data):
    """Convert JSON to XML."""
    return xmltodict.unparse({"response": data}, pretty=True)

# CRUD API for Multi Shops
@app.route('/shops', methods=['GET', 'POST'])
def manage_shops():
    if request.method == 'GET':
        format_type = request.args.get('format', 'json')
        cursor.execute("SELECT * FROM multi_shops")
        shops = cursor.fetchall()
        if format_type == 'xml':
            response = make_response(to_xml(shops))
            response.headers["Content-Type"] = "application/xml"
            return response
        return jsonify(shops)

    elif request.method == 'POST':
        data = request.json
        cursor.execute(
            "INSERT INTO multi_shops (contact_name, email_address, address, phone_number, bicycle_idbicycle) "
            "VALUES (%s, %s, %s, %s, %s)",
            (data['contact_name'], data['email_address'], data['address'], data['phone_number'], data['bicycle_idbicycle'])
        )
        db.commit()
        return jsonify({"message": "Shop created"}), 201

@app.route('/shops/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def shop_operations(id):
    if request.method == 'GET':
        format_type = request.args.get('format', 'json')
        cursor.execute("SELECT * FROM multi_shops WHERE idshop = %s", (id,))
        shop = cursor.fetchone()
        if not shop:
            return jsonify({"error": "Shop not found"}), 404
        if format_type == 'xml':
            response = make_response(to_xml(shop))
            response.headers["Content-Type"] = "application/xml"
            return response
        return jsonify(shop)

    elif request.method == 'PUT':
        data = request.json
        cursor.execute(
            "UPDATE multi_shops SET contact_name = %s, email_address = %s, address = %s, phone_number = %s, bicycle_idbicycle = %s "
            "WHERE idshop = %s",
            (data['contact_name'], data['email_address'], data['address'], data['phone_number'], data['bicycle_idbicycle'], id)
        )
        db.commit()
        return jsonify({"message": "Shop updated"})

    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM multi_shops WHERE idshop = %s", (id,))
        db.commit()
        return jsonify({"message": "Shop deleted"})

# Add CRUD for other tables (bicycles, rentals, renters, payments) similarly.

if __name__ == '__main__':
    app.run(debug=True)
