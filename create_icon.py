from PIL import Image, ImageDraw
import os

def create_icon():
    # Создаем изображение 256x256
    size = 256
    img = Image.new('RGB', (size, size), color='#ff4757')
    draw = ImageDraw.Draw(img)
    
    # Рисуем простой YouTube логотип
    # Красный прямоугольник
    draw.rectangle([50, 50, 206, 206], fill='#ff0000')
    # Белый треугольник (play)
    draw.polygon([(90, 80), (90, 176), (170, 128)], fill='white')
    
    # Сохраняем как ICO
    img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("✅ Иконка создана: icon.ico")

if __name__ == "__main__":
    create_icon()