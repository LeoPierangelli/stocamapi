from flask import Flask, request, jsonify
from flask_cors import CORS
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import io

# Inicializa a aplicação Flask
app = Flask(__name__)
# Habilita o CORS para permitir requisições do frontend
CORS(app)

@app.route('/decode', methods=['POST'])
def decode_datamatrix():
    """
    Endpoint que recebe uma imagem, decodifica o Data Matrix e retorna os dados.
    """
    # Verifica se o arquivo está na requisição
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']

    # Verifica se o nome do arquivo não está vazio
    if file.filename == '':
        return jsonify({'error': 'Nome de arquivo inválido'}), 400

    if file:
        try:
            # Abre a imagem usando a biblioteca Pillow
            image = Image.open(file.stream)

            # Tenta decodificar o Data Matrix na imagem
            decoded_objects = decode(image)

            if decoded_objects:
                # Extrai os dados decodificados
                # O resultado é uma lista, vamos pegar o primeiro e decodificar para string
                data = [obj.data.decode('utf-8') for obj in decoded_objects]
                print(f"Data Matrix lido com sucesso: {data}")
                return jsonify({'success': True, 'data': data})
            else:
                print("Nenhum Data Matrix encontrado na imagem.")
                return jsonify({'success': False, 'message': 'Nenhum Data Matrix encontrado'})

        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")
            return jsonify({'error': f'Erro interno no servidor: {str(e)}'}), 500
