import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading
import os


# ============================================================
# НАСТРОЙКИ
# ============================================================

ASCII_CHARS = "@%#*+=-:. "

ASCII_WIDTH = 50

FONT_SIZE = 8

# Частота обновления предпросмотра
PREVIEW_INTERVAL = 30


# ============================================================
# ASCII-ПРЕОБРАЗОВАНИЕ
# ============================================================

def frame_to_ascii(frame, width=ASCII_WIDTH):
    """
    Преобразует один кадр видео в список ASCII-строк.
    """

    # BGR -> grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    height, original_width = gray.shape

    # Корректируем высоту с учетом пропорций символов
    aspect_ratio = height / original_width

    new_height = max(
        1,
        int(width * aspect_ratio * 0.5)
    )

    # Уменьшаем изображение
    resized = cv2.resize(
        gray,
        (width, new_height),
        interpolation=cv2.INTER_AREA
    )

    ascii_lines = []

    for row in resized:

        line = ""

        for brightness in row:

            index = int(
                brightness / 256 * len(ASCII_CHARS)
            )

            line += ASCII_CHARS[index]

        ascii_lines.append(line)

    return ascii_lines


def ascii_to_image(ascii_lines):
    """
    Превращает ASCII-текст в изображение.
    """

    font = ImageFont.truetype(
        "/System/Library/Fonts/Menlo.ttc",
        FONT_SIZE
    )

    # Временное изображение для измерения символа
    temp = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp)

    bbox = draw.textbbox(
        (0, 0),
        "A",
        font=font
    )

    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]

    width = len(ascii_lines[0]) * char_width
    height = len(ascii_lines) * char_height

    image = Image.new(
        "RGB",
        (width, height),
        "black"
    )

    draw = ImageDraw.Draw(image)

    for y, line in enumerate(ascii_lines):

        for x, char in enumerate(line):

            draw.text(
                (
                    x * char_width,
                    y * char_height
                ),
                char,
                font=font,
                fill="white"
            )

    return image


def convert_frame(frame):
    """
    Полный pipeline:

    видео-кадр
        ↓
    grayscale
        ↓
    resize
        ↓
    ASCII
        ↓
    изображение
    """

    ascii_lines = frame_to_ascii(frame)

    image = ascii_to_image(ascii_lines)

    return image


# ============================================================
# ГЛАВНОЕ ОКНО
# ============================================================

class ASCIIApp:

    def __init__(self, root):

        self.root = root

        self.root.title("ASCII Video")
        self.root.geometry("1000x750")

        self.root.configure(
            bg="#111111"
        )

        # Путь к исходному видео
        self.video_path = None

        # Последний результат
        self.result_path = None

        # Флаг обработки
        self.processing = False

        # ----------------------------------------------------
        # Заголовок
        # ----------------------------------------------------

        title = tk.Label(
            root,
            text="ASCII VIDEO",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#111111"
        )

        title.pack(
            pady=(20, 10)
        )

        # ----------------------------------------------------
        # Область видео
        # ----------------------------------------------------

        self.video_frame = tk.Frame(
            root,
            bg="black",
            width=900,
            height=500
        )

        self.video_frame.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        self.video_frame.pack_propagate(False)

        self.video_label = tk.Label(
            self.video_frame,
            bg="black"
        )

        self.video_label.pack(
            expand=True
        )

        # ----------------------------------------------------
        # Кнопки
        # ----------------------------------------------------

        buttons = tk.Frame(
            root,
            bg="#111111"
        )

        buttons.pack(
            pady=10
        )

        self.load_button = tk.Button(
            buttons,
            text="Загрузить видео",
            command=self.load_video,
            font=("Helvetica", 13),
            padx=20,
            pady=10
        )

        self.load_button.pack(
            side="left",
            padx=5
        )

        self.convert_button = tk.Button(
            buttons,
            text="Преобразовать",
            command=self.start_conversion,
            font=("Helvetica", 13),
            padx=20,
            pady=10,
            state="disabled"
        )

        self.convert_button.pack(
            side="left",
            padx=5
        )

        self.save_button = tk.Button(
            buttons,
            text="Сохранить",
            command=self.save_video,
            font=("Helvetica", 13),
            padx=20,
            pady=10,
            state="disabled"
        )

        self.save_button.pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------------
        # Прогресс
        # ----------------------------------------------------

        self.status_label = tk.Label(
            root,
            text="Выберите видео",
            font=("Helvetica", 11),
            fg="#cccccc",
            bg="#111111"
        )

        self.status_label.pack(
            pady=(0, 15)
        )


    # ========================================================
    # ЗАГРУЗКА ВИДЕО
    # ========================================================

    def load_video(self):

        path = filedialog.askopenfilename(
            title="Выберите видео",
            filetypes=[
                ("Video files",
                 "*.mp4 *.mov *.avi *.mkv"),
                ("All files", "*.*")
            ]
        )

        if not path:
            return

        self.video_path = path

        self.status_label.config(
            text=f"Выбрано: {os.path.basename(path)}"
        )

        self.convert_button.config(
            state="normal"
        )

        # Показываем первый кадр исходного видео
        self.show_first_frame()


    # ========================================================
    # ПОКАЗ ПЕРВОГО КАДРА
    # ========================================================

    def show_first_frame(self):

        video = cv2.VideoCapture(
            self.video_path
        )

        success, frame = video.read()

        video.release()

        if not success:
            messagebox.showerror(
                "Ошибка",
                "Не удалось открыть видео"
            )
            return

        # Просто показываем исходный кадр
        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(
            frame_rgb
        )

        self.show_image(image)


    # ========================================================
    # ПОКАЗ ИЗОБРАЖЕНИЯ
    # ========================================================

    def show_image(self, image):

        # Размер области предпросмотра
        max_width = 880
        max_height = 480

        image.thumbnail(
            (max_width, max_height),
            Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(
            image
        )

        self.video_label.config(
            image=photo
        )

        # Очень важно:
        # иначе Python удалит изображение из памяти
        self.video_label.image = photo


    # ========================================================
    # ЗАПУСК ОБРАБОТКИ
    # ========================================================

    def start_conversion(self):

        if not self.video_path:
            return

        if self.processing:
            return

        self.processing = True

        self.load_button.config(
            state="disabled"
        )

        self.convert_button.config(
            state="disabled"
        )

        self.save_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="Обработка..."
        )

        # Обрабатываем видео в отдельном потоке,
        # чтобы окно не зависало
        thread = threading.Thread(
            target=self.convert_video
        )

        thread.start()


    # ========================================================
    # ОБРАБОТКА ВИДЕО
    # ========================================================

    def convert_video(self):

        video = cv2.VideoCapture(
            self.video_path
        )

        if not video.isOpened():

            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Ошибка",
                    "Не удалось открыть видео"
                )
            )

            self.processing = False

            return

        fps = video.get(
            cv2.CAP_PROP_FPS
        )

        frame_count = int(
            video.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        # -----------------------------------------------
        # Читаем первый кадр
        # -----------------------------------------------

        success, frame = video.read()

        if not success:

            video.release()

            self.processing = False

            return

        first_image = convert_frame(
            frame
        )

        output_width, output_height = (
            first_image.size
        )

        # VideoWriter любит четные размеры
        output_width -= output_width % 2
        output_height -= output_height % 2

        # -----------------------------------------------
        # Временный файл
        # -----------------------------------------------

        temp_path = os.path.join(
            os.path.dirname(
                self.video_path
            ),
            "ascii_result.mp4"
        )

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        writer = cv2.VideoWriter(
            temp_path,
            fourcc,
            fps,
            (
                output_width,
                output_height
            )
        )

        # -----------------------------------------------
        # Обрабатываем первый кадр
        # -----------------------------------------------

        frame_array = np.array(
            first_image
        )

        frame_bgr = cv2.cvtColor(
            frame_array,
            cv2.COLOR_RGB2BGR
        )

        frame_bgr = frame_bgr[
            :output_height,
            :output_width
        ]

        writer.write(
            frame_bgr
        )

        # Показываем первый ASCII-кадр
        self.root.after(
            0,
            lambda img=first_image.copy():
                self.show_image(img)
        )

        # -----------------------------------------------
        # Остальные кадры
        # -----------------------------------------------

        current_frame = 1

        while True:

            success, frame = video.read()

            if not success:
                break

            ascii_image = convert_frame(
                frame
            )

            frame_array = np.array(
                ascii_image
            )

            frame_bgr = cv2.cvtColor(
                frame_array,
                cv2.COLOR_RGB2BGR
            )

            frame_bgr = frame_bgr[
                :output_height,
                :output_width
            ]

            writer.write(
                frame_bgr
            )

            current_frame += 1

            # Обновляем предпросмотр примерно
            # каждые 30 кадров
            if current_frame % PREVIEW_INTERVAL == 0:

                preview = ascii_image.copy()

                self.root.after(
                    0,
                    lambda img=preview:
                        self.show_image(img)
                )

                progress = (
                    current_frame
                    / frame_count
                    * 100
                )

                self.root.after(
                    0,
                    lambda p=progress:
                        self.status_label.config(
                            text=f"Обработка: {p:.1f}%"
                        )
                )

        video.release()
        writer.release()

        self.result_path = temp_path

        self.processing = False

        # Возвращаем интерфейс в главный поток
        self.root.after(
            0,
            self.conversion_finished
        )


    # ========================================================
    # ОБРАБОТКА ЗАКОНЧИЛАСЬ
    # ========================================================

    def conversion_finished(self):

        self.status_label.config(
            text="Готово! Можно сохранить видео."
        )

        self.save_button.config(
            state="normal"
        )

        self.load_button.config(
            state="normal"
        )


    # ========================================================
    # СОХРАНЕНИЕ
    # ========================================================

    def save_video(self):

        if not self.result_path:
            return

        path = filedialog.asksaveasfilename(
            title="Сохранить ASCII-видео",
            defaultextension=".mp4",
            filetypes=[
                ("MP4 video", "*.mp4")
            ]
        )

        if not path:
            return

        try:

            # Копируем готовое видео
            import shutil

            shutil.copy2(
                self.result_path,
                path
            )

            messagebox.showinfo(
                "Готово",
                f"Видео сохранено:\n{path}"
            )

        except Exception as e:

            messagebox.showerror(
                "Ошибка",
                str(e)
            )


# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ASCIIApp(root)

    root.mainloop()