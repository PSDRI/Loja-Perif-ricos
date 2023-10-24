import mysql.connector
from flask import Flask, request, jsonify


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="13122015",
    database="Loja_perifericos"
)

app = Flask(__name__)

@app.route('/produtos', methods=['GET'])
def get_produtos():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Produto")
    produtos = cursor.fetchall()
    cursor.close()
    return jsonify(produtos)


if __name__ == '__main__':
    app.run(debug=True)
