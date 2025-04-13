import os
import shutil
from ultralytics import YOLO
from PIL import Image

# Định nghĩa thư mục AI
AI_FOLDER = "AI"

def scan_book(file_path):
    global class_name
    output_folder = os.path.join(AI_FOLDER, 'scan_book')
    model = YOLO('D:\\VKU\\3\\DACN1\\ServerDACN1\\AI\\model_book.pt')

    # Chạy mô hình YOLO
    results = model.predict(source=file_path, save=True)

    # Kiểm tra có phát hiện được đối tượng không
    if results and results[0].boxes is not None and len(results[0].boxes.xyxy) > 0:
        os.makedirs(output_folder, exist_ok=True)


        filename = os.path.basename(file_path)
        saved_file_path = f"./runs/detect/predict/{filename}"
        new_file_path = os.path.join(output_folder, filename)
        if os.path.exists(saved_file_path):
            shutil.move(saved_file_path, new_file_path)


        for i, (box, cls) in enumerate(zip(results[0].boxes.xyxy, results[0].boxes.cls)):
            class_name = model.names[int(cls)].lower()


        # Xóa thư mục runs sau khi xong
        shutil.rmtree("./runs", ignore_errors=True)

        return class_name

    return False


