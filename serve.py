import json
import os

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename, send_file

from connectDatabase import importData, exportData
from part_book_handle import book_bp
from sendEmail import sendMail

from part_image_handle import image_bp
from part_tyepBook_handle import typeBook_bp

app = Flask(__name__)
CORS(app)


@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter

        user = exportData(
            sql="SELECT * FROM users WHERE email = %s AND password = %s",
            val=(data["email"], data["password"]),
        )
        # Thanh đổi định dạng ngày trong danh sách
        data_list = list(user)
        data_list[6] = data_list[6].isoformat()
        user = tuple(data_list)
        print(user)
        return jsonify(user), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter

        importData(
            sql="""INSERT INTO `users`
                    (`name`, `email`, `password`, `status`, `cccd`, `dob`, `gender`, `pob`, `address`, `point`, `token`, `created_at`, `updated_at`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())""",
            val=(
                data["name"], data["email"], data["password"],
                "5", data["cccd"], data["dob"], data["gender"],
                "", data["address"], 0, data["token"]
            )
        )

        print(data)

        # Trả phản hồi về Flutter
        return jsonify({"message": "Đăng ký thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/sendOtp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        if not data or "email" not in data or "code" not in data:
            return jsonify({"error": "Thiếu email hoặc mã OTP!"}), 400

        sendMail(data["email"], "Code Otp", f"Mã OTP của bạn là: {data['code']}")

        return jsonify({"message": "Mã OTP đã được gửi!"}), 200
    except Exception as e:
        print(f"❌ Lỗi trong send_otp(): {e}")
        return jsonify({"error": str(e)}), 500


app.register_blueprint(image_bp)
app.register_blueprint(typeBook_bp)
app.register_blueprint(book_bp)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
