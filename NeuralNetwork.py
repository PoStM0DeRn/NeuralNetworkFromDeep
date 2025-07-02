# INSERT_YOUR_CODE
import os
import csv




CSV_PATH = "labels.csv" 

def create_labels_csv(root_dir="Generated_images", csv_path="labels.csv"):


    """
    Создает CSV-файл с разметкой изображений и их классов.
    Название класса — это название директории, в которой хранится изображение.
    Параметры:
        root_dir: str — корневая директория с изображениями
        csv_path: str — путь к выходному CSV-файлу
    """
    rows = []
    for class_dir in sorted(os.listdir(root_dir)):
        class_path = os.path.join(root_dir, class_dir)
        if not os.path.isdir(class_path):
            continue
        for fname in sorted(os.listdir(class_path)):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                img_path = os.path.join(class_path, fname)
                # Относительный путь для удобства
                rel_path = os.path.relpath(img_path, root_dir)
                rows.append([rel_path, class_dir])
    # Записываем в CSV
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["image_path", "class"])
        writer.writerows(rows)
        
    print(f"Разметка сохранена в {csv_path}")


    # INSERT_YOUR_CODE
def load_csv_data(csv_path):
    """
    Читает CSV-файл и разбивает его на входные (X) и выходные (y) данные.
    Возвращает два списка: X (пути к изображениям), y (метки классов).
    """
    X = []
    y = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        header = next(reader)  # пропускаем заголовок
        for row in reader:
            if len(row) < 2:
                continue
            X.append(row[0])
            y.append(row[1])
    return X, y

create_labels_csv()
data = []
with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",")
    header = next(reader)  # пропускаем заголовок
    for row in reader:
        if len(row) < 2:
            continue
        data.append([row[0], row[1]])

# INSERT_YOUR_CODE
import random
random.shuffle(data)


print(data)








