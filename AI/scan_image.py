import os
import cv2
import shutil
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR
from PIL import Image

# Định nghĩa thư mục AI
AI_FOLDER = "AI"
os.makedirs(AI_FOLDER, exist_ok=True)

def convert_to_black_white(image_path):
    """Chuyển ảnh về trắng đen (nhị phân) với Otsu's Thresholding."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Chuyển sang ảnh xám

    if img is None:
        print(f"Lỗi: Không thể đọc ảnh {image_path}")
        return None

    # Làm mờ ảnh để giảm nhiễu trước khi nhị phân hóa
    blurred = cv2.GaussianBlur(img, (3, 3), 0)

    # Áp dụng nhị phân với Otsu's thresholding
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary


def recognize_text(image_path):
    """Nhận diện văn bản từ ảnh."""
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Hỗ trợ xoay chữ
    result = ocr.ocr(image_path, cls=True)

    detected_text = []
    for line in result:
        if line:
            for word_info in line:
                detected_text.append(word_info[1][0])

    return " ".join(detected_text)


def scans(file_path):
    output_folder = os.path.join(AI_FOLDER, 'scan')
    cropped_folder = os.path.join(AI_FOLDER, 'cropped')
    model = YOLO('D:/VKU/3/DACN1/ServerDACN1/AI/model_label_number.pt')
    results = model.predict(source=file_path, save=True)

    if results and results[0].boxes is not None and len(results[0].boxes.xyxy) > 0:
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(cropped_folder, exist_ok=True)

        filename = os.path.basename(file_path)
        file_ext = os.path.splitext(filename)[1]
        saved_file_path = f"./runs/detect/predict/{filename}"
        new_file_path = os.path.join(output_folder, filename)

        if os.path.exists(saved_file_path):
            shutil.move(saved_file_path, new_file_path)

        cropped_paths = []
        image = Image.open(file_path)
        text_results = {}

        for i, (box, cls) in enumerate(zip(results[0].boxes.xyxy, results[0].boxes.cls)):
            x1, y1, x2, y2 = map(int, box)
            cropped_image = image.crop((x1, y1, x2, y2))
            class_name = model.names[int(cls)].lower()

            # Nếu là 'title' → OCR
            if class_name == "title":
                class_folder = os.path.join(cropped_folder, "label")
                os.makedirs(class_folder, exist_ok=True)
                cropped_image_path = os.path.join(class_folder, f"image_{i}{file_ext}")
                cropped_image.save(cropped_image_path)
                cropped_paths.append(cropped_image_path)

                # Trắng đen
                bw_img = convert_to_black_white(cropped_image_path)
                bw_img_path = os.path.join(class_folder, f"bw_{i}{file_ext}")
                cv2.imwrite(bw_img_path, bw_img)

                # Nhận diện chữ
                text_results["label"] = recognize_text(bw_img_path)

            # Nếu là số từ 1 → 12 → không OCR, chỉ gán key "text"
            elif class_name.isdigit() and 1 <= int(class_name) <= 12:
                text_results["number"] = class_name

            else:
                # Các nhãn khác → bỏ qua
                continue

        shutil.rmtree("./runs")
        return text_results

    return False
