import tempfile
import pandas as pd 
import plotly.express as px
from PyQt6.QtCore import pyqtSlot, QObject, QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QFileDialog, \
    QTabWidget, QListWidget, QHBoxLayout, QCheckBox, QLabel, QComboBox, QLineEdit, QMessageBox 
from PyQt6.QtCore import Qt
import plotly.graph_objs as go

from abstraction import EscData
from data_process import PostProcess
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QSizePolicy
)
from scipy.signal import savgol_filter




class ComparisonView(QDialog):
    def __init__(self,e0=None,e1=None,e2=None,e3=None,post_process=False):
        super().__init__()
        
        
        h_layout = QHBoxLayout()
        

        self.setWindowIcon(QIcon('data/logo.ico'))
        self.df_esc0=None
        self.df_esc1=None
        self.df_esc2=None
        self.df_esc3=None
        self.df_rpm0=None
        self.df_rpm1=None
        self.df_rpm2=None
        self.df_rpm3=None
        self.esc0= None
        self.esc1= None
        self.esc2= None
        self.esc3= None

                

        from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QSizePolicy

        self.expression_group = QVBoxLayout()
        self.expression_group.setSpacing(10)

        # 🔹 1. Başlık
        self.expression_label = QLabel("Enter Arithmetic Expression:")
        self.expression_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.expression_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.expression_group.addWidget(self.expression_label)

        # 🔹 2. Hint
        self.expression_hint = QLabel("Supported: Addition, Subtraction, Multiplication, Division, Exponentiation, Parentheses")
        self.expression_hint.setStyleSheet("font-weight: bold; color: gray; font-size: 12px;")
        self.expression_hint.setWordWrap(True)  # Metin taşarsa satır atlaması sağlanır
        self.expression_hint.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.expression_group.addWidget(self.expression_hint)

        # 🔹 3. Kullanıcı girişi
        self.expression_input = QLineEdit()
        self.expression_input.setPlaceholderText("Use ESC 0 as E0, ... , ESC3 as E3")
        self.expression_input.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.expression_group.addWidget(self.expression_input)

        # 🔹 4. Apply butonu
        self.apply_expression_button = QPushButton("Apply Expression")
        self.apply_expression_button.setFixedHeight(30)
        self.apply_expression_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.apply_expression_button.clicked.connect(self.apply_expression_clicked)
        self.expression_group.addWidget(self.apply_expression_button)

        # 🔹 Layout'u Widget'a bağla
        self.expression_group_widget = QWidget()
        self.expression_group_widget.setLayout(self.expression_group)
        self.expression_group_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.expression_group_widget.setMinimumWidth(280)  # Genişliği sabitlemek için isteğe bağlı
        self.expression_group_widget.setVisible(False)

        self.toggle_expression_button = QPushButton("Arithmetic Expression")
        self.toggle_expression_button.setCheckable(True)
        self.toggle_expression_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid #888;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        self.toggle_expression_button.clicked.connect(self.toggle_expression_group)

        v_expression_layout = QVBoxLayout()
        v_expression_layout.addWidget(self.toggle_expression_button)
        v_expression_layout.addWidget(self.expression_group_widget)

        v_expression_widget = QWidget()
        v_expression_widget.setLayout(v_expression_layout)

        h_layout.addWidget(v_expression_widget)
        h_layout.setStretchFactor(v_expression_widget, 1)



        h_layout.addWidget(self.expression_group_widget)
        h_layout.setStretchFactor(self.expression_group_widget, 1)


        if not post_process:
            if e0:
                self.esc0 : EscData = e0
            if e1:
                self.esc1 : EscData = e1
            if e2:
                self.esc2 : EscData = e2
            if e3:
                self.esc3 : EscData = e3

            self.setWindowTitle("Comparison View")
            self.setGeometry(100, 100, 1100, 650)
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
            self.list_widget = QListWidget()
            self.list_widget.addItems(['Voltage', 'Current', 'Temperature', 'eRPM','RPM','Throttle Duty',
                                   'Motor Duty', 'Phase Current', 'Power', 'Status 1', 'Status 2'])
            
        else:
            if e0:
                self.esc0 : PostProcess = e0
            if e1:
                self.esc1 : PostProcess = e1
            if e2:
                self.esc2 : PostProcess = e2
            if e3:
                self.esc3 : PostProcess = e3

            self.setWindowTitle("Comparison View - Post Processed")
            self.setGeometry(150, 150, 800, 600)
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
            self.list_widget = QListWidget()
            self.list_widget.addItems(['Voltage', 'Current', 'Temperature', 'RPM', 'Throttle Duty',
                                   'Motor Duty','Phase Current','Power'])


        self.smoothing_enabled = False

        # Liste ve toggle butonu birlikte tutacak layout
        self.smoothing_button = QPushButton("Smoothing Curve")
        self.smoothing_button.setCheckable(True)
        self.smoothing_button.setChecked(False)
        self.smoothing_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #999;
                font-weight: bold;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:checked {
                background-color: #a0c4ff;
            }
        """)
        self.smoothing_button.clicked.connect(self.on_smoothing_toggle_clicked)

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.list_widget)
        list_layout.addWidget(self.smoothing_button)

        list_widget_container = QWidget()
        list_widget_container.setLayout(list_layout)
        h_layout.addWidget(list_widget_container)
        h_layout.setStretchFactor(list_widget_container, 1)





        self.selected_value = 'Voltage'
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.browser = QWebEngineView()
        
        #h_layout.addWidget(self.list_widget)
        h_layout.addWidget(self.browser)
        #h_layout.setStretchFactor(self.list_widget, 1)
        h_layout.setStretchFactor(self.browser, 5)
        self.setLayout(h_layout)
        print("here")
        if not post_process:
            self.load_data()
        else:
            self.load_data_post_process()

        self.update_plot()

    def toggle_expression_group(self):
        visible = self.toggle_expression_button.isChecked()
        self.expression_group_widget.setVisible(visible)
    

    def apply_expression_clicked(self):
        expression = self.expression_input.text().strip()
        if not expression:
            QMessageBox.warning(self, "Input Error", "Expression cannot be empty.")
            return
        
        # Vektörel ifade kontrolü
        import re
        vector_pattern = r"^\((E0|E1|E2|E3)(,(E0|E1|E2|E3))*\)\s*[\+\-\*/\*{2}]{1,2}\s*\d+(\.\d+)?$"
        is_vector_expr = bool(re.match(vector_pattern, expression.replace(" ", "")))

        
        


        esc_dataframes = {
            'E0': self.df_esc0,
            'E1': self.df_esc1,
            'E2': self.df_esc2,
            'E3': self.df_esc3
        }

        selected_attr = self.selected_value  # Örn. 'Voltage', 'RPM'
        variables = {}
        used_keys = []

        for key, df in esc_dataframes.items():
            if df is not None:
                if selected_attr not in df.columns:
                    QMessageBox.warning(self, "Data Missing", f"{selected_attr} not found in {key}.")
                    return
                variables[key] = pd.Series(df[selected_attr].values)
                used_keys.append(key)
        
        
        if is_vector_expr:
            # (E1,E2,E3) / 3 → ['E1','E2','E3'], op → /3
            vector_match = re.match(r"^\((E[0-3](?:,E[0-3])*)\)\s*([\+\-\*/]{1,2})\s*(\d+(?:\.\d+)?)$", expression.replace(" ", ""))
            if not vector_match:
                QMessageBox.warning(self, "Parse Error", "Vector expression couldn't be parsed.")
                return

            esc_keys = vector_match.group(1).split(",")
            operator = vector_match.group(2)
            value = vector_match.group(3)

            result_dict = {}
            for key in esc_keys:
                if key in variables:
                    expr = f"{key} {operator} {value}"
                    try:
                        result = eval(expr, {}, variables)
                        result_dict[expr] = result
                    except Exception as e:
                        QMessageBox.critical(self, "Expression Error", f"{expr} failed:\n{str(e)}")
                        return
            self.show_expression_result_plot(result_dict, expression)
        else:
            try:
                result = eval(expression, {}, variables)
                self.show_expression_result_plot({expression: result}, expression)
            except Exception as e:
                QMessageBox.critical(self, "Expression Error", f"Failed to evaluate expression:\n{str(e)}")
                return


        


    



    def show_expression_result_plot(self, result_dict, expression):
            fig = go.Figure()
            self.last_expression = expression

            # 🔹 1. Aritmetik sonuçlar
            vector_colors = ['#171717', '#444444', '#526D82', '#A27B5C']
            # X-axis olarak uygun Time verisini bul (örnek: E1 varsa onun Time verisi)
            time_x = None
            for esc_key in ['E0', 'E1', 'E2', 'E3']:
                if esc_key in expression and getattr(self, f'df_esc{esc_key[-1]}') is not None:
                    time_x = getattr(self, f'df_esc{esc_key[-1]}')['Time']
                    break

            if time_x is None:
                time_x = list(range(len(next(iter(result_dict.values())))))  # fallback to index

            for idx, (label, data) in enumerate(result_dict.items()):
                color = vector_colors[idx % len(vector_colors)]
                fig.add_trace(go.Scatter(
                    x=time_x,
                    y=data,
                    mode='lines',
                    name=label,
                    line=dict(color=color),
                    hoverinfo='x+y+name'
                ))



            # 🔹 2. ESC verileri (kıyas için)
            esc_dataframes = {
                'E0': self.df_esc0,
                'E1': self.df_esc1,
                'E2': self.df_esc2,
                'E3': self.df_esc3
            }
            selected_attr = self.selected_value

            for key in ['E0', 'E1', 'E2', 'E3']:
                if esc_dataframes[key] is not None:
                    y_data = esc_dataframes[key][selected_attr]
                    if self.smoothing_enabled and len(y_data) >= 201:
                        try:
                            y_data = savgol_filter(y_data, window_length=201, polyorder=2)
                        except Exception as e:
                            print(f"Smoothing failed on ESC {key}: {e}")
                    fig.add_trace(go.Scatter(
                        x=esc_dataframes[key]['Time'],
                        y=y_data,
                        mode='lines',
                        name=key,
                        line=dict(),
                        hoverinfo='x+y+name'
                    ))



            fig.update_layout(
                title=f"Result of Expression: {expression}",
                xaxis_title="Index",
                yaxis_title=selected_attr
            )

            html = fig.to_html(include_plotlyjs='cdn')

            # Yeni QDialog oluştur
            dialog = QDialog(self)
            dialog.setWindowTitle("Expression Result Plot")
            dialog.resize(1000, 600)
            dialog.setWindowFlags(
                Qt.WindowType.Window |
                Qt.WindowType.CustomizeWindowHint |
                Qt.WindowType.WindowMinimizeButtonHint |
                Qt.WindowType.WindowMaximizeButtonHint |
                Qt.WindowType.WindowCloseButtonHint
            )

            layout = QVBoxLayout(dialog)

            attr_selector = QComboBox()
            attr_selector.addItems([
                'Voltage', 'Current', 'Temperature', 'eRPM','RPM', 'Throttle Duty',
                'Motor Duty', 'Phase Current', 'Power', 'Status 1', 'Status 2'
            ])
            attr_selector.setCurrentText(self.selected_value)
            layout.addWidget(QLabel("Select Attribute to Apply:"))
            layout.addWidget(attr_selector)

            new_expression_input = QLineEdit()
            new_expression_input.setPlaceholderText("Enter New Arithmetic Expression Here:")
            new_expression_input.setClearButtonEnabled(True)
            layout.addWidget(new_expression_input)

            # Yeni HBox Layout
            button_row = QHBoxLayout()

            reapply_button = QPushButton("Apply New Expression")
            reapply_button.setFixedHeight(30)
            reapply_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            smooth_expr_button = QPushButton("Smoothing Curve")
            smooth_expr_button.setCheckable(True)
            smooth_expr_button.setFixedHeight(30)
            smooth_expr_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            smooth_expr_button.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #999;
                    font-weight: bold;
                    padding: 4px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:checked {
                    background-color: #a0c4ff;
                }
            """)

            button_row.addWidget(reapply_button)
            button_row.addWidget(smooth_expr_button)
            layout.addLayout(button_row)
            # Smoothing butonuna basıldığında yeniden çizim yap
            def toggle_smoothing_button():
                self.smoothing_enabled = smooth_expr_button.isChecked()
                self.smoothing_button.setChecked(self.smoothing_enabled)

                # Kutudaki ifade boşsa, son kullanılanı kullan
                current_expr = new_expression_input.text().strip()
                if not current_expr and hasattr(self, "last_expression"):
                    new_expression_input.setText(self.last_expression)
                    current_expr = self.last_expression

                reapply_expression()



            smooth_expr_button.clicked.connect(toggle_smoothing_button)
            
            


            view = QWebEngineView()
            view.setHtml(html)
            layout.addWidget(view)

            dialog.setLayout(layout)
            dialog.show()
            dialog.raise_()
            dialog.activateWindow()

            self.expression_plot_dialog = dialog
            # Ana sayfadaki smoothing aktifse bu buton da aktif başlasın
            smooth_expr_button.setChecked(self.smoothing_enabled)

            def reapply_expression():
                new_expr = new_expression_input.text().strip()
                if not new_expr:
                    QMessageBox.warning(dialog, "Input Error", "Expression cannot be empty.")
                    return

                esc_dataframes = {
                    'E0': self.df_esc0,
                    'E1': self.df_esc1,
                    'E2': self.df_esc2,
                    'E3': self.df_esc3
                }

                selected_attr = attr_selector.currentText()
                variables = {}
                for key, df in esc_dataframes.items():
                    if df is not None and selected_attr in df.columns:
                        variables[key] = pd.Series(df[selected_attr].values)

                import re
                vector_pattern = r"^\((E0|E1|E2|E3)(,(E0|E1|E2|E3))*\)\s*[\+\-\*/\*{2}]{1,2}\s*\d+(\.\d+)?$"
                is_vector_expr = bool(re.match(vector_pattern, new_expr.replace(" ", "")))

                result_dict = {}
                if is_vector_expr:
                    vector_match = re.match(r"^\((E[0-3](?:,E[0-3])*)\)\s*([\+\-\*/]{1,2})\s*(\d+(?:\.\d+)?)$", new_expr.replace(" ", ""))
                    if not vector_match:
                        QMessageBox.warning(dialog, "Parse Error", "Vector expression couldn't be parsed.")
                        return
                    esc_keys = vector_match.group(1).split(",")
                    operator = vector_match.group(2)
                    value = vector_match.group(3)
                    for key in esc_keys:
                        if key in variables:
                            expr = f"{key} {operator} {value}"
                            try:
                                result = eval(expr, {}, variables)
                                if self.smoothing_enabled and len(result) >= 201:
                                    result = savgol_filter(result, window_length=201, polyorder=2)
                                result_dict[expr] = result
                            except Exception as e:
                                QMessageBox.critical(dialog, "Expression Error", f"{expr} failed:\n{str(e)}")
                                return
                else:
                    try:
                        result = eval(new_expr, {}, variables)
                        if self.smoothing_enabled and len(result) >= 201:
                            result = savgol_filter(result, window_length=201, polyorder=2)
                        result_dict[new_expr] = result
                    except Exception as e:
                        QMessageBox.critical(dialog, "Expression Error", str(e))
                        return

                fig = go.Figure()
                vector_colors = ['#171717', '#444444', '#526D82', '#A27B5C']

                # ⏱ X-axis ayarla
                time_x = None
                for esc_key in ['E0', 'E1', 'E2', 'E3']:
                    if esc_key in new_expr and esc_dataframes[esc_key] is not None:
                        time_x = esc_dataframes[esc_key]['Time']
                        break
                if time_x is None:
                    time_x = list(range(len(next(iter(result_dict.values())))))

                for idx, (label, data) in enumerate(result_dict.items()):
                    color = vector_colors[idx % len(vector_colors)]
                    fig.add_trace(go.Scatter(x=time_x, y=data, mode='lines', name=label, line=dict(color=color)))

                for key in ['E0', 'E1', 'E2', 'E3']:
                    if esc_dataframes[key] is not None:
                        y_data = esc_dataframes[key][selected_attr]
                        if self.smoothing_enabled and len(y_data) >= 201:
                            try:
                                y_data = savgol_filter(y_data, window_length=201, polyorder=2)
                            except Exception as e:
                                print(f"Smoothing failed on ESC {key}: {e}")
                        fig.add_trace(go.Scatter(
                            x=esc_dataframes[key]['Time'],
                            y=y_data,
                            mode='lines',
                            name=key,
                            line=dict(),
                            hoverinfo='x+y+name'
                        ))



                fig.update_layout(title=f"Result of: {new_expr}", xaxis_title="Index", yaxis_title=selected_attr)
                view.setHtml(fig.to_html(include_plotlyjs='cdn'))


            def update_plot_on_attribute_change():
                selected_attr = attr_selector.currentText()
                expression_to_apply = new_expression_input.text().strip()
                if not expression_to_apply:
                    if hasattr(self, "last_expression"):
                        expression_to_apply = self.last_expression

                esc_dataframes = {
                    'E0': self.df_esc0,
                    'E1': self.df_esc1,
                    'E2': self.df_esc2,
                    'E3': self.df_esc3
                }

                for key, df in esc_dataframes.items():
                    if df is not None:
                        print(f"{key} DataFrame sütunları:", df.columns.tolist())

                variables = {}
                for key, df in esc_dataframes.items():
                    if df is not None and selected_attr in df.columns:
                        variables[key] = pd.Series(df[selected_attr].values)

                result_dict = {}
                import re
                vector_pattern = r"^\((E0|E1|E2|E3)(,(E0|E1|E2|E3))*\)\s*[\+\-\*/\*{2}]{1,2}\s*\d+(\.\d+)?$"
                is_vector_expr = bool(re.match(vector_pattern, expression_to_apply.replace(" ", "")))

                if is_vector_expr:
                    vector_match = re.match(r"^\((E[0-3](?:,E[0-3])*)\)\s*([\+\-\*/]{1,2})\s*(\d+(?:\.\d+)?)$", expression_to_apply.replace(" ", ""))
                    if not vector_match:
                        QMessageBox.warning(dialog, "Parse Error", "Vector expression couldn't be parsed.")
                        return
                    esc_keys = vector_match.group(1).split(",")
                    operator = vector_match.group(2)
                    value = vector_match.group(3)
                    for key in esc_keys:
                        if key in variables:
                            expr = f"{key} {operator} {value}"
                            try:
                                result = eval(expr, {}, variables)
                                result_dict[expr] = result
                            except Exception as e:
                                QMessageBox.critical(dialog, "Expression Error", f"{expr} failed:\n{str(e)}")
                                return
                else:
                    try:
                        result = eval(expression_to_apply, {}, variables)
                        result_dict[expression_to_apply] = result
                    except Exception as e:
                        QMessageBox.critical(dialog, "Expression Error", str(e))
                        return

                # 🔹 X ekseni olarak Time belirle
                time_x = None
                for esc_key in ['E0', 'E1', 'E2', 'E3']:
                    if esc_key in expression_to_apply and esc_dataframes[esc_key] is not None:
                        time_x = esc_dataframes[esc_key]['Time']
                        break
                if time_x is None:
                    time_x = list(range(len(next(iter(result_dict.values())))))  # fallback to index

                new_fig = go.Figure()
                vector_colors = ['#171717', '#444444', '#526D82', '#A27B5C']
                for idx, (label, data) in enumerate(result_dict.items()):
                    color = vector_colors[idx % len(vector_colors)]
                    new_fig.add_trace(go.Scatter(x=time_x, y=data, mode='lines', name=label, line=dict(color=color)))
                
                for key in ['E0', 'E1', 'E2', 'E3']:
                    if esc_dataframes[key] is not None:
                        y_data = esc_dataframes[key][selected_attr]
                        if self.smoothing_enabled and len(y_data) >= 201:
                            try:
                                y_data = savgol_filter(y_data, window_length=201, polyorder=2)
                            except Exception as e:
                                print(f"Smoothing failed on ESC {key}: {e}")
                        new_fig.add_trace(go.Scatter(
                            x=esc_dataframes[key]['Time'],
                            y=y_data,
                            mode='lines',
                            name=key,
                            line=dict(),
                            hoverinfo='x+y+name'
                        ))



                new_fig.update_layout(title=f"Result of: {expression_to_apply}", xaxis_title="Time", yaxis_title=selected_attr)
                view.setHtml(new_fig.to_html(include_plotlyjs='cdn'))



            reapply_button.clicked.connect(reapply_expression)
            attr_selector.currentTextChanged.connect(update_plot_on_attribute_change)








        

    def load_data(self):
        if self.esc0:
            self.df_esc0 = pd.DataFrame({
                'Time': self.esc0.timestamp,
                'Voltage': self.esc0.voltage,
                'Current': self.esc0.current,
                'Temperature': self.esc0.temp,
                'eRPM': self.esc0.e_rpm,
                'RPM': self.esc0.rpm,
                'Throttle Duty': self.esc0.t_duty,
                'Motor Duty': self.esc0.m_duty,
                'Phase Current': self.esc0.phase_current,
                'Power': self.esc0.pwr,
                'Status 1': self.esc0.stat_1,
                'Status 2': self.esc0.stat_2,
                'Serial Number': self.esc0.serial_number
            })
            self.df_esc0['ESC'] = 'ESC0'
            print("ESC0 DataFrame created successfully")
            print(self.df_esc0.head())

        if self.esc1:
            self.df_esc1 = pd.DataFrame({
                'Time': self.esc1.timestamp,
                'Voltage': self.esc1.voltage,
                'Current': self.esc1.current,
                'Temperature': self.esc1.temp,
                'eRPM': self.esc1.e_rpm,
                'RPM': self.esc1.rpm,
                'Throttle Duty': self.esc1.t_duty,
                'Motor Duty': self.esc1.m_duty,
                'Phase Current': self.esc1.phase_current,
                'Power': self.esc1.pwr,
                'Status 1': self.esc1.stat_1,
                'Status 2': self.esc1.stat_2,
                'Serial Number': self.esc1.serial_number
            })
            self.df_esc1['ESC'] = 'ESC1'
            print("ESC1 DataFrame created successfully")
            print(self.df_esc1.head())

        if self.esc2:
            self.df_esc2 = pd.DataFrame({
                'Time': self.esc2.timestamp,
                'Voltage': self.esc2.voltage,
                'Current': self.esc2.current,
                'Temperature': self.esc2.temp,
                'eRPM': self.esc2.e_rpm,
                'RPM': self.esc2.rpm,
                'Throttle Duty': self.esc2.t_duty,
                'Motor Duty': self.esc2.m_duty,
                'Phase Current': self.esc2.phase_current,
                'Power': self.esc2.pwr,
                'Status 1': self.esc2.stat_1,
                'Status 2': self.esc2.stat_2,
                'Serial Number': self.esc2.serial_number
            })
            self.df_esc2['ESC'] = 'ESC2'
            print("ESC2 DataFrame created successfully")
            print(self.df_esc2.head())

        if self.esc3:
            self.df_esc3 = pd.DataFrame({
                'Time': self.esc3.timestamp,
                'Voltage': self.esc3.voltage,
                'Current': self.esc3.current,
                'Temperature': self.esc3.temp,
                'eRPM': self.esc3.e_rpm,
                'RPM': self.esc3.rpm,
                'Throttle Duty': self.esc3.t_duty,
                'Motor Duty': self.esc3.m_duty,
                'Phase Current': self.esc3.phase_current,
                'Power': self.esc3.pwr,
                'Status 1': self.esc3.stat_1,
                'Status 2': self.esc3.stat_2,
                'Serial Number': self.esc3.serial_number
            })
            self.df_esc3['ESC'] = 'ESC3'
            print("ESC3 DataFrame created successfully")
            print(self.df_esc3.head())

        self.df_combined = pd.concat([self.df_esc0, self.df_esc1, self.df_esc2, self.df_esc3])

    def load_data_post_process(self):
        try:
            if self.esc0:
                self.df_esc0 = pd.DataFrame({
                    'Time': self.esc0.timestamp,
                    'Voltage': self.esc0.voltage,
                    'Current': self.esc0.current,
                    'Temperature': self.esc0.temp,
                    'RPM': self.esc0.rpm,
                    'Throttle Duty': self.esc0.t_duty,
                    'Motor Duty': self.esc0.m_duty,
                    'Phase Current': self.esc0.phase_current,
                    'Power': self.esc0.pwr,
                    'Serial Number': self.esc0.serial_number
                })
                self.df_esc0['ESC'] = 'ESC0'
                print("ESC0 DataFrame created successfully")
                print(self.df_esc0.head())
                self.df_rpm0 = pd.DataFrame({
                    'Mean RPM': self.esc0.mean_rpm,
                    'Throttle': self.esc0.mean_thr,
                })
                self.df_rpm0['ESC'] = 'ESC0'

            if self.esc1:
                self.df_esc1 = pd.DataFrame({
                    'Time': self.esc1.timestamp,
                    'Voltage': self.esc1.voltage,
                    'Current': self.esc1.current,
                    'Temperature': self.esc1.temp,
                    'RPM': self.esc1.rpm,
                    'Throttle Duty': self.esc1.t_duty,
                    'Motor Duty': self.esc1.m_duty,
                    'Phase Current': self.esc1.phase_current,
                    'Power': self.esc1.pwr,
                    'Serial Number': self.esc1.serial_number
                })
                self.df_esc1['ESC'] = 'ESC1'
                print("ESC1 DataFrame created successfully")
                print(self.df_esc1.head())
                self.df_rpm1 = pd.DataFrame({
                    'Mean RPM': self.esc1.mean_rpm,
                    'Throttle': self.esc1.mean_thr,
                })
                self.df_rpm1['ESC'] = 'ESC1'

            if self.esc2:
                self.df_esc2 = pd.DataFrame({
                    'Time': self.esc2.timestamp,
                    'Voltage': self.esc2.voltage,
                    'Current': self.esc2.current,
                    'Temperature': self.esc2.temp,
                    'RPM': self.esc2.rpm,
                    'Throttle Duty': self.esc2.t_duty,
                    'Motor Duty': self.esc2.m_duty,
                    'Phase Current': self.esc2.phase_current,
                    'Power': self.esc2.pwr,
                    'Serial Number': self.esc2.serial_number
                })
                self.df_esc2['ESC'] = 'ESC2'
                print("ESC2 DataFrame created successfully")
                print(self.df_esc2.head())
                self.df_rpm2 = pd.DataFrame({
                    'Mean RPM': self.esc2.mean_rpm,
                    'Throttle': self.esc2.mean_thr,
                })
                self.df_rpm2['ESC'] = 'ESC2'

            if self.esc3:
                self.df_esc3 = pd.DataFrame({
                    'Time': self.esc3.timestamp,
                    'Voltage': self.esc3.voltage,
                    'Current': self.esc3.current,
                    'Temperature': self.esc3.temp,
                    'RPM': self.esc3.rpm,
                    'Throttle Duty': self.esc3.t_duty,
                    'Motor Duty': self.esc3.m_duty,
                    'Phase Current': self.esc3.phase_current,
                    'Power': self.esc3.pwr,
                    'Serial Number': self.esc3.serial_number
                })
                self.df_esc3['ESC'] = 'ESC3'
                print("ESC3 DataFrame created successfully")
                print(self.df_esc3.head())
                self.df_rpm3 = pd.DataFrame({
                    'Mean RPM': self.esc3.mean_rpm,
                    'Throttle': self.esc3.mean_thr,
                })
                self.df_rpm3['ESC'] = 'ESC3'

            self.df_combined = pd.concat([self.df_esc0, self.df_esc1, self.df_esc2, self.df_esc3])
            self.df_rpm_combined = pd.concat([self.df_rpm0,self.df_rpm1, self.df_rpm2, self.df_rpm3])
            print("Combined DataFrame created successfully")
            print(self.df_combined.head())

        except Exception as e:
            print(f"An error occurred: {e}")

    def on_item_clicked(self, item):
        self.selected_value = item.text()
        print(f"Selected value: {self.selected_value}")

        self.expression_group_widget.setVisible(False)

        if self.selected_value == 'RPM - Throttle':
            self.mean_plot()
        else:
            self.update_plot()

    def update_plot(self):
        df_to_plot = self.df_combined.copy()

        if self.smoothing_enabled and self.selected_value in df_to_plot.columns:
            try:
                df_to_plot[self.selected_value] = df_to_plot.groupby('ESC')[self.selected_value].transform(
                    lambda x: savgol_filter(x, window_length=201, polyorder=2) if len(x) >= 201 else x
                )
            except Exception as e:
                print(f"Smoothing failed: {e}")

        fig = px.line(df_to_plot, x='Time', y=self.selected_value, color='ESC',
                    labels={'Time': 'Time', self.selected_value: self.selected_value},
                    title='Comparison View')

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            fig.write_html(tmp_file.name)
            tmp_file_path = tmp_file.name

        self.browser.setUrl(QUrl.fromLocalFile(tmp_file_path))


    def mean_plot(self):
        df_sorted = self.df_rpm_combined.sort_values(by='Throttle').copy()

        if self.smoothing_checkbox.isChecked():
            try:
                df_sorted['Mean RPM'] = df_sorted.groupby('ESC')['Mean RPM'].transform(
                    lambda x: savgol_filter(x, window_length=201, polyorder=2) if len(x) >= 201 else x
                )
            except Exception as e:
                print(f"Smoothing failed in mean_plot: {e}")

        fig = px.line(df_sorted, x='Throttle', y='Mean RPM', color='ESC', markers=True,
                    title='Mean RPM vs Throttle',
                    labels={'Throttle': 'Throttle', 'Mean RPM': 'Mean RPM','ESC':'ESC'})
        fig.update_traces(marker=dict(size=8, symbol='circle'), line=dict(width=2))

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            fig.write_html(tmp_file.name)
            tmp_file_path = tmp_file.name

        self.browser.setUrl(QUrl.fromLocalFile(tmp_file_path))

    def on_smoothing_toggle_clicked(self):
        self.smoothing_enabled = self.smoothing_button.isChecked()
        self.update_plot()
