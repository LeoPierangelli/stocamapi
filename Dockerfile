# Use uma imagem Python 3.11 oficial e leve
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Atualiza os pacotes do sistema e instala a dependência libdmtx
RUN apt-get update && apt-get install -y libdmtx0b

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação
COPY . .

# Expõe a porta que a aplicação vai rodar. Render define a variável PORT.
# O valor padrão é 10000.
EXPOSE 10000

# Comando para iniciar a aplicação quando o container for executado
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
