import json
import os
from datetime import datetime

from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from connectDatabase import importData, exportData, importDataGetId

cart_bp = Blueprint('cart', __name__)

@cart_bp.route("/export_cart_purchase", methods=['POST'])
def export_cart_purchase():
    data = request.get_json()

    list = exportData(
        sql="""
        SELECT 
            cart.id, 
            cart.status, 
            cart.address, 
            cart.total, 
            users.name 
        FROM `cart` JOIN users 
        ON cart.id_seller = users.id 
        WHERE cart.id_user = %s """,
        val=(data["id_user"],),
        fetch_all=True
    )
    return jsonify(list), 200

@cart_bp.route("/export_cart_seller", methods=['POST'])
def export_cart_seller():
    data = request.get_json()

    list = exportData(
        sql="""
        SELECT 
            cart.id, 
            cart.status, 
            cart.address, 
            cart.total, 
            users.name 
        FROM `cart` JOIN users 
        ON cart.id_user = users.id 
        WHERE cart.id_seller = %s """,
        val=(data["id_user"],),
        fetch_all=True
    )

    return jsonify(list), 200


@cart_bp.route("/update_state_cart", methods=['POST'])
def update_state_cart():
    try:
        data = request.get_json()
        now = datetime.now()
        print(data)

        # Kiểm tra trường dữ liệu bắt buộc
        required_fields = ["state", "total", "id_user", "id_cart"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Thiếu trường dữ liệu cần thiết."}), 400

        # Cộng điểm nếu đơn hàng đã chuyển
        if data["state"] == "Đã chuyển":
            importData(
                sql="""UPDATE `users` SET `point` = `point` + %s WHERE id = %s""",
                val=(int(data["total"]), data["id_user"]),
            )

        # Cập nhật trạng thái đơn hàng
        result = importData(
            sql="""
            UPDATE `cart` 
            SET `status` = %s,
                `updated_at` = %s
            WHERE `id` = %s
            """,
            val=(data["state"], now, data["id_cart"])
        )

        return jsonify({"message": "Cập nhật trạng thái giỏ hàng thành công", "result": result})

    except Exception as e:
        return jsonify({"error": f"Lỗi xử lý: {str(e)}"}), 500

@cart_bp.route("/export_item_cart", methods=['POST'])
def export_item_cart():
    data = request.get_json()

    list = exportData(
        sql=""
            "SELECT detail_cart.id, detail_cart.quantity, detail_cart.id_book,book.date_purchase, book.price,book.description, book.image,type_books.name_book  FROM `detail_cart` JOIN book ON detail_cart.id_book = book.id JOIN type_books ON book.id_type_book = type_books.id WHERE detail_cart.id_cart = %s ",
        val=(int(data["id_cart"]),),
        fetch_all=True,
    )

    print(list)

    return jsonify(list), 200


@cart_bp.route('/insert_cart', methods=['POST'])
def insertCart():
    data = request.get_json()
    address = data.get("address", "")
    total_raw = data.get("total", "0")
    all_items = data.get("data", {})
    id_user = int(data.get("id_user", 0))

    total_list = [int(t.strip()) for t in total_raw.split('-') if t.strip().isdigit()]
    now = datetime.now()



    try:
        for index, (seller_id, books_json) in enumerate(all_items.items()):
            if not books_json:
                continue

            books = json.loads(books_json)
            total = total_list[index] if index < len(total_list) else 0

            cart_id = importDataGetId(
                sql="""
                    INSERT INTO cart (
                        status, address, total, id_user, id_seller, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                val=("Đã xác nhận", address, total, id_user, int(seller_id), now, now)
            )

            importData(
                sql="""UPDATE `users` SET `point` = `point` - %s WHERE id = %s""",
                val=(int(total), id_user)
            )

            for book_detail_json in books.values():
                book_detail = json.loads(book_detail_json)
                quantity = book_detail.get("quantity", 0)
                book_info = book_detail.get("bookModal", {})
                id_book = int(book_info.get("id", 0))

                importData(
                    sql="""
                        INSERT INTO detail_cart (quantity, id_book, id_cart)
                        VALUES (%s, %s, %s)
                    """,
                    val=(quantity, id_book, cart_id)
                )

        return {"message": "Insert successful"}, 200

    except Exception as e:
        print("Error inserting cart:", e)
        return {"message": "Insert failed", "error": str(e)}, 500


