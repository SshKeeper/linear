import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, FloatText, BoundedFloatText
import ipywidgets as widgets

def plot_linear_function_with_grid_control():
    """
    Интерактивный график линейной функции с настройкой:
    - Коэффициентов k и b
    - Масштаба осей (xlim, ylim)
    - Шага сетки (deltax, deltay)
    - Отображения угла наклона в выбранной точке
    """
    
    # Создаем элементы управления
    k_slider = FloatSlider(value=1.0, min=-10.0, max=10.0, step=0.1, description='k (наклон):', continuous_update=False)
    b_slider = FloatSlider(value=0.0, min=-10.0, max=10.0, step=0.1, description='b (сдвиг):', continuous_update=False)
    
    x_point_slider = FloatSlider(value=1.0, min=-10.0, max=10.0, step=0.1, description='Точка X:', continuous_update=False)
    
    # Масштабирование осей
    x_min_input = FloatText(value=-10.0, description='X min:', step=1.0)
    x_max_input = FloatText(value=10.0, description='X max:', step=1.0)
    y_min_input = FloatText(value=-10.0, description='Y min:', step=1.0)
    y_max_input = FloatText(value=10.0, description='Y max:', step=1.0)
    
    # Шаг сетки (новое требование)
    delta_x_input = BoundedFloatText(value=1.0, min=0.1, max=10.0, step=0.1, description='Step X:')
    delta_y_input = BoundedFloatText(value=1.0, min=0.1, max=10.0, step=0.1, description='Step Y:')

    def update_plot(k, b, x_point, x_min, x_max, y_min, y_max, dx, dy):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Проверка корректности диапазонов
        if x_min >= x_max:
            x_max = x_min + 1
        if y_min >= y_max:
            y_max = y_min + 1
            
        # Данные для графика
        x = np.linspace(x_min, x_max, 1000)
        y = k * x + b
        
        ax.plot(x, y, label=f'y = {k}x + {b}', color='blue', linewidth=2)
        
        # Настройка сетки с индивидуальными шагами
        ax.set_xticks(np.arange(np.ceil(x_min/dx)*dx, x_max+dx, dx))
        ax.set_yticks(np.arange(np.ceil(y_min/dy)*dy, y_max+dy, dy))
        ax.grid(True, which='both', linestyle='--', alpha=0.7)
        
        # Настройка пределов осей
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        
        # Оси координат
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        
        # Выделенная точка
        y_point = k * x_point + b
        if x_min <= x_point <= x_max and y_min <= y_point <= y_max:
            ax.plot(x_point, y_point, 'ro', markersize=8, label=f'Точка ({x_point}, {y_point:.2f})')
            
            # Отрисовка угла
            # Визуализируем треугольник для угла
            dx_vis = 1.0 if x_max - x_min > 2 else (x_max - x_min) / 4
            x2 = x_point + dx_vis
            y2 = k * x2 + b
            
            # Горизонтальная проекция
            ax.plot([x_point, x2], [y_point, y_point], 'g--', linewidth=1.5, label='Проекция OX')
            # Линия графика от точки
            ax.plot([x_point, x2], [y_point, y2], 'g-', linewidth=1.5)
            
            # Вычисление угла в градусах
            angle_rad = np.arctan(abs(k))
            angle_deg = np.degrees(angle_rad)
            
            # Текст с углом
            label_pos_x = x_point + dx_vis / 2
            label_pos_y = y_point + (abs(k) * dx_vis) / 4
            ax.text(label_pos_x, label_pos_y, f'{angle_deg:.1f}°', fontsize=12, color='green', 
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        ax.set_title(f'График линейной функции (Шаг сетки: X={dx}, Y={dy})')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend(loc='best')
        ax.set_aspect('auto') # Важно для независимого масштабирования
        
        plt.show()

    # Компоновка виджетов
    grid_controls = widgets.HBox([delta_x_input, delta_y_input])
    axis_controls = widgets.HBox([x_min_input, x_max_input, y_min_input, y_max_input])
    
    ui = widgets.VBox([
        k_slider,
        b_slider,
        x_point_slider,
        widgets.HTML("<b>Настройки сетки:</b>"),
        grid_controls,
        widgets.HTML("<b>Масштаб осей:</b>"),
        axis_controls
    ])
    
    out = widgets.interactive_output(update_plot, {
        'k': k_slider,
        'b': b_slider,
        'x_point': x_point_slider,
        'x_min': x_min_input,
        'x_max': x_max_input,
        'y_min': y_min_input,
        'y_max': y_max_input,
        'dx': delta_x_input,
        'dy': delta_y_input
    })
    
    display(ui, out)

# Запуск функции (если вы в Jupyter)
# plot_linear_function_with_grid_control()
print("Код готов к запуску в Jupyter Notebook. Вызовите функцию plot_linear_function_with_grid_control()")
