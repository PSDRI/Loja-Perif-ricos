import mysql.connector
from flask import Flask, request, jsonify

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="13122015",
    database="Loja_perifericos"
)

class Produto:
    def __init__(self, idproduto, nome, descricao, preco, estoque):
        self.idproduto = idproduto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque

    
    @classmethod
    def criar_produto(cls, nome, descricao, preco, estoque):
        cursor = db.cursor()
        cursor.execute("INSERT INTO Produto (nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s)",
                       (nome, descricao, preco, estoque))
        db.commit()
        return cls(cursor.lastrowid, nome, descricao, preco, estoque)

    @classmethod
    def obter_produto_por_id(cls, idproduto):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Produto WHERE idproduto = %s", (idproduto,))
        produto_data = cursor.fetchone()
        if produto_data:
            return cls(*produto_data)
        return None


    def atualizar_produto(self, nome, descricao, preco, estoque):
        cursor = db.cursor()
        cursor.execute("UPDATE Produto SET nome = %s, descricao = %s, preco = %s, estoque = %s WHERE idproduto = %s",
                       (nome, descricao, preco, estoque, self.idproduto))
        db.commit()
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque

    def excluir_produto(self):
        cursor = db.cursor()
        cursor.execute("DELETE FROM Produto WHERE idproduto = %s", (self.idproduto,))
        db.commit()

app = Flask(__name__)

@app.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json()
    nome = data.get('nome')
    descricao = data.get('descricao')
    preco = data.get('preco')
    estoque = data.get('estoque')

    novo_produto = Produto.criar_produto(nome, descricao, preco, estoque)
    return jsonify(novo_produto.__dict__)

@app.route('/produtos/<int:idproduto>', methods=['GET'])
def obter_produto(idproduto):
    produto = Produto.obter_produto_por_id(idproduto)
    if produto:
        return jsonify(produto.__dict__)
    return jsonify({"mensagem": "Produto não encontrado"}), 404

@app.route('/produtos/<int:idproduto>', methods=['PUT'])
def atualizar_produto(idproduto):
    produto = Produto.obter_produto_por_id(idproduto)
    if not produto:
        return jsonify({"mensagem": "Produto não encontrado"}), 404

    data = request.get_json()
    nome = data.get('nome')
    descricao = data.get('descricao')
    preco = data.get('preco')
    estoque = data.get('estoque')

    produto.atualizar_produto(nome, descricao, preco, estoque)
    return jsonify(produto.__dict__)

@app.route('/produtos/<int:idproduto>', methods=['DELETE'])
def excluir_produto(idproduto):
    produto = Produto.obter_produto_por_id(idproduto)
    if not produto:
        return jsonify({"mensagem": "Produto não encontrado"}), 404

    produto.excluir_produto()
    return jsonify({"mensagem": "Produto excluído com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
