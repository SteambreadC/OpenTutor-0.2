import json
import os
import uuid
import jwt
from datetime import datetime

from flask import Flask, request, send_from_directory, jsonify, session
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
#CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = 'supersecretkey'
# 假设你的文件和处理后的文件都将暂时存储在这个目录下
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
api = Api(app)

JWT_SECRET = 'anothersecretkey'
JWT_ALGORITHM = 'HS256'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'  # 使用SQLite作为本地开发数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Course(db.Model):
    id = db.Column(db.String(36), primary_key=True) # 使用字符串存储UUID
    courseName = db.Column(db.String(80), nullable=False)
    school = db.Column(db.String(120))
    professor = db.Column(db.String(120))
    year = db.Column(db.String(4))
    info = db.Column(db.Text)
    skip = db.Column(db.Boolean, default=False)

class UserCourse(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course_code = db.Column(db.String(36), db.ForeignKey('course.id'), primary_key=True)

class FileMetadata(db.Model):
    file_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.String(36), db.ForeignKey('course.id'))
    file_path = db.Column(db.String(255))
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)

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
        access_token = create_access_token(identity={'id': user.id, 'username': user.username})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401


@app.route('/generate-token', methods=['GET'])
def generate_token():
    user_id = str(uuid.uuid4())  # 生成一个临时用户ID
    token = create_access_token(identity={'id': user_id})
    return jsonify({'token': token}), 200


# 课程注册路由
class CreateCourseAPI(Resource):
    def post(self):
        #user_id = get_jwt_identity()['id']
        parser = reqparse.RequestParser()
        parser.add_argument('courseName', type=str, required=True, help='Course Name is required')
        parser.add_argument('school', type=str)
        parser.add_argument('professor', type=str)
        parser.add_argument('year', type=str)
        parser.add_argument('info', type=str)
        parser.add_argument('skip', type=bool, default=False)
        args = parser.parse_args()

        course_id = str(uuid.uuid4())  # 生成唯一课程ID

        new_course = Course(
            id=course_id,
            courseName=args['courseName'],
            school=args['school'],
            professor=args['professor'],
            year=args['year'],
            info=args['info'],
            skip=args['skip']
        )
        db.session.add(new_course)
        db.session.commit()

        user_course = UserCourse(
            user_id=1,
            course_code=course_id
        )
        db.session.add(user_course)
        db.session.commit()

        return {"message": "Course created successfully", "course_id": course_id}, 201

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

class Default(Resource):
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
    #@jwt_required()
    def post(self):
        #user_id = get_jwt_identity()['id']
        course_id = request.form.get('course_id')
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

api.add_resource(Default, '/')
api.add_resource(Hello, '/hello')
api.add_resource(CreateCourseAPI, '/api/register-course')
api.add_resource(SubmitAPI, '/api/submit')

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    #db.drop_all()
    db.create_all()
    app.run(host='127.0.0.1', port=8010, debug=True)
