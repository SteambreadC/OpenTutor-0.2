import json
import os
from datetime import datetime

from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token

# 假设你的文件和处理后的文件都将暂时存储在这个目录下
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'  # 使用SQLite作为本地开发数据库
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String(150), unique=True, nullable=False)


# 注册路由
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

# 登录路由
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

# 课程注册路由
@app.route('/api/register-course', methods=['POST'])
def register_course():
    data = request.get_json()
    course_name = data.get('courseName')
    if not course_name:
        return jsonify(message="Missing courseName"), 400
    new_course = Course(courseName=course_name)
    db.session.add(new_course)
    db.session.commit()
    return jsonify(message="Course registered successfully"), 201

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
        # 检查是否有文件上传
        if not request.files:
            return {'message': 'No file part'}, 400
        # 获取所有可能的文件
        files = {
            'textbook': request.files.get('textbook'),
            'ppt': request.files.get('ppt'),
            'notes': request.files.get('notes'),
            'tests': request.files.get('tests'),
            'mockTests': request.files.get('mockTests'),
            'others': request.files.get('others')
        }

        # 检查至少有一个文件被上传
        if not any(files.values()):
            return {'message': 'No file uploaded'}, 400

        # 保存所有文件
        for key, file in files.items():
            print(key)
            if file:
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                print(f"Saved file: {filename}")

            '''
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            # 保存文本到文件
            text_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'submitted_text.txt')
            with open(text_filename, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            '''

        # 模拟生成预测结果
        predictions = "这是预测结果"
        return {'message': 'Files received', 'predictions': predictions}, 200


api.add_resource(Hello, '/hello')
api.add_resource(SubmitAPI, '/api/submit')

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    db.create_all()
    app.run(host='127.0.0.1', port=8010, debug=True)
