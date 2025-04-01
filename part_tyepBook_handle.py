import os
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from AI.scan_image import scans
from connectDatabase import importData, exportData

typeBook_bp = Blueprint('type_book', __name__)

@typeBook_bp.route('/insertBook', methods=['POST'])
def insertTypeBook():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        print(data)
        importData(
            sql="""INSERT INTO `type_books`
                    (`name_book`, `type_book`, `image`, `description`, `created_at`, `updated_at`)
                    VALUES (%s, %s, %s, %s, NOW(), NOW())""",
            val=(
                data["name_book"], data["type_book"], data["image"], data["description"]
            )
        )

        # Trả phản hồi về Flutter
        return jsonify({"message": "Thêm sách thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@typeBook_bp.route('/upload_image_book', methods=['POST'])
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
    return jsonify({"message": "Upload successful", "file_path": f"/{image_path}", "label": text_output["label"], "number": text_output["number"]} ), 200