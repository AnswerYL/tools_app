from PIL import Image
from flask import Flask, request, jsonify
import os
import random
import string
import shutil
import threading
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

def generate_random_folder_name():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

def save_uploaded_image(image_file, output_folder):
    try:
        # 生成一个随机的文件夹名
        folder_name = generate_random_folder_name()
        folder_path = os.path.join(output_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # 保存图片到随机生成的文件夹中
        image = Image.open(image_file)
        image.save(os.path.join(folder_path, "uploaded_image.jpg"))

        # 返回文件夹路径，以便后续删除
        return folder_path
    except Exception as e:
        raise e

def split_image_to_nine(image_path, output_folder):
    # 切分图片的代码，保持不变

@app.route('/split_image', methods=['POST'])
def split_image():
    try:
        # 获取上传的图片文件
        image_file = request.files.get('image')
        if not image_file:
            return jsonify({"error": "未上传图片文件"}), 400

        # 保存上传的图片文件到临时目录
        temp_image_path = "temp_image.jpg"
        image_file.save(temp_image_path)

        # 保存上传的图片到随机生成的文件夹中
        output_folder = os.path.dirname(os.path.abspath(__file__))  # 保存在当前文件夹下
        folder_path = save_uploaded_image(temp_image_path, output_folder)

        # 切分图片并保存到随机生成的文件夹中
        split_image_to_nine(temp_image_path, folder_path)

        # 删除临时图片文件
        os.remove(temp_image_path)

        # 启动线程，在10分钟后删除文件夹
        threading.Timer(600, lambda: shutil.rmtree(folder_path)).start()

        return jsonify({"message": "图片切分成功！", "folder_path": folder_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
