from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    mensagem = "Esta é uma mensagem gerada por Python no servidor."
    return render_template('index.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)
