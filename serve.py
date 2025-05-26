import json
import os

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename, send_file

from connectDatabase import importData, exportData
from part_book_handle import book_bp
from part_cart_handle import cart_bp
from part_user_handle import user_bp
from sendEmail import sendMail

from part_image_handle import image_bp
from part_tyepBook_handle import typeBook_bp

app = Flask(__name__)
CORS(app)


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
app.register_blueprint(cart_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
