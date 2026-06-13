import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QComboBox, QPushButton,
                               QLineEdit, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QFont, QColor, QPainter
# Import Chart modules natively available in PySide6
from PySide6.QtCharts import QChart, QChartView, QSplineSeries, QValueAxis, QCategoryAxis


class WeatherCard(QFrame):
    """Custom widget representing a single day's weather card."""

    def __init__(self, day_name, date_str, condition, emoji, current_temp, high_temp, low_temp, wind, precip=None):
        super().__init__()
        self.setObjectName("WeatherCard")
        self.setStyleSheet("""
            QFrame#WeatherCard {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
            QLabel { color: #f8fafc; }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(15, 20, 15, 20)

        lbl_day = QLabel(day_name)
        lbl_day.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        lbl_day.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_date = QLabel(date_str)
        lbl_date.setFont(QFont("Segoe UI", 9))
        lbl_date.setStyleSheet("color: #94a3b8;")
        lbl_date.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_cond = QLabel(condition)
        lbl_cond.setFont(QFont("Segoe UI", 10))
        lbl_cond.setStyleSheet("color: #cbd5e1;")
        lbl_cond.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_icon = QLabel(emoji)
        lbl_icon.setFont(QFont("Segoe UI", 40))
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_curr_label = QLabel("NOW")
        lbl_curr_label.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        lbl_curr_label.setStyleSheet("color: #38bdf8;")
        lbl_curr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_temp = QLabel(f"{current_temp}°C")
        lbl_temp.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        lbl_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)

        high_low_layout = QHBoxLayout()
        high_low_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        high_low_layout.setSpacing(12)

        lbl_high = QLabel(f"🔺 {high_temp}°C")
        lbl_high.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        lbl_high.setStyleSheet("color: #f87171;")

        lbl_low = QLabel(f"🔻 {low_temp}°C")
        lbl_low.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        lbl_low.setStyleSheet("color: #60a5fa;")

        high_low_layout.addWidget(lbl_high)
        high_low_layout.addWidget(lbl_low)

        lbl_wind = QLabel(f"💨 {wind}")
        lbl_wind.setFont(QFont("Segoe UI", 9))
        lbl_wind.setStyleSheet("color: #94a3b8; margin-top: 3px;")
        lbl_wind.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl_day)
        layout.addWidget(lbl_date)
        layout.addWidget(lbl_cond)
        layout.addWidget(lbl_icon)
        layout.addWidget(lbl_curr_label)
        layout.addWidget(lbl_temp)
        layout.addLayout(high_low_layout)
        layout.addWidget(lbl_wind)

        if precip:
            lbl_precip = QLabel(f"💧 {precip}")
            lbl_precip.setFont(QFont("Segoe UI", 9))
            lbl_precip.setStyleSheet("color: #38bdf8;")
            lbl_precip.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl_precip)


class DistrictWeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DistrictWeather - 5-Day Evolution Tracking")
        self.resize(1200, 750)  # Slightly widened to naturally accommodate 5 cards cleanly
        self.setMinimumSize(1050, 680)

        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 20, 30, 30)
        main_layout.setSpacing(20)

        self.setStyleSheet("""
            QWidget#CentralWidget { background-color: #0f172a; }
            QLabel#AppTitle { color: #38bdf8; font-size: 22px; font-weight: bold; }
            QLabel#SectionTitle { color: #ffffff; font-size: 14px; font-weight: bold; }
            QLabel#FieldLabel { color: #94a3b8; font-size: 12px; }
            QComboBox, QLineEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 6px 12px;
                color: #f8fafc;
                font-size: 12px;
            }
            QPushButton {
                background-color: #0284c7;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 7px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0369a1; }
        """)

        # --- TOP HEADER BAR ---
        header_layout = QHBoxLayout()
        app_title = QLabel("🌧 DistrictWeather")
        app_title.setObjectName("AppTitle")
        header_layout.addWidget(app_title)
        header_layout.addStretch()

        self.combo_district = QComboBox()
        self.combo_district.addItems(["Avenida da Liberdade", "Baixa", "Alfama", "Belém"]) #TODO adicionar distritos
        self.combo_city = QComboBox()
        self.combo_city.addItems(["Lisbon", "Porto", "Faro", "Braga"]) # TODO adicionar cidades
        btn_get_weather = QPushButton("Get Weather")
        btn_get_weather.clicked.connect(self.update_weather)

        header_layout.addWidget(QLabel("District:", objectName="FieldLabel"))
        header_layout.addWidget(self.combo_district)
        header_layout.addWidget(QLabel("City:", objectName="FieldLabel"))
        header_layout.addWidget(self.combo_city)
        header_layout.addWidget(btn_get_weather)
        main_layout.addLayout(header_layout)

        # --- SEARCH BAR ---
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search locations...")
        main_layout.addWidget(self.search_bar)

        # --- 5-DAY FORECAST CARDS ROW ---
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(12)  # Decreased slightly to space out 5 items nicely
        main_layout.addLayout(self.cards_layout)

        # --- TEMPERATURE EVOLUTION GRAPH PANEL ---
        lbl_graph_title = QLabel("TEMPERATURE EVOLUTION (5-DAY TREND OUTLOOK)")
        lbl_graph_title.setObjectName("SectionTitle")
        main_layout.addWidget(lbl_graph_title)

        # Setup the Chart View container element
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet("""
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
        """)
        main_layout.addWidget(self.chart_view, stretch=1)

        # Generate layout views populated with telemetry sets
        self.update_weather()

    def update_weather(self):
        """Refreshes structural cards data and redraws the trend chart visualization."""
        print("Update Weather")
        # 1. Refresh metric cards row layout
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Updated to include 5 Days total (Current + 4 Days)
        # TODO obter dados para 5 dias
        mock_data = [
            WeatherCard("Today", "May 30", "Sunny", "☀️", "21", "24", "13", "10 km/h W"),
            WeatherCard("Sunday", "May 31", "Mostly Sunny", "⛅", "20", "23", "12", "8 km/h NW"),
            WeatherCard("Monday", "Jun 01", "Thunderstorms", "⛈️", "17", "19", "10", "15 km/h E", "90%"),
            WeatherCard("Tuesday", "Jun 02", "Rainy", "🌧️", "16", "18", "11", "12 km/h SE", "75%"),
            WeatherCard("Wednesday", "Jun 03", "Partly Cloudy", "🌥️", "19", "21", "12", "9 km/h W")
        ]

        for card in mock_data:
            self.cards_layout.addWidget(card)

        # 2. Build and update the dynamic trend graph visualization
        chart = QChart()
        chart.setBackgroundVisible(False)  # Blends into underlying styled QChartView frame
        chart.legend().hide()

        # Spline series mapping out High and Low data progressions
        high_series = QSplineSeries()
        low_series = QSplineSeries()

        # Extended data arrays to dynamically plot all 5 coordinates (Indices 0 to 4)
        high_series.append([QPointF(0, 24), QPointF(1, 23), QPointF(2, 19), QPointF(3, 18), QPointF(4, 21)])
        low_series.append([QPointF(0, 13), QPointF(1, 12), QPointF(2, 10), QPointF(3, 11), QPointF(4, 12)])

        # Apply specific colors to graphs matching high/low cards accents
        high_series.setColor(QColor("#f87171"))
        high_series.setPointsVisible(True)
        low_series.setColor(QColor("#60a5fa"))
        low_series.setPointsVisible(True)

        chart.addSeries(high_series)
        chart.addSeries(low_series)

        # X-Axis configuration expanded to cleanly map out 5 categorical intervals
        axis_x = QCategoryAxis()
        axis_x.append("Today (May 30)", 0)
        axis_x.append("Sun (May 31)", 1)
        axis_x.append("Mon (Jun 01)", 2)
        axis_x.append("Tue (Jun 02)", 3)
        axis_x.append("Wed (Jun 03)", 4)
        axis_x.setLabelsColor(QColor("#94a3b8"))
        axis_x.setLinePenColor(QColor("#334155"))
        axis_x.setGridLineVisible(False)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        high_series.attachAxis(axis_x)
        low_series.attachAxis(axis_x)

        # Y-Axis configuration handling numerical degrees scaling values bounds
        axis_y = QValueAxis()
        axis_y.setRange(5, 30)
        axis_y.setLabelFormat("%d°C")
        axis_y.setLabelsColor(QColor("#94a3b8"))
        axis_y.setLinePenColor(QColor("#334155"))
        axis_y.setGridLinePen(QColor("#1e293b"))
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        high_series.attachAxis(axis_y)
        low_series.attachAxis(axis_y)

        # Swaps running scene architecture to process fresh parameters rendering dynamically
        self.chart_view.setChart(chart)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = DistrictWeatherApp()
    window.show()
    sys.exit(app.exec())