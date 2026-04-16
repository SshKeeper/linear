import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, TextBox
import matplotlib.ticker as ticker

# Настройка бэкенда
import matplotlib
try:
    matplotlib.use('Qt5Agg')
except ImportError:
    try:
        matplotlib.use('TkAgg')
    except ImportError:
        matplotlib.use('Agg')

class LinearFunctionPlotter:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(left=0.1, bottom=0.35, right=0.95, top=0.95)

        # Исходные данные
        self.k = 1.0
        self.b = 0.0
        self.x_point_val = 2.0
        
        # Параметры сетки и масштаба
        self.step_x = 0.5
        self.step_y = 2.0
        self.x_lim = 10.0
        self.y_lim = 10.0

        # Генерация данных для линии
        self.x_data = np.linspace(-self.x_lim, self.x_lim, 400)
        self.line, = self.ax.plot(self.x_data, self.k * self.x_data + self.b, 'b-', linewidth=2, label=f'y = {self.k}x + {self.b}')

        # Точка на графике
        self.point_scatter = self.ax.scatter([self.x_point_val], [self.k * self.x_point_val + self.b], c='red', s=50, zorder=5)

        # Объекты для отрисовки угла (изначально пустые)
        self.angle_arc = None
        self.angle_text = None
        self.horiz_line = None
        self.diag_line = None

        # Настройки осей
        self.ax.set_title("Линейная функция: Угол зависит от масштаба (пикселей)")
        self.ax.grid(True, which='both', linestyle='--', alpha=0.7)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.legend(loc='upper left')
        self.ax.set_aspect('auto')
        
        self.update_limits_and_grid()

        # --- Создание виджетов управления ---
        ax_color = 'lightgoldenrodyellow'
        rect_slider_k = plt.axes([0.125, 0.25, 0.75, 0.03], facecolor=ax_color)
        rect_slider_b = plt.axes([0.125, 0.20, 0.75, 0.03], facecolor=ax_color)
        rect_slider_x = plt.axes([0.125, 0.15, 0.75, 0.03], facecolor=ax_color)
        
        self.slider_k = Slider(rect_slider_k, 'K (наклон)', -10.0, 10.0, valinit=self.k)
        self.slider_b = Slider(rect_slider_b, 'B (сдвиг)', -10.0, 10.0, valinit=self.b)
        self.slider_x = Slider(rect_slider_x, 'Точка X', -self.x_lim, self.x_lim, valinit=self.x_point_val)

        # Текстовые поля для сетки и масштаба
        rect_step_x = plt.axes([0.125, 0.10, 0.2, 0.03], facecolor=ax_color)
        rect_step_y = plt.axes([0.35, 0.10, 0.2, 0.03], facecolor=ax_color)
        rect_scale_x = plt.axes([0.125, 0.05, 0.2, 0.03], facecolor=ax_color)
        rect_scale_y = plt.axes([0.35, 0.05, 0.2, 0.03], facecolor=ax_color)

        self.box_step_x = TextBox(rect_step_x, 'Step X', initial=str(self.step_x))
        self.box_step_y = TextBox(rect_step_y, 'Step Y', initial=str(self.step_y))
        self.box_scale_x = TextBox(rect_scale_x, 'X Limit (+-)', initial=str(self.x_lim))
        self.box_scale_y = TextBox(rect_scale_y, 'Y Limit (+-)', initial=str(self.y_lim))

        # Привязка событий
        self.slider_k.on_changed(self.update_all)
        self.slider_b.on_changed(self.update_all)
        self.slider_x.on_changed(self.update_point_only)
        
        self.box_step_x.on_submit(self.update_limits_and_grid)
        self.box_step_y.on_submit(self.update_limits_and_grid)
        self.box_scale_x.on_submit(self.update_limits_and_grid)
        self.box_scale_y.on_submit(self.update_limits_and_grid)
        
        # Событие перерисовки (ресайз окна, пан, зум)
        self.cid_draw = self.fig.canvas.mpl_connect('draw_event', self.on_draw_event)

        self.update_all(None)

    def update_limits_and_grid(self, text=None):
        """Обновляет пределы осей и шаг сетки из текстовых полей."""
        try:
            self.step_x = float(self.box_step_x.text)
            self.step_y = float(self.box_step_y.text)
            self.x_lim = float(self.box_scale_x.text)
            self.y_lim = float(self.box_scale_y.text)
            
            self.ax.set_xlim(-self.x_lim, self.x_lim)
            self.ax.set_ylim(-self.y_lim, self.y_lim)
            
            self.ax.xaxis.set_major_locator(ticker.MultipleLocator(self.step_x))
            self.ax.yaxis.set_major_locator(ticker.MultipleLocator(self.step_y))
            
            self.slider_x.valmin = -self.x_lim
            self.slider_x.valmax = self.x_lim
            
            self.update_all(None)
        except ValueError:
            pass

    def on_draw_event(self, event):
        """Событие отрисовки. Вызывается при изменении вида (зум, пан, ресайз)."""
        self.draw_angle_visual()
        
    def update_all(self, val):
        """Полное обновление графика."""
        self.k = self.slider_k.val
        self.b = self.slider_b.val
        self.x_point_val = self.slider_x.val
        
        y_func = self.k * self.x_data + self.b
        self.line.set_ydata(y_func)
        self.line.set_label(f'y = {self.k:.2f}x + {self.b:.2f}')
        self.ax.legend(loc='upper left')
        
        self.update_point_only(val)

    def update_point_only(self, val):
        """Обновление только позиции точки и угла."""
        if val is not None:
            self.x_point_val = self.slider_x.val
            
        y_point = self.k * self.x_point_val + self.b
        self.point_scatter.set_offsets([[self.x_point_val, y_point]])
        
        self.draw_angle_visual()
        self.fig.canvas.draw_idle()

    def draw_angle_visual(self):
        """
        Рисует угол на основе экранных координат (пикселей).
        Сначала удаляет старые элементы угла.
        """
        # 1. Очистка старых элементов
        if self.angle_arc:
            self.angle_arc.remove()
            self.angle_arc = None
        if self.angle_text:
            self.angle_text.remove()
            self.angle_text = None
        if self.horiz_line:
            self.horiz_line.remove()
            self.horiz_line = None
        if self.diag_line:
            self.diag_line.remove()
            self.diag_line = None

        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        x0 = self.x_point_val
        y0 = self.k * x0 + self.b
        
        if not (xlim[0] <= x0 <= xlim[1] and ylim[0] <= y0 <= ylim[1]):
            return

        # 2. Преобразование в пиксели для расчета реального визуального угла
        dx_data = (xlim[1] - xlim[0]) * 0.1
        x1_data = x0 + dx_data
        y1_data = self.k * x1_data + self.b
        
        trans = self.ax.transData.transform
        pt0_px = trans([x0, y0])
        pt1_px = trans([x1_data, y1_data])
        
        vec_x = pt1_px[0] - pt0_px[0]
        vec_y = pt1_px[1] - pt0_px[1]
        
        if abs(vec_x) < 1e-6:
            angle_rad = np.pi / 2 if vec_y > 0 else -np.pi / 2
        else:
            angle_rad = np.arctan2(vec_y, vec_x)
            
        if angle_rad < 0:
            angle_rad += 2 * np.pi
            
        angle_deg = np.degrees(angle_rad)
        
        # 3. Расчет размеров для отрисовки дуги (чтобы она была круглой на экране)
        bbox = self.ax.get_window_extent()
        width_px = bbox.width
        height_px = bbox.height
        
        units_per_px_x = (xlim[1] - xlim[0]) / width_px
        units_per_px_y = (ylim[1] - ylim[0]) / height_px
        
        radius_px = 50.0
        radius_x_data = radius_px * units_per_px_x
        radius_y_data = radius_px * units_per_px_y
        
        # 4. Отрисовка дуги
        t = np.linspace(0, angle_rad, 100)
        arc_x = x0 + radius_x_data * np.cos(t)
        arc_y = y0 + radius_y_data * np.sin(t)
        
        self.angle_arc, = self.ax.plot(arc_x, arc_y, color='green', linewidth=2)
        
        # Горизонтальный луч
        h_x = [x0, x0 + radius_x_data]
        h_y = [y0, y0]
        self.horiz_line, = self.ax.plot(h_x, h_y, 'r--', alpha=0.6)
        
        # Диагональный луч
        end_x = x0 + radius_x_data * np.cos(angle_rad)
        end_y = y0 + radius_y_data * np.sin(angle_rad)
        d_x = [x0, end_x]
        d_y = [y0, end_y]
        self.diag_line, = self.ax.plot(d_x, d_y, 'g--', alpha=0.6)
        
        # Текст с градусами
        mid_angle = angle_rad / 2
        text_r_px = radius_px * 1.2
        text_r_x = text_r_px * units_per_px_x
        text_r_y = text_r_px * units_per_px_y
        
        tx = x0 + text_r_x * np.cos(mid_angle)
        ty = y0 + text_r_y * np.sin(mid_angle)
        
        display_angle = angle_deg
        if display_angle > 180:
            display_angle = 360 - display_angle
            
        self.angle_text = self.ax.text(tx, ty, f'{display_angle:.1f}°', color='blue', fontsize=12, fontweight='bold',
                                       ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

if __name__ == "__main__":
    plotter = LinearFunctionPlotter()
    plt.show()
