import json
import os
from datetime import datetime

from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from connectDatabase import importData, exportData, importDataGetId

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
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

@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter

        importData(
            sql="""INSERT INTO `users`
                    (`name`, `email`, `password`, `status`, `cccd`, `dob`, `gender`, `pob`, `address`, `point`, `token`, `created_at`, `updated_at`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())""",
            val=(
                data["name"], data["email"], data["password"],
                "4", data["cccd"], data["dob"], data["gender"],
                "", data["address"],data["point"], data["token"]
            )
        )

        print(data)

        # Trả phản hồi về Flutter
        return jsonify({"message": "Đăng ký thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/loadUser', methods=['POST'])
def loadUser():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter

        user = exportData(
            sql="SELECT * FROM users WHERE id = %s",
            val=(data["id_user"],),
        )

        return jsonify(user), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

@user_bp.route('/loadDataUser', methods=['GET'])
def loadDataUser():
    try:
        user = exportData(
            sql="SELECT * FROM users",
            val=(),
            fetch_all=True
        )
        print(user)
        return jsonify(user), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400