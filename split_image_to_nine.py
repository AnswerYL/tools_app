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
        # Generate a random folder name
        folder_name = generate_random_folder_name()
        folder_path = os.path.join(output_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Save the uploaded image to the randomly generated folder
        image = Image.open(image_file)
        image = image.convert('RGB')  # Convert RGBA to RGB
        image.save(os.path.join(folder_path, "uploaded_image.jpg"))

        # Return the folder path for later use
        return folder_path
    except Exception as e:
        raise e

def split_image_to_nine(image_path, output_folder):
    # Image splitting code, unchanged
    try:
        # 打开图片
        image = Image.open(image_path)
        width, height = image.size

        # 确定九宫格切分后的每个小图的宽度和高度
        small_width = width // 3
        small_height = height // 3

        # 切分并保存每个小图
        for row in range(3):
            for col in range(3):
                left = col * small_width
                upper = row * small_height
                right = (col + 1) * small_width
                lower = (row + 1) * small_height

                small_image = image.crop((left, upper, right, lower))
                output_path = os.path.join(output_folder, f"part_{row}_{col}.png")
                small_image.save(output_path)

        return "图片切分成功！"
    except Exception as e:
        return f"图片切分失败：{str(e)}"

@app.route('/split_image', methods=['POST'])
def split_image():
    try:
        # Get the uploaded image file
        image_file = request.files.get('image')
        if not image_file:
            return jsonify({"error": "未上传图片文件"}), 400

        # Save the uploaded image to the current folder
        output_folder = os.path.dirname(os.path.abspath(__file__))  # Save in the current folder
        folder_path = save_uploaded_image(image_file, output_folder)

        # Split the image and save it to the randomly generated folder
        split_image_to_nine(image_file, folder_path)

        # Start a thread to delete the folder after 10 minutes
        threading.Timer(600, lambda: shutil.rmtree(folder_path)).start()

        return jsonify({"message": "图片切分成功！", "folder_path": folder_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
