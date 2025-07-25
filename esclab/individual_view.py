import tempfile

import pandas as pd
import plotly.express as px
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QDialog, QTabWidget

from abstraction import EscData


class IndividualView(QDialog):
    def __init__(self,e0=None,e1=None,e2=None,e3=None):
        super().__init__()
        self.setWindowIcon(QIcon('data/logo.ico'))
        self.esc0=None
        self.esc1=None
        self.esc2=None
        self.esc3=None
        self.setWindowTitle("Individual View")
        self.setGeometry(150, 150, 800, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        self.tab_widget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        if e0:
            self.esc0 : EscData = e0
            self.create_tab("ESC 0", self.create_plot_1())
        if e1:
            self.esc1 : EscData = e1
            self.create_tab("ESC 1", self.create_plot_2())
        if e2:
            self.esc2 : EscData = e2
            self.create_tab("ESC 2", self.create_plot_3())
        if e3:
            self.esc3 : EscData = e3
            self.create_tab("ESC 3", self.create_plot_4())




    def create_plot_1(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc0.voltage))),
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
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-0'+'  '+'Serial Number'+ self.esc0.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_plot_2(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc1.voltage))),
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
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-1'+'  '+'Serial Number'+ self.esc1.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_plot_3(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc2.voltage))),
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
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-2'+'  '+'Serial Number'+ self.esc2.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_plot_4(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc3.voltage))),
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
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-3'+'  '+'Serial Number'+ self.esc3.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_tab(self, title, fig):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            fig.write_html(tmp_file.name)
            tmp_file_path = tmp_file.name

        browser = QWebEngineView()
        browser.setUrl(QUrl.fromLocalFile(tmp_file_path))

        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(browser)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, title)
