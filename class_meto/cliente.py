import mysql.connector
from flask import Flask, request, jsonify

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="13122015",
    database="Loja_perifericos"
)

class Cliente:
    def __init__(self, idcliente, nome, endereco, telefone):
        self.idcliente = idcliente
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone

    @classmethod
    def criar_cliente(cls, nome, endereco, telefone):
        cursor = db.cursor()
        cursor.execute("INSERT INTO Cliente (nome, endereco, telefone) VALUES (%s, %s, %s)",
                       (nome, endereco, telefone))
        db.commit()
        return cls(cursor.lastrowid, nome, endereco, telefone)

    @classmethod
    def obter_cliente_por_id(cls, idcliente):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Cliente WHERE idcliente = %s", (idcliente,))
        cliente_data = cursor.fetchone()
        if cliente_data:
            return cls(*cliente_data)
        return None


    def atualizar_cliente(self, nome, endereco, telefone):
        cursor = db.cursor()
        cursor.execute("UPDATE Cliente SET nome = %s, endereco = %s, telefone = %s WHERE idcliente = %s",
                       (nome, endereco, telefone, self.idcliente))
        db.commit()
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone


    def excluir_cliente(self):
        cursor = db.cursor()
        cursor.execute("DELETE FROM Cliente WHERE idcliente = %s", (self.idcliente,))
        db.commit()

app = Flask(__name__)

@app.route('/clientes', methods=['POST'])
def criar_cliente():
    data = request.get_json()
    nome = data.get('nome')
    endereco = data.get('endereco')
    telefone = data.get('telefone')

    novo_cliente = Cliente.criar_cliente(nome, endereco, telefone)
    return jsonify(novo_cliente.__dict__)


@app.route('/clientes/<int:idcliente>', methods=['GET'])
def obter_cliente(idcliente):
    cliente = Cliente.obter_cliente_por_id(idcliente)
    if cliente:
        return jsonify(cliente.__dict__)
    return jsonify({"mensagem": "Cliente não encontrado"}), 404


@app.route('/clientes/<int:idcliente>', methods=['PUT'])
def atualizar_cliente(idcliente):
    cliente = Cliente.obter_cliente_por_id(idcliente)
    if not cliente:
        return jsonify({"mensagem": "Cliente não encontrado"}), 404

    data = request.get_json()
    nome = data.get('nome')
    endereco = data.get('endereco')
    telefone = data.get('telefone')

    cliente.atualizar_cliente(nome, endereco, telefone)
    return jsonify(cliente.__dict__)

@app.route('/clientes/<int:idcliente>', methods=['DELETE'])
def excluir_cliente(idcliente):
    cliente = Cliente.obter_cliente_por_id(idcliente)
    if not cliente:
        return jsonify({"mensagem": "Cliente não encontrado"}), 404

    cliente.excluir_cliente()
    return jsonify({"mensagem": "Cliente excluído com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
