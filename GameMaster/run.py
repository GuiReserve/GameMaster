import uuid
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

UPLOAD = 'static/assets'
app.config['UPLOAD'] = UPLOAD


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro_p", methods=['GET', 'POST'])
def cadastro_plataformas():
    if request.method == 'POST':
        nome = request.form['nome']
        fabricante = request.form['fabricante']
        
        imagem = request.files['imagem']
        if imagem:
            extensao = imagem.filename.split('.')[-1]
            nome_imagem = f"{nome.strip().lower().replace(".", "_")}.{extensao}"
            caminho_imagem = os.path.join(app.config['UPLOAD'], nome_imagem)
            imagem.save(caminho_imagem)
        
        cod_plataforma = str(uuid.uuid4())

        caminho_arquivo = 'models/plataforma.txt'
    
        with open(caminho_arquivo, 'a') as arquivo:
            arquivo.write(f"{cod_plataforma};{nome};{fabricante}; {caminho_imagem}\n")

        return redirect("/cadastro_p")

    return render_template("cadastro_plataformas.html")

@app.route('/consulta_plataformas')  # Define a rota para a página de consulta de plataformas.
def consulta_plataformas():
    plataformas = []  # Cria uma lista vazia para armazenar as plataformas lidas do arquivo.
    linha_controle = 0  # Inicializa um controle numérico para contar as linhas (registros).
    caminho_plataformas = 'models/plataforma.txt'  # Define o caminho do arquivo onde as plataformas estão armazenadas.

    with open(caminho_plataformas, 'r') as arquivo:  # Abre o arquivo em modo de leitura ('r').
        for linha in arquivo:  # Itera sobre cada linha do arquivo.
            dados = linha.strip().split(';')  # Remove espaços em branco no início e fim da linha e divide os dados com base no ponto e vírgula.
            plataformas.append({  # Adiciona um dicionário à lista 'plataformas' com as informações da linha.
                'linha': linha_controle,  # Armazena o número da linha.
                'cod_plataforma': dados[0],  # Código da plataforma.
                'nome': dados[1],  # Nome da plataforma.
                'fabricante': dados[2],  # Fabricante da plataforma.
                'imagem': dados [3]
            })
            linha_controle += 1  # Incrementa o controle numérico das linhas.

    return render_template('consulta_plataformas.html', dados_lista=plataformas)  # Renderiza o template com os dados das plataformas.

@app.route('/excluir_plataforma', methods=['GET', 'POST'])  # Define a rota para exclusão de uma plataforma.
def excluir_plataforma():
    linha_para_excluir = int(request.args.get('linha'))  # Obtém a linha a ser excluída com base no parâmetro 'linha' enviado pela URL.
    caminho_plataformas = 'models/plataforma.txt'  # Define o caminho do arquivo onde as plataformas estão armazenadas.

    with open(caminho_plataformas, 'r') as arquivo:  # Abre o arquivo em modo de leitura ('r').
        linhas = arquivo.readlines()  # Lê todas as linhas do arquivo e as armazena na lista 'linhas'.

    del linhas[linha_para_excluir]  # Exclui a linha correspondente ao número informado.

    with open(caminho_plataformas, 'w') as arquivo:  # Abre o arquivo em modo de escrita ('w') para sobrescrever o conteúdo.
        arquivo.writelines(linhas)  # Escreve as linhas restantes no arquivo, sem a linha excluída.

    return redirect('/consulta_plataformas')  # Redireciona o usuário para a página de consulta de plataformas após a exclusão.

# Roda a aplicação Flask no endereço 127.0.0.1 e na porta 80, com o modo debug ativo.
app.run(host='127.0.0.1', port=80, debug=True)

