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
        "data": book,
        "path": image_path
    }), 200
@book_bp.route('/insertBook', methods=['POST'])
def insertBook():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        importData(
            sql="""
            INSERT INTO `book`(`date_purchase`, `price`, `description`, `status`, `quantity` ,`image`, `id_user`, `id_type_book`, `created_at`, `updated_at`) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())""",
            val=(
                data["date_purchase"],
                data["price"],
                data["description"],
                data["status"],
                data["quantity"],
                data["image"],
                data["id_user"],
                data["id_type_book"]
            )
        )

        # Trả phản hồi về Flutter
        return jsonify({"message": "Thêm sách thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@book_bp.route("/exportMyBook" , methods=['POST'])
def exportMyBook():
    data = request.get_json()

    list = exportData(
        sql="""SELECT  
        book.id, 
        type_books.name_book, 
        type_books.type_book, 
        book.date_purchase, 
        book.price, 
        book.description, 
        book.image ,
        book.id_user,
        book.id_type_book,
        book.status,
        book.quantity
        FROM book JOIN type_books ON book.id_type_book = type_books.id 
        WHERE book.id_user = %s""",
        val=(data["id_user"],),
        fetch_all=True
    )

    return jsonify(list), 200

@book_bp.route("/exportBook", methods=['GET'])
def exportBook():
    books = exportData(
        sql="""
            SELECT  
                book.id, 
                type_books.name_book, 
                type_books.type_book, 
                book.date_purchase, 
                book.price, 
                book.description, 
                book.image,
                book.id_user,
                book.id_type_book,
                book.status,
                book.quantity
            FROM book 
            JOIN type_books ON book.id_type_book = type_books.id
            WHERE book.status = 1 AND book.quantity > 0
        """,
        val=(),
        fetch_all=True
    )

    return jsonify(books), 200


@book_bp.route('/deleteBook', methods=['POST'])
def deleteBook():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        importData(
            sql="""DELETE FROM `book` WHERE `id` = %s """,
            val=(data["id"],)
        )

        if os.path.exists(data["image"]):
            os.remove(data["image"])
            print("Đã xóa ảnh.")
        else:
            print("Ảnh không tồn tại.")

        # Trả phản hồi về Flutter
        return jsonify({"message": "Xoá thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@book_bp.route('/updateBook', methods=['POST'])
def updateBook():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        importData(
            sql="""
            UPDATE `book` SET 
            `date_purchase`=%s,
            `price`=%s,
            `description`=%s,
            `quantity`=%s,
            `updated_at`=NOW() 
            WHERE `id`= %s """,
            val=(
                data["date_purchase"], data["price"], data["description"],data["quantity"] ,data["id"]
            )
        )

        # Trả phản hồi về Flutter
        return jsonify({"message": "Cập nhật thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@book_bp.route('/public/image_book_client/<path:filename>')
def serve_image(filename):
    return send_from_directory("public/image_book_client", filename)