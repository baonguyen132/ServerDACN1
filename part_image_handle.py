import os
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from connectDatabase import importData, exportData

image_bp = Blueprint('image', __name__)

UPLOAD_FOLDER = 'uploads'

@image_bp.route('/upload_image', methods=['POST'])
def upload_file():
    UPLOAD_FOLDER = 'uploads'
    # Kiểm tra số có được gửi lên không
    number = request.form.get('number')
    status = request.form.get('status')
    id = request.form.get('id')


    if not number:
        return jsonify({"error": "Missing number"}), 400

    # Tạo thư mục theo số
    folder_path = os.path.join(UPLOAD_FOLDER, number)
    os.makedirs(folder_path, exist_ok=True)

    # Kiểm tra file ảnh
    if 'image' not in request.files:
        return jsonify({"error": "No image file found"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Lưu ảnh vào thư mục tương ứng
    image_path = os.path.join(folder_path, image.filename)
    image.save(image_path)

    importData(
        sql="""INSERT INTO `images`(`path`, `status`, `id_user`) VALUES (%s,%s,%s)""",
        val=(image_path , status , id)
    )

    return jsonify({"message": "Upload successful", "file_path": image_path})
@image_bp.route('/export_image_avata', methods=['POST'])
def export_image_avata():
    try:
        data = request.get_json()  # Nhận JSON từ Flutter
        user_id = data.get('id')

        if not user_id:
            return jsonify({"error": "Thiếu tham số 'id'"}), 400

        # Truy vấn ảnh mới nhất (ID lớn nhất)
        path_result = exportData(
            sql="SELECT `path` FROM `images` WHERE `id_user` = %s ORDER BY `id` DESC LIMIT 1",
            val=(user_id,),
        )

        if not path_result:
            return jsonify({"error": "Không tìm thấy ảnh"}), 404

        # Nếu kết quả là danh sách, lấy phần tử đầu tiên
        image_path = path_result[0] if isinstance(path_result, list) else path_result

        print(f"Ảnh mới nhất: {image_path}")
        return jsonify({"path": image_path}), 200

    except Exception as e:
        print(f"Lỗi server: {e}")
        return jsonify({"error": str(e)}), 500

@image_bp.route('/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory("uploads", filename)