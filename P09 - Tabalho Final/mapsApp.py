import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QComboBox, QPushButton,
                               QLineEdit, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QFont, QColor, QPainter
from PySide6.QtCharts import QChart, QChartView, QSplineSeries, QValueAxis, QCategoryAxis


class TelemetryCard(QFrame):
    """Custom widget representing a single metric card for the journey data."""

    def __init__(self, title, main_value, subtitle, icon_emoji, accent_color="#38bdf8"):
        super().__init__()
        self.setObjectName("TelemetryCard")
        self.setStyleSheet(f"""
            QFrame#TelemetryCard {{
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }}
            QLabel {{ color: #f8fafc; }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 20, 15, 20)

        lbl_title = QLabel(title.upper())
        lbl_title.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        lbl_title.setStyleSheet(f"color: {accent_color}; letter-spacing: 1px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_icon = QLabel(icon_emoji)
        lbl_icon.setFont(QFont("Segoe UI", 36))
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_val = QLabel(main_value)
        lbl_val.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        lbl_val.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_sub = QLabel(subtitle)
        lbl_sub.setFont(QFont("Segoe UI", 9))
        lbl_sub.setStyleSheet("color: #94a3b8;")
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_icon)
        layout.addWidget(lbl_val)
        layout.addWidget(lbl_sub)


class RoutePlannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Route Analytics Tracker - Distance & Consumption (Metric)")
        self.resize(1200, 750)
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
            QLineEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 8px 12px;
                color: #f8fafc;
                font-size: 12px;
            }
            QPushButton {
                background-color: #0284c7;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0369a1; }
        """)

        # --- TOP HEADER BAR ---
        header_layout = QHBoxLayout()
        app_title = QLabel("📍 RouteAnalytics")
        app_title.setObjectName("AppTitle")
        header_layout.addWidget(app_title)
        header_layout.addStretch()

        # Swapped layout variables to support European/Metric Fuel Economy standard notation (L/100km)
        header_layout.addWidget(QLabel("Fuel Economy:", objectName="FieldLabel"))
        self.txt_efficiency = QLineEdit()
        self.txt_efficiency.setText("6.5")  # Default to roughly 36 MPG equivalent
        self.txt_efficiency.setFixedWidth(50)
        self.txt_efficiency.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.txt_efficiency)
        header_layout.addWidget(QLabel("L/100km", objectName="FieldLabel"))
        main_layout.addLayout(header_layout)

        # --- ADDRESS INPUT HOUSING LAYOUT ---
        inputs_layout = QHBoxLayout()
        inputs_layout.setSpacing(15)

        self.input_start = QLineEdit()
        self.input_start.setPlaceholderText("🛫 Enter Starting Point Address...")
        self.input_start.setText("Porto, Portugal") # TODO

        self.input_end = QLineEdit()
        self.input_end.setPlaceholderText("🛬 Enter Destination Address...")
        self.input_end.setText("Lisbon, Portugal") # TODO

        btn_calculate = QPushButton("Calculate Analytics")
        btn_calculate.clicked.connect(self.calculate_route_metrics)

        inputs_layout.addWidget(self.input_start, stretch=2)
        inputs_layout.addWidget(self.input_end, stretch=2)
        inputs_layout.addWidget(btn_calculate, stretch=1)
        main_layout.addLayout(inputs_layout)

        # --- TELEMETRY CARDS ROW ---
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(15)
        main_layout.addLayout(self.cards_layout)

        # --- ELEVATION PROFILE TREND PANEL ---
        lbl_graph_title = QLabel("TERRAIN ELEVATION PROFILE TRACKING (ROUTE GRADIENT)")
        lbl_graph_title.setObjectName("SectionTitle")
        main_layout.addWidget(lbl_graph_title)

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet("""
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
        """)
        main_layout.addWidget(self.chart_view, stretch=1)

        self.calculate_route_metrics()

    def calculate_route_metrics(self):
        """Calculates distance variables and refreshes the data displays and telemetry charts."""
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        try:
            l_per_100km = float(self.txt_efficiency.text())
        except ValueError:
            l_per_100km = 6.5

        # Metric distances (e.g., Porto to Lisbon route approximation)
        mock_distance_km = 313.5 # TODO
        mock_duration_mins = 175.0  # TODO

        # Metric Fuel Equation: (Distance * economy) / 100
        fuel_burned_liters = (mock_distance_km * l_per_100km) / 100
        est_cost_eur = fuel_burned_liters * 1.74  #

        # 1. Populating New Metric Journey Matrix Cards
        # TODO
        metrics_data = [
            TelemetryCard("Total Distance", f"{mock_distance_km} km",
                          f"~ {round(mock_distance_km / 1.609, 1)} miles alternative conversion", "🛣️", "#38bdf8"),
            TelemetryCard("Travel Duration", f"2h 55m", f"{int(mock_duration_mins)} total runtime minutes", "⏱️",
                          "#a78bfa"),
            TelemetryCard("Fuel Consumption", f"{round(fuel_burned_liters, 1)} L",
                          f"Calculated based on {l_per_100km} L/100km", "⛽", "#fbbf24"),
            TelemetryCard("Estimated Cost", f"€{round(est_cost_eur, 2)}", "Estimated at current local fuel prices", "💶",
                          "#34d399")
        ]

        for card in metrics_data:
            self.cards_layout.addWidget(card)

        # 2. Rendering the Gradient Elevation Profile Visuals
        chart = QChart()
        chart.setBackgroundVisible(False)
        chart.legend().hide()

        elevation_series = QSplineSeries()

        # Mock path elevation data coordinates
        # TODO
        elevation_series.append([
            QPointF(0, 85),  # Porto altitude
            QPointF(1, 160),
            QPointF(2, 210),  # Central Massif shifts
            QPointF(3, 95),
            QPointF(4, 15)  # Lisbon sea-level altitude
        ])

        elevation_series.setColor(QColor("#22d3ee"))
        elevation_series.setPointsVisible(True)
        chart.addSeries(elevation_series)

        axis_x = QCategoryAxis()
        axis_x.append("Start", 0)
        axis_x.append("25%", 1)
        axis_x.append("Halfway", 2)
        axis_x.append("75%", 3)
        axis_x.append("Destination", 4)
        axis_x.setLabelsColor(QColor("#94a3b8"))
        axis_x.setLinePenColor(QColor("#334155"))
        axis_x.setGridLineVisible(False)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        elevation_series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 250)
        axis_y.setLabelFormat("%d m")
        axis_y.setLabelsColor(QColor("#94a3b8"))
        axis_y.setLinePenColor(QColor("#334155"))
        axis_y.setGridLinePen(QColor("#1e293b"))
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        elevation_series.attachAxis(axis_y)

        self.chart_view.setChart(chart)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = RoutePlannerApp()
    window.show()
    sys.exit(app.exec())