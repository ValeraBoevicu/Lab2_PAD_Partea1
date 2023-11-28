from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

data = {
    "nume": "Alex",
    "varsta": 24
}

executor = ThreadPoolExecutor(2)

@app.route('/data', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def manage_data():
    format = request.args.get('format', 'json')

    if request.method == 'GET':
        if format == 'xml':
            xml_data = f"<data><nume>{data['nume']}</nume><varsta>{data['varsta']}</varsta></data>"
            return xml_data, 200, {'Content-Type': 'application/xml'}
        return jsonify(data), 200

    elif request.method == 'POST' or request.method == 'PUT':
        new_data = request.get_json()
        if new_data:
            future = executor.submit(update_data, new_data)
            return future.result(), 200
        else:
            return jsonify({"message": "Cererea nu contine date valide."}), 400

    elif request.method == 'PATCH':
        updated_data = request.get_json()
        if updated_data:
            future = executor.submit(patch_data, updated_data)
            return future.result(), 200
        else:
            return jsonify({"message": "Cererea nu contine date valide."}), 400

    elif request.method == 'DELETE':
        future = executor.submit(delete_data)
        return future.result(), 200

def update_data(new_data):
    with app.app_context():
        data.update(new_data)
        return jsonify({"message": "Datele au fost actualizate."})

def patch_data(updated_data):
    with app.app_context():
        data.update(updated_data)
        return jsonify({"message": "Datele au fost modificate folosind PATCH."})

def delete_data():
    with app.app_context():
        data.clear()
        return jsonify({"message": "Datele au fost șterse."})

if __name__ == '__main__':
    app.run()




# http://localhost:5000/data?format=json - JSON
# http://localhost:5000/data?format=xml - XML