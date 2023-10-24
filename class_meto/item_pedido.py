import mysql.connector
from flask import Flask, request, jsonify

db = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="loja_perifericos"
)

class ItemPedido:
    def __init__(self, iditempedido, idpedido, idproduto, quantidade):
        self.iditempedido = iditempedido
        self.idpedido = idpedido
        self.idproduto = idproduto
        self.quantidade = quantidade

    @classmethod
    def adicionar_item_pedido(cls, idpedido, idproduto, quantidade):
        cursor = db.cursor()
        cursor.execute("INSERT INTO ItemPedido (idpedido, idproduto, quantidade) VALUES (%s, %s, %s)",
                       (idpedido, idproduto, quantidade))
        db.commit()
        return cls(cursor.lastrowid, idpedido, idproduto, quantidade)


    @classmethod
    def obter_item_pedido_por_id(cls, iditempedido):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM ItemPedido WHERE iditempedido = %s", (iditempedido,))
        itempedido_data = cursor.fetchone()
        if itempedido_data:
            return cls(*itempedido_data)
        return None

    def atualizar_item_pedido(self, quantidade):
        cursor = db.cursor()
        cursor.execute("UPDATE ItemPedido SET quantidade = %s WHERE iditempedido = %s",
                       (quantidade, self.iditempedido))
        db.commit()
        self.quantidade = quantidade

    def excluir_item_pedido(self):
        cursor = db.cursor()
        cursor.execute("DELETE FROM ItemPedido WHERE iditempedido = %s", (self.iditempedido,))
        db.commit()

app = Flask(__name__)

@app.route('/pedidos/<int:idpedido>/itens', methods=['POST'])
def adicionar_item_pedido(idpedido):
    data = request.get_json()
    idproduto = data.get('idproduto')
    quantidade = data.get('quantidade')

    novo_item_pedido = ItemPedido.adicionar_item_pedido(idpedido, idproduto, quantidade)
    return jsonify(novo_item_pedido.__dict__)

@app.route('/itenspedido/<int:iditempedido>', methods=['GET'])
def obter_item_pedido(iditempedido):
    item_pedido = ItemPedido.obter_item_pedido_por_id(iditempedido)
    if item_pedido:
        return jsonify(item_pedido.__dict__)
    return jsonify({"mensagem": "Item de pedido não encontrado"}), 404

@app.route('/itenspedido/<int:iditempedido>', methods=['PUT'])
def atualizar_item_pedido(iditempedido):
    item_pedido = ItemPedido.obter_item_pedido_por_id(iditempedido)
    if not item_pedido:
        return jsonify({"mensagem": "Item de pedido não encontrado"}), 404

    data = request.get_json()
    quantidade = data.get('quantidade')

    item_pedido.atualizar_item_pedido(quantidade)
    return jsonify(item_pedido.__dict__)

@app.route('/itenspedido/<int:iditempedido>', methods=['DELETE'])
def excluir_item_pedido(iditempedido):
    item_pedido = ItemPedido.obter_item_pedido_por_id(iditempedido)
    if not item_pedido:
        return jsonify({"mensagem": "Item de pedido não encontrado"}), 404

    item_pedido.excluir_item_pedido()
    return jsonify({"mensagem": "Item de pedido excluído com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
