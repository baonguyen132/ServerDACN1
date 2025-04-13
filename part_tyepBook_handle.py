import os
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from AI.scan_image import scans
from connectDatabase import importData, exportData

typeBook_bp = Blueprint('type_book', __name__)

@typeBook_bp.route('/insertTypeBook', methods=['POST'])
def insertTypeBook():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        print(data)
        importData(
            sql="""INSERT INTO `type_books`
                    (`name_book`, `type_book`, `price` ,`image`, `description`, `created_at`, `updated_at`)
                    VALUES (%s, %s ,%s, %s, %s, NOW(), NOW())""",
            val=(
                data["name_book"], data["type_book"], data["price"] ,data["image"], data["description"]
            )
        )

        # Trả phản hồi về Flutter
        return jsonify({"message": "Thêm sách thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@typeBook_bp.route('/updateTypeBook', methods=['POST'])
def updateTypeBook():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        importData(
            sql="""UPDATE `type_books` SET 
            `name_book`=%s,
            `type_book`=%s,
            `price` = %s ,
            `image`=%s,
            `description`=%s,
            `updated_at`=NOW() 
            WHERE `id`= %s """,
            val=(
                data["name_book"], data["type_book"], data["price"] ,data["image"], data["description"] , data["id"]
            )
        )

        # Trả phản hồi về Flutter
        return jsonify({"message": "Cập nhật thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@typeBook_bp.route('/deleteTypeBook', methods=['POST'])
def deleteTypeBook():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        importData(
            sql="""DELETE FROM `type_books` WHERE `id` = %s """,
            val=(data["id"],)
        )

        # Trả phản hồi về Flutter
        return jsonify({"message": "Xoá thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@typeBook_bp.route("/exportTypeBook" , methods=['POST'])
def exportTypeBook():

    list = exportData(
        sql="SELECT * FROM `type_books` WHERE 1",
        val=(),
        fetch_all=True
    )

    return jsonify(list), 200


@typeBook_bp.route('/upload_type_image_book', methods=['POST'])
def uploadImageBook():
    UPLOAD_FOLDER = 'public/image/'
    # Tạo thư mục nếu chưa có
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Kiểm tra file ảnh
    if 'image' not in request.files:
        return jsonify({"error": "No image file found"}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Đổi tên file an toàn
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    text_output = scans(image_path)

    # Trả về đường dẫn ảnh hợp lệ
    return jsonify({
        "message": "Upload successful",
        "file_path": f"/{image_path}",
        "label": text_output["label"],
        "number": text_output["number"]}
    ), 200

@typeBook_bp.route('/public/image/<path:filename>')
def serve_image(filename):
    return send_from_directory("public/image", filename)