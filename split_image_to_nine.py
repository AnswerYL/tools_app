from PIL import Image
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def split_image_to_nine(image_path, output_folder):
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
        # 获取上传的图片文件
        image_file = request.files.get('image')
        if not image_file:
            return jsonify({"error": "未上传图片文件"}), 400

        # 获取保存图片的路径
        output_folder = request.form.get('output_folder')
        if not output_folder:
            return jsonify({"error": "未指定保存图片的路径"}), 400

        os.makedirs(output_folder, exist_ok=True)

        # 保存上传的图片文件到临时目录
        temp_image_path = "temp_image.jpg"
        image_file.save(temp_image_path)

        # 切分图片并保存到输出文件夹
        result = split_image_to_nine(temp_image_path, output_folder)

        # 删除临时图片文件
        os.remove(temp_image_path)

        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
