from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import csv
from glob import glob
import numpy as np


# Конфигурация
FONT_PATH = "GOST2304A.ttf"  # Путь к файлу шрифта (поддерживающему кириллицу)
FONT_SIZE = 36  # Размер шрифта (будет масштабироваться под изображение)
IMAGE_SIZE = (28, 28)  # Размер выходного изображения
BACKGROUND_COLOR = (255, 255, 255)  # Белый фон
TEXT_COLOR = (0, 0, 0)  # Черный цвет текста
NUM_IMAGES = 10  # Количество изображений на букву

# Список русских букв
RUSSIAN_LETTERS = [
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й',
    'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
    'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я'
]







def smart_binarize(image, variability=True):
    """
    Умная бинаризация с сохранением особенностей букв

    Параметры:
        image: PIL.Image - входное изображение
        variability: bool - добавлять случайные вариации

    Возвращает:
        PIL.Image - бинаризованное изображение с сохранением особенностей
    """
    # Конвертируем в grayscale
    if image.mode != 'L':
        image = image.convert('L')

    # Применяем легкое размытие для сглаживания артефактов
    image = image.filter(ImageFilter.GaussianBlur(radius=0.7))

    # Создаем массив
    img_array = np.array(image)

    if variability:
        # Динамический порог с вариациями
        base_threshold = np.random.randint(120, 160)
        threshold_variation = np.random.randint(5, 20)

        # Создаем маску с градиентным порогом
        x = np.arange(img_array.shape[1])
        y = np.arange(img_array.shape[0])
        xx, yy = np.meshgrid(x, y)

        # Градиентный порог (имитация неравномерного освещения)
        threshold_map = base_threshold + threshold_variation * np.sin(xx / 30)
    else:
        # Фиксированный порог для стабильного результата
        threshold_map = np.full_like(img_array, 128)

    # Применяем адаптивную бинаризацию
    binary_array = np.where(img_array < threshold_map, 0, 255)

    # Добавляем случайные артефакты (5% вероятности)
    if variability and np.random.random() < 0.05:
        # Случайные точки
        noise = np.random.randint(0, 2, size=img_array.shape) * 255
        binary_array = np.where(noise > 0, noise, binary_array)

    # Конвертируем обратно в изображение
    result = Image.fromarray(binary_array.astype(np.uint8))

    # Применяем морфологические операции для улучшения формы
    if variability:
        iterations = np.random.randint(0, 2)
        for _ in range(iterations):
            if np.random.random() > 0.5:
                result = result.filter(ImageFilter.MinFilter(3))
            else:
                result = result.filter(ImageFilter.MaxFilter(3))

    return result


def add_noise(image):
    """
    Добавляет гауссов шум на изображение в оттенках серого
    (шум одинаков для всех каналов, сохраняя изображение серым)
    """
    # Конвертируем в numpy array и преобразуем в grayscale
    img_array = np.array(image.convert('L'))  # 'L' - режим оттенков серого
    height, width = img_array.shape
    noisy = img_array.copy()

    # Параметры гауссова шума
    mean = 0
    var = np.random.uniform(0.001, 0.02)  # Диапазон дисперсии
    sigma = var ** 0.5

    # Генерируем шум (один канал)
    gauss = np.random.normal(mean, sigma, (height, width))

    # Применяем шум и обрезаем значения
    noisy = np.clip(noisy + gauss * 255, 0, 255).astype(np.uint8)

    # Конвертируем обратно в RGB (но сохраняем оттенки серого)
    return Image.fromarray(noisy).convert('RGB')


def create_letter_image(letter, font_path, slant=0.2):
    """Создает изображение с наклонной буквой"""
    # Загружаем шрифт
    try:
        base_font = ImageFont.truetype(font_path, FONT_SIZE)
    except OSError as e:
        print(f"Ошибка загрузки шрифта: {font_path}")
        print(e)
        return

    # Создаем временное изображение для измерения текста
    temp_image = Image.new('RGB', IMAGE_SIZE, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(temp_image)
    text_width, text_height = draw.textbbox((0, 0), letter, font=base_font)[2:]

    # Создаем основное изображение с учетом наклона
    image = Image.new('RGB',
                      (int(IMAGE_SIZE[0] + abs(slant * text_height)), IMAGE_SIZE[1]),
                      BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    # Рисуем текст с наклоном
    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2
    draw.text((x, y), letter, font=base_font, fill=TEXT_COLOR)

    return image


def main():
    # Загружаем шрифт
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print(f"Ошибка: Шрифт по пути '{FONT_PATH}' не найден")
        return

    # Создаем корневую директорию


    for letter in RUSSIAN_LETTERS:
        # Создаем директорию для буквы
        letter_dir = f"Generated_images/Letter_{letter}"
        os.makedirs(letter_dir, exist_ok=True)

        # Генерируем эталонное изображение
        #img = smart_binarize(img)
        # Сохраняем NUM_IMAGES копий
        for i in range(NUM_IMAGES):
            img = create_letter_image(letter, FONT_PATH)
            img = add_noise(img)
            file_name = f"Letter_{letter}_{i:04d}.png"
            file_path = os.path.join(letter_dir, file_name)
            img.save(file_path)

        print(f"Сгенерировано {NUM_IMAGES} изображений для буквы '{letter}'")


if __name__ == "__main__":
    main()