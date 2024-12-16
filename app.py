from flask import Flask, render_template, request, redirect, url_for, send_file
from markitdown import MarkItDown
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            markitdown = MarkItDown()
            result = markitdown.convert(file_path)
            
            markdown_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted.md')
            with open(markdown_file_path, 'w') as f:
                f.write(result.text_content)
            
            response = send_file(markdown_file_path, as_attachment=True, download_name='converted.md')
            
            # 一時ファイルを削除
            os.remove(file_path)
            os.remove(markdown_file_path)
            
            return response
    return '''
    <!doctype html>
    <title>ファイルをアップロード</title>
    <h1>ファイルをアップロードしてください</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="アップロード">
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
