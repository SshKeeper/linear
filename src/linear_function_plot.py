"""
Интерактивный график линейной функции с возможностью:
- Редактирования коэффициентов k и b
- Отображения угла между осью OX и графиком
- Независимого масштабирования осей OX и OY
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ipywidgets as widgets
from IPython.display import display, clear_output


def create_linear_function_plot(k=1, b=0, x_min=-10, x_max=10, y_min=-10, y_max=10, 
                                 show_angle=True, angle_point_x=0):
    """
    Создает интерактивный график линейной функции y = k*x + b
    
    Параметры:
    -----------
    k : float
        Коэффициент наклона (угловой коэффициент)
    b : float
        Свободный член (смещение по оси Y)
    x_min : float
        Минимальное значение оси X
    x_max : float
        Максимальное значение оси X
    y_min : float
        Минимальное значение оси Y
    y_max : float
        Максимальное значение оси Y
    show_angle : bool
        Показывать угол между осью OX и графиком
    angle_point_x : float
        X-координата точки, где показывается угол
    """
    
    # Создаем массив значений X
    x = np.linspace(x_min, x_max, 1000)
    y = k * x + b
    
    # Вычисляем угол наклона в градусах
    angle_degrees = np.degrees(np.arctan(k))
    
    # Вычисляем Y для точки, где показываем угол
    angle_point_y = k * angle_point_x + b
    
    # Создаем фигуру
    fig = make_subplots(rows=1, cols=1)
    
    # Добавляем основную линию функции
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name=f'y = {k:.2f}x + {b:.2f}',
        line=dict(color='blue', width=3)
    ))
    
    # Добавляем оси координат
    # Ось X
    fig.add_trace(go.Scatter(
        x=[x_min, x_max], y=[0, 0],
        mode='lines',
        name='Ось X',
        line=dict(color='black', width=2),
        hoverinfo='skip'
    ))
    
    # Ось Y
    fig.add_trace(go.Scatter(
        x=[0, 0], y=[y_min, y_max],
        mode='lines',
        name='Ось Y',
        line=dict(color='black', width=2),
        hoverinfo='skip'
    ))
    
    # Добавляем точку, где измеряется угол
    if show_angle:
        fig.add_trace(go.Scatter(
            x=[angle_point_x], y=[angle_point_y],
            mode='markers',
            name='Точка измерения угла',
            marker=dict(color='red', size=10),
            hovertext=f'({angle_point_x:.2f}, {angle_point_y:.2f})'
        ))
        
        # Рисуем горизонтальную линию от точки (проекция оси OX)
        horizontal_x = [angle_point_x, angle_point_x + 2]
        horizontal_y = [angle_point_y, angle_point_y]
        fig.add_trace(go.Scatter(
            x=horizontal_x, y=horizontal_y,
            mode='lines',
            name='Проекция OX',
            line=dict(color='green', width=2, dash='dash'),
            hoverinfo='skip'
        ))
        
        # Рисуем дугу для отображения угла
        arc_radius = 1.5
        if k >= 0:
            theta = np.linspace(0, np.arctan(k), 100)
        else:
            theta = np.linspace(np.arctan(k), 0, 100)
        
        arc_x = angle_point_x + arc_radius * np.cos(theta)
        arc_y = angle_point_y + arc_radius * np.sin(theta)
        
        fig.add_trace(go.Scatter(
            x=arc_x, y=arc_y,
            mode='lines',
            name='Угол',
            line=dict(color='orange', width=3),
            hoverinfo='skip'
        ))
        
        # Добавляем подпись угла
        mid_angle = theta[len(theta)//2]
        label_x = angle_point_x + (arc_radius + 0.3) * np.cos(mid_angle)
        label_y = angle_point_y + (arc_radius + 0.3) * np.sin(mid_angle)
        
        fig.add_annotation(
            x=label_x, y=label_y,
            text=f'{angle_degrees:.1f}°',
            showarrow=False,
            font=dict(color='orange', size=14, weight='bold'),
            bgcolor='white',
            bordercolor='orange',
            borderwidth=1,
            borderpad=4
        )
    
    # Настраиваем макет
    fig.update_layout(
        title=f'Линейная функция: y = {k:.2f}x + {b:.2f}<br>Угол наклона: {angle_degrees:.2f}°',
        xaxis=dict(
            title='Ось X',
            range=[x_min, x_max],
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2,
            gridcolor='lightgray',
            showgrid=True
        ),
        yaxis=dict(
            title='Ось Y',
            range=[y_min, y_max],
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2,
            gridcolor='lightgray',
            showgrid=True,
            scaleanchor=None  # Позволяет независимое масштабирование
        ),
        height=600,
        width=800,
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Добавляем информацию о точке пересечения с осями
    x_intercept = -b / k if k != 0 else None
    y_intercept = b
    
    info_text = f"Точка пересечения с OY: (0, {y_intercept:.2f})"
    if x_intercept is not None:
        info_text += f"<br>Точка пересечения с OX: ({x_intercept:.2f}, 0)"
    
    fig.add_annotation(
        x=x_min + (x_max - x_min) * 0.02,
        y=y_max - (y_max - y_min) * 0.1,
        text=info_text,
        showarrow=False,
        font=dict(size=12),
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='blue',
        borderwidth=1,
        borderpad=4,
        align='left'
    )
    
    return fig


def create_interactive_widget():
    """
    Создает интерактивный виджет для управления параметрами линейной функции
    """
    
    # Создаем виджеты для ввода параметров
    k_slider = widgets.FloatSlider(
        value=1.0,
        min=-10.0,
        max=10.0,
        step=0.1,
        description='k (наклон):',
        style={'description_width': '100px'},
        continuous_update=True
    )
    
    b_slider = widgets.FloatSlider(
        value=0.0,
        min=-20.0,
        max=20.0,
        step=0.5,
        description='b (сдвиг):',
        style={'description_width': '100px'},
        continuous_update=True
    )
    
    # Виджеты для масштабирования осей
    x_min_widget = widgets.FloatText(
        value=-10.0,
        description='X мин:',
        style={'description_width': '70px'}
    )
    
    x_max_widget = widgets.FloatText(
        value=10.0,
        description='X макс:',
        style={'description_width': '70px'}
    )
    
    y_min_widget = widgets.FloatText(
        value=-10.0,
        description='Y мин:',
        style={'description_width': '70px'}
    )
    
    y_max_widget = widgets.FloatText(
        value=10.0,
        description='Y макс:',
        style={'description_width': '70px'}
    )
    
    # Виджет для позиции точки измерения угла
    angle_point_widget = widgets.FloatSlider(
        value=0.0,
        min=-10.0,
        max=10.0,
        step=0.5,
        description='Точка угла X:',
        style={'description_width': '100px'},
        continuous_update=True
    )
    
    # Чекбокс для показа угла
    show_angle_checkbox = widgets.Checkbox(
        value=True,
        description='Показать угол',
        indent=False
    )
    
    # Вывод для графика
    output = widgets.Output()
    
    def update_plot(change=None):
        """Обновляет график при изменении параметров"""
        with output:
            clear_output(wait=True)
            
            try:
                fig = create_linear_function_plot(
                    k=k_slider.value,
                    b=b_slider.value,
                    x_min=x_min_widget.value,
                    x_max=x_max_widget.value,
                    y_min=y_min_widget.value,
                    y_max=y_max_widget.value,
                    show_angle=show_angle_checkbox.value,
                    angle_point_x=angle_point_widget.value
                )
                fig.show()
            except Exception as e:
                print(f"Ошибка при построении графика: {e}")
    
    # Подключаем обработчики событий
    k_slider.observe(update_plot, names='value')
    b_slider.observe(update_plot, names='value')
    x_min_widget.observe(update_plot, names='value')
    x_max_widget.observe(update_plot, names='value')
    y_min_widget.observe(update_plot, names='value')
    y_max_widget.observe(update_plot, names='value')
    angle_point_widget.observe(update_plot, names='value')
    show_angle_checkbox.observe(update_plot, names='value')
    
    # Создаем компоновку виджетов
    controls = widgets.VBox([
        widgets.HBox([k_slider, b_slider]),
        widgets.HBox([angle_point_widget, show_angle_checkbox]),
        widgets.HTML("<b>Масштабирование осей:</b>"),
        widgets.HBox([x_min_widget, x_max_widget]),
        widgets.HBox([y_min_widget, y_max_widget]),
    ])
    
    display(widgets.VBox([controls, output]))
    
    # Первоначальное построение
    update_plot()
    
    return {
        'k_slider': k_slider,
        'b_slider': b_slider,
        'x_min': x_min_widget,
        'x_max': x_max_widget,
        'y_min': y_min_widget,
        'y_max': y_max_widget,
        'angle_point': angle_point_widget,
        'show_angle': show_angle_checkbox,
        'output': output
    }


# Пример использования без виджетов (для скриптов)
if __name__ == "__main__":
    # Статический пример
    fig = create_linear_function_plot(k=2, b=3, x_min=-5, x_max=5, y_min=-5, y_max=15)
    fig.write_html("linear_function.html")
    print("График сохранен в файл: linear_function.html")
    
    # Для запуска интерактивного виджета в Jupyter Notebook раскомментируйте:
    # create_interactive_widget()
