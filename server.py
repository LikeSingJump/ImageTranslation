import time
from flask import Flask, request, jsonify, send_from_directory
import requests
from flask_sqlalchemy import SQLAlchemy
import os

# from functions import gen_vis_fake_img
# from models import models

app = Flask(__name__)
# MySQL所在主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名
USERNAME = "root"
# 连接MySQL的密码
PASSWORD = "Lkjoiu!123"
# MySQL上创建的数据库名称
DATABASE = "myDB"
# 通过修改以下代码来操作不同的SQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
db = SQLAlchemy(app)
# image_styles = models.keys()


def get_public_ip():
    response = requests.get('https://api.ipify.org')
    ip = response.text
    host = "http://"+ip
    return host


CLOUDHOST = get_public_ip()


def allowed_file(filename):
    # 检查文件类型是否允许上传
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


UPLOAD_FOLDER = '/home/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 设置最大请求内容大小为 100 MB


def time_format():
    return str(time.strftime("%Y%m%d%H%M%S", time.localtime()))


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        response = {'message': 'Invalid credentials'}
        return jsonify(response), 400

    user = Users.query.filter_by(username=username).first()

    if user and user.password == password:
        response = {'message': 'Login successful'}
        return jsonify(response), 200

    response = {'message': 'Invalid username or password'}
    return jsonify(response), 401


@app.route('/register', methods=['POST'])
def register():
    # 获取请求中的注册信息
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if username and email and password:
        user = Users(username=username, email=email, password=password)
        db.session.add(user)
        try:
            db.session.commit()
            response = {'message': 'Registration successful'}
            return jsonify(response), 200
        except Exception as e:
            response = {'message': 'Registration failed'}
            return jsonify(response), 401

    else:
        response = {'message': 'Invalid data. Please provide all required fields.'}
        return jsonify(response), 400


@app.route('/user', methods=['POST'])
def home():
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    if user:
        response = {'email': user.email}
        return jsonify(response), 200
    else:
        response = {'message': 'User not found'}
        return jsonify(response), 401


@app.route('/images/<path:username>/<path:filename>')
def get_image(username, filename):
    image_path = '/home/images/' + username
    return send_from_directory(image_path, filename)


@app.route('/outputs/<filename>')
def outputs_image(filename):
    return send_from_directory('outputs/', filename)


@app.route('/styles/<filename>')
def style_image(filename):
    return send_from_directory('styles/', filename)


@app.route('/images', methods=['GET'])
def get_user_images():
    username = request.args.get('username')

    images = Images.query.filter_by(username=username).order_by(Images.time.desc()).all()
    if images:
        urls = [image.url for image in images]
        response = {'urls': urls}
        return jsonify(response), 200
    else:
        response = {'message': 'No images found'}
        return jsonify(response), 404


@app.route('/getStyles', methods=['GET'])
def get_styles():
    styles = Styles.query.all()
    results = []
    for style in styles:
        results.append({
            'style': style.style,
            'url': style.url,
        })
    return jsonify(results)


@app.route('/upload', methods=['POST'])
def upload():
    username = request.form.get('username')
    # 检查是否有文件被上传
    if 'file' not in request.files:
        response = {'message': 'No file uploaded'}
        return jsonify(response), 400

    file = request.files['file']

    file_extension = os.path.splitext(file.filename)[1]
    file.filename = time_format() + file_extension

    # 检查文件类型是否允许上传
    if not allowed_file(file.filename):
        response = {'message': 'Invalid file type'}
        return jsonify(response), 400

    # 保存上传的文件到指定路径
    directory = os.path.join(app.config['UPLOAD_FOLDER'], username)
    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(directory):
        os.makedirs(directory)
    file.save(os.path.join(directory, file.filename))
    url = os.path.join(CLOUDHOST, "images", username, file.filename)

    # 创建新的 Image 对象并保存到数据库
    image = Images(username=username, url=url, path=os.path.join(directory, file.filename), time=time_format())
    db.session.add(image)
    db.session.commit()

    response = {'message': 'File uploaded successfully'}
    return jsonify(response), 200


@app.route('/generate', methods=['POST'])
def generate_image():
    style = request.form.get('style')
    image_url = request.form.get('url')
    image = Images.query.filter_by(url=image_url).first()
    source_path = image.path
    print(source_path)

    if style:
        return 200
        # if style in image_styles:
        #     # 文件名和路径
        #     filename = style + time_format() + '.jpg'
        #     save_path = 'outputs/' + filename
        #
        #     gen_vis_fake_img(source_path, models[style], target_domain=style, figsize=5, save_path=save_path)
        #
        #     # 以url方式响应
        #     url = f'/outputs/{filename}'
        #     print(url)
        #     response = {'url': url}
        #     return jsonify(response), 200
        # else:
        #     response = {
        #         'message': 'Style error',
        #         'style:': style
        #     }
        #     return jsonify(response), 401
    else:
        response = {'message': 'Generate failed'}
        return jsonify(response), 400


@app.route('/delete', methods=['POST'])
def delete_image():
    image_url = request.form.get('url')

    # 查询要删除的图片
    image = Images.query.filter_by(url=image_url).first()

    # 检查图片是否存在
    if image is None:
        response = {'message': 'Image not found'}
        return jsonify(response), 404

    # 删除图片文件
    if os.path.exists(image.path):
        os.remove(image.path)

    # 删除数据库中的图片记录
    db.session.delete(image)
    db.session.commit()

    response = {'message': 'Image deleted successfully'}
    return jsonify(response), 200


if __name__ == '__main__':
    app.run()


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Images(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)


class Styles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
