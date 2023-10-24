import mysql.connector
from flask import Flask, request, jsonify

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="13122015",
    database="Loja_perifericos"
)

class Pedido:
    def __init__(self, idpedido, data, status):
        self.idpedido = idpedido
        self.data = data
        self.status = status

    @classmethod
    def criar_pedido(cls, data, status):
        cursor = db.cursor()
        cursor.execute("INSERT INTO Pedido (data, status) VALUES (%s, %s)",
                       (data, status))
        db.commit()
        return cls(cursor.lastrowid, data, status)

    @classmethod
    def obter_pedido_por_id(cls, idpedido):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Pedido WHERE idpedido = %s", (idpedido,))
        pedido_data = cursor.fetchone()
        if pedido_data:
            return cls(*pedido_data)
        return None

    def atualizar_pedido(self, data, status):
        cursor = db.cursor()
        cursor.execute("UPDATE Pedido SET data = %s, status = %s WHERE idpedido = %s",
                       (data, status, self.idpedido))
        db.commit()
        self.data = data
        self.status = status

    def excluir_pedido(self):
        cursor = db.cursor()
        cursor.execute("DELETE FROM Pedido WHERE idpedido = %s", (self.idpedido,))
        db.commit()

app = Flask(__name__)

@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    data = request.get_json()
    data_pedido = data.get('data')
    status = data.get('status')

    novo_pedido = Pedido.criar_pedido(data_pedido, status)
    return jsonify(novo_pedido.__dict__)

@app.route('/pedidos/<int:idpedido>', methods=['GET'])
def obter_pedido(idpedido):
    pedido = Pedido.obter_pedido_por_id(idpedido)
    if pedido:
        return jsonify(pedido.__dict__)
    return jsonify({"mensagem": "Pedido não encontrado"}), 404

@app.route('/pedidos/<int:idpedido>', methods=['PUT'])
def atualizar_pedido(idpedido):
    pedido = Pedido.obter_pedido_por_id(idpedido)
    if not pedido:
        return jsonify({"mensagem": "Pedido não encontrado"}), 404

    data = request.get_json()
    data_pedido = data.get('data')
    status = data.get('status')

    pedido.atualizar_pedido(data_pedido, status)
    return jsonify(pedido.__dict__)

@app.route('/pedidos/<int:idpedido>', methods=['DELETE'])
def excluir_pedido(idpedido):
    pedido = Pedido.obter_pedido_por_id(idpedido)
    if not pedido:
        return jsonify({"mensagem": "Pedido não encontrado"}), 404

    pedido.excluir_pedido()
    return jsonify({"mensagem": "Pedido excluído com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
