import json
import os
from datetime import datetime

from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource



# 假设你的PDF文件和处理后的PDF文件都将暂时存储在这个目录下
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=["GET"])
@app.route('/', methods=["POST"])
def index():
    return "Welcome to my gpt ta, try /hello or submit your files."


class Hello(Resource):
    @staticmethod
    def get():
        # 获取当前时间
        current_time = datetime.now()
        # 自定义格式化字符串
        formatted_time = current_time.strftime('%Y-%m-%d  %H:%M:%S')

        return formatted_time

    @staticmethod
    def post():
        return "[post] hello flask"


class SubmitAPI(Resource):
    def post(self):
        if 'material' not in request.files:
            return {'message': 'No file part'}, 400
        file = request.files['material']
        text = request.form['text']

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            # 处理逻辑...
            processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed.pdf')
            return {'message': 'File and text received, processing done'}, 200
        else:
            return {'message': 'No file uploaded'}, 400


api.add_resource(Hello, '/hello')
api.add_resource(SubmitAPI, '/api/submit')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8010, debug=False)
