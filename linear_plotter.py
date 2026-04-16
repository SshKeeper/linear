import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, TextBox, Button
import matplotlib.ticker as ticker
import matplotlib.patches as patches

# Настройка бэкенда для отображения в отдельном окне или inline
import matplotlib
# Используем Qt5Agg как основной, так как он более стабилен в Linux средах
try:
    matplotlib.use('Qt5Agg')
except ImportError:
    try:
        matplotlib.use('TkAgg')
    except ImportError:
        matplotlib.use('Agg')  # Для сред без GUI

class LinearFunctionPlotter:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(left=0.1, bottom=0.35, right=0.95, top=0.95)
        
        # Исходные данные
        self.k = 1.0
        self.b = 0.0
        self.x_point = 2.0
        self.step_x = 0.5
        self.step_y = 2.0
        
        # Генерация данных для линии
        self.x = np.linspace(-10, 10, 400)
        self.line, = self.ax.plot(self.x, self.k * self.x + self.b, 'b-', linewidth=2, label='y = kx + b')
        
        # Точка на графике
        self.point_scatter = self.ax.scatter([self.x_point], [self.k * self.x_point + self.b], c='red', zorder=5)
        
        # Линии для отображения угла
        self.angle_line_h = self.ax.plot([], [], 'r--', alpha=0.5)[0] # Горизонтальная проекция
        self.angle_line_diag = self.ax.plot([], [], 'g--', alpha=0.5)[0] # Участок графика
        
        # Настройки осей и сетки
        self.ax.set_title("Линейная функция: Редактирование коэффициентов и сетки")
        self.ax.grid(True, which='both', linestyle='--', alpha=0.7)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.legend(loc='upper left')
        self.ax.set_aspect('auto') # Позволяет масштабировать оси независимо
        
        # --- Создание виджетов управления ---
        
        # Область для слайдеров
        ax_slider_k = plt.axes([0.125, 0.25, 0.75, 0.03])
        ax_slider_b = plt.axes([0.125, 0.22, 0.75, 0.03])
        ax_slider_x = plt.axes([0.125, 0.19, 0.75, 0.03])
        
        self.slider_k = Slider(ax_slider_k, 'Коэфф. k (Наклон)', -10.0, 10.0, valinit=self.k)
        self.slider_b = Slider(ax_slider_b, 'Коэфф. b (Сдвиг)', -10.0, 10.0, valinit=self.b)
        self.slider_x = Slider(ax_slider_x, 'Точка X (для угла)', -10.0, 10.0, valinit=self.x_point)
        
        # Область для текстовых полей (сетка и масштаб)
        ax_box_dx = plt.axes([0.125, 0.14, 0.2, 0.04])
        ax_box_dy = plt.axes([0.425, 0.14, 0.2, 0.04])
        ax_box_xlim = plt.axes([0.125, 0.10, 0.2, 0.04])
        ax_box_ylim = plt.axes([0.425, 0.10, 0.2, 0.04])
        
        self.box_dx = TextBox(ax_box_dx, 'Step X:', initial=str(self.step_x))
        self.box_dy = TextBox(ax_box_dy, 'Step Y:', initial=str(self.step_y))
        self.box_xlim = TextBox(ax_box_xlim, 'X Limit (±):', initial='10')
        self.box_ylim = TextBox(ax_box_ylim, 'Y Limit (±):', initial='10')
        
        # Подключение событий
        self.slider_k.on_changed(self.update_graph)
        self.slider_b.on_changed(self.update_graph)
        self.slider_x.on_changed(self.update_graph)
        
        self.box_dx.on_submit(self.update_grid_and_view)
        self.box_dy.on_submit(self.update_grid_and_view)
        self.box_xlim.on_submit(self.update_grid_and_view)
        self.box_ylim.on_submit(self.update_grid_and_view)
        
        # Первичная отрисовка
        self.update_graph(None)
        self.update_grid_and_view(None)
        
        plt.show()

    def update_graph(self, val):
        """Обновление линии, точки и угла при изменении слайдеров"""
        # Получаем значения
        self.k = self.slider_k.val
        self.b = self.slider_b.val
        self.x_point = self.slider_x.val
        
        # Обновляем линию функции
        y_vals = self.k * self.x + self.b
        self.line.set_ydata(y_vals)
        
        # Вычисляем координаты точки
        y_point = self.k * self.x_point + self.b
        self.point_scatter.set_offsets([[self.x_point, y_point]])
        
        # Рисуем угол
        # Горизонтальная линия от (x_point - 1, y_point) до (x_point, y_point)
        # Но лучше сделать фиксированную длину или до пересечения с сеткой. 
        # Сделаем отступ в 1 единицу по X для наглядности угла
        h_start_x = self.x_point - 1.5 if self.k >= 0 else self.x_point - 1.5
        # Для визуализации угла нарисуем луч от точки влево и луч по графику
        
        # Луч горизонтальный (проекция на ось X относительно точки)
        # Рисуем от точки влево на некоторую дистанцию
        dist = 2.0 
        hx = [self.x_point - dist, self.x_point]
        hy = [y_point, y_point]
        self.angle_line_h.set_data(hx, hy)
        
        # Луч по графику (от точки назад на ту же дистанцию по X)
        gx = [self.x_point - dist, self.x_point]
        gy = [self.k * (self.x_point - dist) + self.b, y_point]
        self.angle_line_diag.set_data(gx, gy)
        
        # Рисуем дугу угла
        angle_rad = np.arctan(self.k)
        angle_deg = np.degrees(angle_rad)
        
        # Параметры для дуги
        arc_radius = 0.5 * (self.ax.get_xlim()[1] - self.ax.get_xlim()[0]) / 20
        if arc_radius < 0.1:
            arc_radius = 0.1
            
        theta1 = 0
        theta2 = angle_deg
        
        # Удаляем старые дуги и текст перед добавлением новых
        for artist in self.ax.artists[:]:
            if isinstance(artist, patches.Arc):
                artist.remove()
        for child in self.ax.get_children():
            if hasattr(child, 'get_text') and '°' in str(child.get_text()):
                child.remove()
        
        # Рисуем дугу
        arc = patches.Arc((self.x_point, y_point), 
                         2*arc_radius, 2*arc_radius,
                         angle=0,
                         theta1=theta1,
                         theta2=theta2,
                         color='green', linewidth=2)
        self.ax.add_patch(arc)
        
        # Подпись угла
        label_x = self.x_point + arc_radius * np.cos(np.radians(angle_deg/2))
        label_y = y_point + arc_radius * np.sin(np.radians(angle_deg/2))
        self.ax.text(label_x, label_y, f'{angle_deg:.1f}°', color='green', fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
        
        # Обновляем заголовок с текущими значениями
        self.ax.set_title(f"y = {self.k:.2f}x + {self.b:.2f} | Точка: ({self.x_point:.2f}, {y_point:.2f})")
        
        self.fig.canvas.draw_idle()

    def update_grid_and_view(self, text):
        """Обновление сетки и масштабов осей из текстовых полей"""
        try:
            # Чтение значений
            dx = float(self.box_dx.text.strip())
            dy = float(self.box_dy.text.strip())
            lim_x = float(self.box_xlim.text.strip())
            lim_y = float(self.box_ylim.text.strip())
            
            # Проверка на положительность шагов
            if dx <= 0 or dy <= 0:
                raise ValueError("Шаг должен быть > 0")
                
            self.step_x = dx
            self.step_y = dy
            
            # Настройка сетки
            self.ax.xaxis.set_major_locator(ticker.MultipleLocator(self.step_x))
            self.ax.yaxis.set_major_locator(ticker.MultipleLocator(self.step_y))
            
            # Настройка пределов осей (масштабирование)
            self.ax.set_xlim(-lim_x, lim_x)
            self.ax.set_ylim(-lim_y, lim_y)
            
            # Принудительное обновление канваса
            self.fig.canvas.draw_idle()
            
        except ValueError:
            # Если введено не число, просто игнорируем или можно подсветить ошибку
            pass

if __name__ == "__main__":
    app = LinearFunctionPlotter()
