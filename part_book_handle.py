import json
import os
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from AI.scan_book import scan_book
from AI.scan_image import scans
from connectDatabase import importData, exportData

book_bp = Blueprint('book', __name__)

@book_bp.route('/upload_image_book', methods=['POST'])
def upload_book():
    UPLOAD_FOLDER = 'public/image_book_client/'
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

    text_output = scan_book(image_path)

    book = exportData(
        sql="SELECT * FROM `type_books` WHERE `id` = %s",
        val=(text_output,)
    )

    # Chuyển đổi kết quả sang JSON


    print(book)

    # Trả về đường dẫn ảnh hợp lệ
    return jsonify({
        "message": "Upload successful",
        "data": book
    }), 200
@book_bp.route('/insertBook', methods=['POST'])
def insertBook():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        print(data)

        # Trả phản hồi về Flutter
        return jsonify({"message": "Thêm sách thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400