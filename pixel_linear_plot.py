import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PixelLinearPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Линейная функция по пикселям")
        
        # Параметры масштаба (пикселей на условную единицу)
        self.scale_x = 10.0  # пикселей в 1 уд по X
        self.scale_y = 10.0  # пикселей в 1 уд по Y
        
        # Точки в пиксельных координатах [(x_px, y_px), ...]
        self.points = []
        self.max_points = 2
        
        # Создание основного фрейма
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создание фигуры matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Настройка осей
        self.ax.set_aspect('auto')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_xlabel('X (условные единицы)')
        self.ax.set_ylabel('Y (условные единицы)')
        self.ax.set_title('График линейной функции')
        
        # Привязка событий
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('resize_event', self.on_resize)
        
        # Панель управления
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        # Поля ввода масштаба
        ttk.Label(control_frame, text="Масштаб X (px/уд):").grid(row=0, column=0, padx=5, pady=2)
        self.entry_scale_x = ttk.Entry(control_frame, width=10)
        self.entry_scale_x.insert(0, "10")
        self.entry_scale_x.grid(row=0, column=1, padx=5, pady=2)
        self.entry_scale_x.bind('<Return>', self.update_scale)
        
        ttk.Label(control_frame, text="Масштаб Y (px/уд):").grid(row=0, column=2, padx=5, pady=2)
        self.entry_scale_y = ttk.Entry(control_frame, width=10)
        self.entry_scale_y.insert(0, "10")
        self.entry_scale_y.grid(row=0, column=3, padx=5, pady=2)
        self.entry_scale_y.bind('<Return>', self.update_scale)
        
        # Кнопка сброса
        self.btn_reset = ttk.Button(control_frame, text="Сброс", command=self.reset_points)
        self.btn_reset.grid(row=0, column=4, padx=10, pady=2)
        
        # Поля для отображения результатов
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.lbl_points = ttk.Label(results_frame, text="Точки (пиксели): Нет точек")
        self.lbl_points.pack(side=tk.LEFT, padx=5)
        
        self.lbl_coefficients = ttk.Label(results_frame, text="k = -, b = -")
        self.lbl_coefficients.pack(side=tk.LEFT, padx=5)
        
        self.lbl_angle = ttk.Label(results_frame, text="Угол: -°")
        self.lbl_angle.pack(side=tk.LEFT, padx=5)
        
        # Инициализация графика
        self.update_plot()
    
    def on_click(self, event):
        """Обработка клика мыши для добавления/перемещения точки"""
        if event.inaxes != self.ax:
            return
        
        # Преобразование координат события в пиксели относительно осей
        x_px = event.x
        y_px = event.y
        
        # Получаем границы осей в пикселях
        bbox = self.ax.get_window_extent()
        
        # Проверяем, находится ли клик внутри области графика
        if not bbox.contains(event.x, event.y):
            return
        
        # Добавляем новую точку
        if len(self.points) >= self.max_points:
            # Удаляем самую старую точку и добавляем новую
            self.points.pop(0)
        
        self.points.append((x_px, y_px))
        self.update_plot()
    
    def on_resize(self, event):
        """Обработка изменения размера окна"""
        self.update_plot()
    
    def update_scale(self, event=None):
        """Обновление масштаба осей"""
        try:
            new_scale_x = float(self.entry_scale_x.get())
            new_scale_y = float(self.entry_scale_y.get())
            
            if new_scale_x > 0 and new_scale_y > 0:
                self.scale_x = new_scale_x
                self.scale_y = new_scale_y
                self.update_plot()
        except ValueError:
            pass  # Игнорируем некорректный ввод
    
    def reset_points(self):
        """Сброс всех точек"""
        self.points = []
        self.update_plot()
    
    def calculate_coefficients(self):
        """Расчет коэффициентов k и b на основе пиксельных координат"""
        if len(self.points) < 2:
            return None, None
        
        p1 = self.points[0]
        p2 = self.points[1]
        
        # Разница в пикселях
        delta_px = p2[0] - p1[0]
        delta_py = p2[1] - p1[1]
        
        # Преобразование в условные единицы
        # Важно: в экранных координатах Y растет вниз, а в графике вверх
        # Поэтому инвертируем delta_py
        delta_ux = delta_px / self.scale_x
        delta_uy = -delta_py / self.scale_y  # Инверсия Y
        
        if abs(delta_ux) < 1e-10:  # Вертикальная линия
            return float('inf'), None
        
        k = delta_uy / delta_ux
        
        # Вычисляем b через первую точку
        # u1x, u1y - координаты первой точки в условных единицах
        # Для этого нужно знать начало координат в пикселях
        # Но мы можем выразить b через уравнение прямой
        
        # Найдем координаты первой точки в условных единицах относительно начала осей
        # Начало осей (0,0) в данных графика соответствует некоторой позиции в пикселях
        # Однако, поскольку мы работаем с относительными изменениями, 
        # нам нужно определить абсолютное положение
        
        # Получаем текущие пределы осей в условных единицах
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        # Получаем размеры области графика в пикселях
        bbox = self.ax.get_window_extent()
        width_px = bbox.width
        height_px = bbox.height
        
        # Вычисляем положение начала координат (0,0) в пикселях
        # x=0 соответствует левой границе, если xlim[0]=0
        origin_x_px = bbox.x0 + (0 - xlim[0]) * (width_px / (xlim[1] - xlim[0]))
        origin_y_px = bbox.y0 + (ylim[1] - 0) * (height_px / (ylim[1] - ylim[0]))
        
        # Координаты первой точки в условных единицах
        u1x = (p1[0] - origin_x_px) / self.scale_x
        u1y = (origin_y_px - p1[1]) / self.scale_y  # Инверсия Y
        
        b = u1y - k * u1x
        
        return k, b
    
    def calculate_screen_angle(self):
        """Расчет экранного угла в градусах"""
        if len(self.points) < 2:
            return None
        
        p1 = self.points[0]
        p2 = self.points[1]
        
        delta_x = p2[0] - p1[0]
        delta_y = p2[1] - p1[1]  # В экранных координатах Y растет вниз
        
        # Угол между линией и горизонталью экрана
        # Используем atan2 для правильного определения квадранта
        angle_rad = np.arctan2(-delta_y, delta_x)  # Инвертируем delta_y для стандартной системы
        angle_deg = np.degrees(angle_rad)
        
        # Нормализуем угол от 0 до 180 градусов
        if angle_deg < 0:
            angle_deg += 180
            
        return angle_deg
    
    def update_plot(self):
        """Обновление графика"""
        self.ax.clear()
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_xlabel('X (условные единицы)')
        self.ax.set_ylabel('Y (условные единицы)')
        self.ax.set_title('График линейной функции')
        
        # Обновляем информацию о точках
        if self.points:
            points_str = ", ".join([f"({int(p[0])}, {int(p[1])})" for p in self.points])
            self.lbl_points.config(text=f"Точки (пиксели): {points_str}")
        else:
            self.lbl_points.config(text="Точки (пиксели): Нет точек")
        
        # Если есть хотя бы две точки, рисуем линию и рассчитываем коэффициенты
        if len(self.points) >= 2:
            # Рисуем точки
            x_px = [p[0] for p in self.points]
            y_px = [p[1] for p in self.points]
            
            # Преобразуем пиксельные координаты в данные графика
            bbox = self.ax.get_window_extent()
            xlim = self.ax.get_xlim() if hasattr(self, '_xlim') else (-10, 10)
            ylim = self.ax.get_ylim() if hasattr(self, '_ylim') else (-10, 10)
            
            # Сохраняем текущие пределы
            self._xlim = xlim
            self._ylim = ylim
            
            width_px = bbox.width
            height_px = bbox.height
            
            # Функция преобразования пикселей в данные
            def px_to_data(px, py):
                dx = (px - bbox.x0) / width_px * (xlim[1] - xlim[0]) + xlim[0]
                dy = (bbox.y1 - py) / height_px * (ylim[1] - ylim[0]) + ylim[0]
                return dx, dy
            
            data_points = [px_to_data(px, py) for px, py in self.points]
            data_x = [p[0] for p in data_points]
            data_y = [p[1] for p in data_points]
            
            # Рисуем линию через все точки (для двух точек это отрезок)
            self.ax.plot(data_x, data_y, 'b-', linewidth=2, label='Линейная функция')
            
            # Рисуем точки
            self.ax.scatter(data_x, data_y, c='red', s=100, zorder=5, label='Точки')
            
            # Рассчитываем и отображаем коэффициенты
            k, b = self.calculate_coefficients()
            if k is not None:
                if np.isinf(k):
                    self.lbl_coefficients.config(text="k = ∞ (вертикальная линия), b = -")
                else:
                    self.lbl_coefficients.config(text=f"k = {k:.4f}, b = {b:.4f}")
            else:
                self.lbl_coefficients.config(text="k = -, b = -")
            
            # Рассчитываем и отображаем угол
            angle = self.calculate_screen_angle()
            if angle is not None:
                self.lbl_angle.config(text=f"Угол: {angle:.2f}°")
                
                # Рисуем дугу угла в первой точке
                self.draw_angle_arc(data_points[0], data_points[1], angle)
            else:
                self.lbl_angle.config(text="Угол: -°")
            
            self.ax.legend(loc='upper right')
        else:
            # Если точек меньше двух, просто рисуем имеющиеся точки
            if self.points:
                bbox = self.ax.get_window_extent()
                xlim = self.ax.get_xlim() if hasattr(self, '_xlim') else (-10, 10)
                ylim = self.ax.get_ylim() if hasattr(self, '_ylim') else (-10, 10)
                self._xlim = xlim
                self._ylim = ylim
                
                width_px = bbox.width
                height_px = bbox.height
                
                def px_to_data(px, py):
                    dx = (px - bbox.x0) / width_px * (xlim[1] - xlim[0]) + xlim[0]
                    dy = (bbox.y1 - py) / height_px * (ylim[1] - ylim[0]) + ylim[0]
                    return dx, dy
                
                data_points = [px_to_data(px, py) for px, py in self.points]
                data_x = [p[0] for p in data_points]
                data_y = [p[1] for p in data_points]
                
                self.ax.scatter(data_x, data_y, c='red', s=100, zorder=5)
            
            self.lbl_coefficients.config(text="k = -, b = -")
            self.lbl_angle.config(text="Угол: -°")
        
        self.canvas.draw_idle()
    
    def draw_angle_arc(self, p1, p2, angle_deg):
        """Рисование дуги угла"""
        import matplotlib.patches as patches
        
        # Длина дуги в условных единицах
        arc_radius = min(abs(p2[0] - p1[0]), abs(p2[1] - p1[1])) * 0.3
        if arc_radius < 0.1:
            arc_radius = 0.5
        
        # Создаем дугу
        # Угол в радианах
        angle_rad = np.radians(angle_deg)
        
        # Дуга от 0 до angle_deg
        arc = patches.Arc(
            (p1[0], p1[1]),
            2 * arc_radius,
            2 * arc_radius,
            angle=0,
            theta1=0,
            theta2=angle_deg,
            color='green',
            linewidth=2,
            label=f'Угол: {angle_deg:.1f}°'
        )
        
        self.ax.add_patch(arc)
        
        # Добавляем текст с значением угла рядом с дугой
        mid_angle = angle_rad / 2
        text_x = p1[0] + arc_radius * 1.2 * np.cos(mid_angle)
        text_y = p1[1] + arc_radius * 1.2 * np.sin(mid_angle)
        
        self.ax.text(text_x, text_y, f'{angle_deg:.1f}°', 
                    color='green', fontsize=10, fontweight='bold')

def main():
    root = tk.Tk()
    root.geometry("1000x800")
    
    app = PixelLinearPlotter(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
