import tempfile
import pandas as pd
import plotly.graph_objects as go
from PyQt6.QtCore import pyqtSlot, QObject, QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QFileDialog, \
    QTabWidget, QListWidget, QHBoxLayout, QCheckBox, QLabel, QComboBox
from plotly.subplots import make_subplots
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox


from abstraction import EscData
from data_process import PostProcess


class CombinedView(QDialog):
    def __init__(self,e0=None,e1=None,e2=None,e3=None,post_process=False):
        super().__init__()
        self.setWindowIcon(QIcon('data/logo.ico'))
        self.df_esc0=None
        self.df_esc1=None
        self.df_esc2=None
        self.df_esc3=None
        self.esc0= None
        self.esc1= None
        self.esc2= None
        self.esc3= None
        if post_process:
            if e0:
                self.esc0 : PostProcess = e0
            if e1:
                self.esc1 : PostProcess = e1
            if e2:
                self.esc2 : PostProcess = e2
            if e3:
                self.esc3 : PostProcess = e3

            self.setWindowTitle("Combined View - Post Process")
            self.setGeometry(150, 150, 800, 600)
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
            self.checkbox_layout = QVBoxLayout()
            self.checkboxes = []
            names = ['Voltage', 'Current', 'Temperature', 'RPM', 'Throttle Duty', 'Motor Duty','Phase Current','Power']
            for i in range(8):
                checkbox = QCheckBox(names[i])
                checkbox.stateChanged.connect(self.update_status)
                self.checkbox_layout.addWidget(checkbox)
                self.checkboxes.append(checkbox)
        else :
            if e0:
                self.esc0 : EscData = e0
            if e1:
                self.esc1 : EscData = e1
            if e2:
                self.esc2 : EscData = e2
            if e3:
                self.esc3 : EscData = e3

            self.setWindowTitle("Combined View")
            self.setGeometry(150,150,800,600)
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
            self.checkbox_layout = QVBoxLayout()
            self.checkboxes = []
            names = ['Voltage','Current','Temperature','eRPM','Throttle Duty','Motor Duty','Phase Current','Power','Status 1','Status 2']
            for i in range(10):
                checkbox = QCheckBox(names[i])
                checkbox.stateChanged.connect(self.update_status)
                self.checkbox_layout.addWidget(checkbox)
                self.checkboxes.append(checkbox)


        checkbox_container = QWidget()
        checkbox_container.setLayout(self.checkbox_layout)

        self.browser = QWebEngineView()

        main_layout = QHBoxLayout()

        main_layout.addWidget(self.browser)
        main_layout.addWidget(checkbox_container)

        main_layout.setStretchFactor(checkbox_container, 1)
        main_layout.setStretchFactor(self.browser, 6)

        self.setLayout(main_layout)

        self.status_label = QLabel()
        self.checkbox_layout.addWidget(self.status_label)

        if post_process:
            print("here")
            self.load_data_post_process()
            self.update_plot(None)
        else:
            self.load_data()
            self.update_plot(None)

    def update_status(self):
        checked_boxes = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]

        
        if not checked_boxes:
            sender = self.sender()
            if sender:
                
                sender.blockSignals(True)
                sender.setChecked(True)
                sender.blockSignals(False)

                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle(" Attribute Selection Error ")
                msg.setText("<b> Please ensure that at least one data attribute remains selected. !")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()  



                return

        
        self.status_label.setText("")
        self.update_plot(checked_boxes)

    def load_data(self):
        if self.esc0:
            self.df_esc0 = pd.DataFrame({
                'Time': self.esc0.timestamp,
                'Voltage': self.esc0.voltage,
                'Current': self.esc0.current,
                'Temperature': self.esc0.temp,
                'eRPM': self.esc0.e_rpm,
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

            self.df_combined = pd.concat([self.df_esc0, self.df_esc1, self.df_esc2, self.df_esc3])
            print("Combined DataFrame created successfully")
            print(self.df_combined.head())

        except Exception as e:
            print(f"An error occurred: {e}")

    def update_plot(self, option=None):
        if option is None or not all(col in self.df_combined.columns for col in option):
            fig = make_subplots(rows=1, cols=1)
        else:
            num_columns = len(option)
            num_rows = (num_columns - 1) // 3 + 1

            fig = make_subplots(rows=num_rows, cols=3,
                                subplot_titles=option,
                                shared_xaxes='all',
                                vertical_spacing=0.15,
                                horizontal_spacing=0.1)
            esc_colors = {
                'ESC0': 'blue',
                'ESC1': 'red',
                'ESC2': 'green',
                'ESC3': 'purple'
            }
            esc_traces = {esc: [] for esc in self.df_combined['ESC'].unique()}
            for i, col_name in enumerate(option):
                row = i // 3 + 1
                col = i % 3 + 1
                for esc in self.df_combined['ESC'].unique():
                    df_filtered = self.df_combined[self.df_combined['ESC'] == esc]
                    trace = go.Scatter(
                        x=df_filtered['Time'],
                        y=df_filtered[col_name],
                        mode='lines',
                        name=f"{col_name} ({esc})",
                        line=dict(color=esc_colors.get(esc, 'black')),
                        legendgroup=esc
                    )
                    esc_traces[esc].append(trace)
                    fig.add_trace(trace, row=row, col=col)
            for esc, traces in esc_traces.items():
                fig.add_trace(
                    go.Scatter(
                        x=[],
                        y=[],
                        mode='lines',
                        name=esc,
                        line=dict(color=esc_colors.get(esc, 'black')),
                        visible='legendonly',
                        legendgroup=esc
                    )
                )
            fig.update_layout(
                showlegend=True,
                title="ESC Data Over Time"
            )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            fig.write_html(tmp_file.name)
            tmp_file_path = tmp_file.name
        self.browser.setUrl(QUrl.fromLocalFile(tmp_file_path))
