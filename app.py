
from flask import Flask, request, jsonify
from flask_cors import CORS
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import io

# Inicializa a aplicação Flask
app = Flask(__name__)
# Habilita o CORS para permitir requisições do frontend
CORS(app)

@app.route('/')
def health_check():
    """
    Rota de health check para o Render.
    """
    return jsonify({'status': 'ok'}), 200

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

            # --- Otimização da Imagem ---
            print("Otimizando a imagem...")
            # Converte para tons de cinza (L = Luminance)
            optimized_image = image.convert('L')

            # Redimensiona a imagem se ela for maior que 1200x1200 pixels, mantendo a proporção.
            # Este é um bom equilíbrio entre performance e precisão da leitura.
            MAX_SIZE = (1200, 1200)
            optimized_image.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
            print(f"Imagem redimensionada para: {optimized_image.size}")
            # --- Fim da Otimização ---

            # Tenta decodificar o Data Matrix na imagem otimizada
            print("Tentando decodificar a imagem otimizada...")
            decoded_objects = decode(optimized_image)

            if decoded_objects:
                # Extrai os dados decodificados
                data = [obj.data.decode('utf-8') for obj in decoded_objects]
                print(f"Data Matrix lido com sucesso: {data}")
                return jsonify({'success': True, 'data': data})
            else:
                print("Nenhum Data Matrix encontrado na imagem.")
                return jsonify({'success': False, 'message': 'Nenhum Data Matrix encontrado'})

        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")
            return jsonify({'error': f'Erro interno no servidor: {str(e)}'}), 500
