FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をコピーしてインストール
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# Flaskアプリケーションを起動
CMD ["python", "app.py"]
