import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QComboBox, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QListWidget, QFrame, QAbstractItemView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor


class MetricCard(QFrame):
    """Custom dashboard metric layout card."""

    def __init__(self, title, value, subtitle="", alert_mode=False):
        super().__init__()
        self.setObjectName("MetricCard")

        bg_color = "#2d1a1a" if alert_mode else "#1e1e24"
        border_color = "#ef4444" if alert_mode else "#2d2d34"
        val_color = "#f87171" if alert_mode else "#ffffff"

        self.setStyleSheet(f"""
            QFrame#MetricCard {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_title = QLabel(title.upper())
        lbl_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #a1a1aa;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_val = QLabel(str(value))
        lbl_val.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        lbl_val.setStyleSheet(f"color: {val_color}; margin: 5px 0px;")
        lbl_val.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)

        if subtitle:
            lbl_sub = QLabel(subtitle)
            lbl_sub.setFont(QFont("Segoe UI", 9))
            lbl_sub.setStyleSheet("color: #71717a;")
            lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl_sub)


class BlazeAlertApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BlazeAlert - Active Fires Dashboard")
        self.resize(1000, 620)
        self.setMinimumSize(850, 550)

        # Central Window Widget & Structural Base
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        # Main Layout (Padding and spacing around the workspace edges)
        workspace_layout = QVBoxLayout(central_widget)
        workspace_layout.setContentsMargins(30, 25, 30, 30)
        workspace_layout.setSpacing(20)

        # Application stylesheets matching the modern dark mockups
        self.setStyleSheet("""
            QWidget#CentralWidget {
                background-color: #121214;
            }
            QLabel#AppLogoTitle {
                color: #f97316;
                font-size: 20px;
                font-weight: bold;
            }
            QLabel#SectionTitle {
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            QComboBox {
                background-color: #1e1e24;
                border: 1px solid #2d2d34;
                border-radius: 6px;
                padding: 6px 12px;
                color: #ffffff;
            }
            QPushButton#UpdateBtn {
                background-color: #e11d48;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 7px 16px;
                font-weight: bold;
            }
            QPushButton#UpdateBtn:hover { background-color: #be123c; }

            /* Table Customizations */
            QTableWidget {
                background-color: #18181c;
                border: 1px solid #252529;
                border-radius: 8px;
                gridline-color: #252529;
                color: #e4e4e7;
            }
            QHeaderView::section {
                background-color: #1e1e24;
                color: #a1a1aa;
                padding: 8px;
                border: none;
                font-weight: bold;
                border-bottom: 1px solid #252529;
            }

            /* Feed List styling */
            QListWidget {
                background-color: #18181c;
                border: 1px solid #252529;
                border-radius: 8px;
                color: #e4e4e7;
                padding: 5px;
            }
        """)

        # --- TOP HEADER BAR ---
        top_bar = QHBoxLayout()

        # Re-introduced the app logo branding into the top menu bar directly
        app_logo = QLabel("🔥 BlazeAlert")
        app_logo.setObjectName("AppLogoTitle")
        top_bar.addWidget(app_logo)
        top_bar.addStretch()

        lbl_district = QLabel("District:")
        lbl_district.setStyleSheet("color: #a1a1aa;")
        self.combo_district = QComboBox()
        self.combo_district.addItems(["Lisbon District", "Porto District", "Faro District"]) # TODO : adicionar distritos
        self.combo_district.setFixedWidth(160)

        lbl_city = QLabel("City:")
        lbl_city.setStyleSheet("color: #a1a1aa;")
        self.combo_city = QComboBox()
        self.combo_city.addItems(["Sintra", "Cascais", "Mafra", "Loures"]) # TODO: adicionar cidades
        self.combo_city.setFixedWidth(140)

        btn_update = QPushButton("UPDATE LOCATION")
        btn_update.setObjectName("UpdateBtn")
        btn_update.clicked.connect(self.update_incidents)

        top_bar.addWidget(lbl_district)
        top_bar.addWidget(self.combo_district)
        top_bar.addWidget(lbl_city)
        top_bar.addWidget(self.combo_city)
        top_bar.addWidget(btn_update)
        workspace_layout.addLayout(top_bar)

        # Incident Table Title Block
        lbl_table_header = QLabel("ACTIVE INCIDENTS IN SINTRA") # TODO : seleccionar cidade correcta
        lbl_table_header.setObjectName("SectionTitle")
        workspace_layout.addWidget(lbl_table_header)

        # Incidents List Table Grid Setup
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(
            ["Incident ID", "Status", "Intensity", "Location Description", "Last Updated"])
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Format table columns to adapt dynamically
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        workspace_layout.addWidget(self.table_widget)

        # --- BOTTOM DATA/TICKER PANELS ---
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        # Live Stats Column Layout
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(15)

        # TODO : criar string dependendo da cidade escolhida
        self.card_active = MetricCard("Total Active Fires In Sintra", "3", "Action Required", alert_mode=True)
        self.card_area = MetricCard("Total Area Affected", "120 HA", "Fire Weather Conditions Apply")

        stats_layout.addWidget(self.card_active)
        stats_layout.addWidget(self.card_area)
        bottom_row.addLayout(stats_layout, stretch=2)

        # Right Side Alert Ticker Panel
        ticker_container = QVBoxLayout()
        lbl_ticker_title = QLabel("ALERT TICKER")
        lbl_ticker_title.setObjectName("SectionTitle")

        self.ticker_feed = QListWidget()

        ticker_container.addWidget(lbl_ticker_title)
        ticker_container.addWidget(self.ticker_feed)
        bottom_row.addLayout(ticker_container, stretch=3)

        workspace_layout.addLayout(bottom_row)

        # Load data items
        self.update_incidents()

    def update_feed(self):
        print("Update Feed")
        self.ticker_feed.clear()

        # TODO: adicionar dados
        self.ticker_feed.addItems([
            "⚠️ [13:50] New Report (Critical) us controlled limits canus Sintra.",
            "ℹ️ [12:36] Status Update: Incident 0002 brought under high control measures.",
            "⚠️ [12:32] Medium smoke observation found in Center Peslivstra, Sintra.",
            "ℹ️ [11:15] Emergency management response dispatch sent to location Salariode."
        ])

    def update_incidents(self):
        """Populates the incidents table with structured analytical dataset metrics."""
        print("Update Incidents")
        self.update_feed()

        # TODO adicionar dados
        mock_incidents = [
            ("0001", "New Report (Critical)", "Medium", "Soyaoutsitroisenation Found in Padiano, Sintra",
             "17/03/2026, 13:50"),
            ("0002", "Controlled", "High", "Location Saliariode Maisins, Sintra", "17/03/2026, 12:36"),
            ("0003", "Controlled", "Medium", "Location Center Peslivstra, Sintra", "17/03/2026, 12:32"),
            ("0004", "Controlled", "Sower", "Location Sarerta, Sintra", "17/03/2026, 11:15")
        ]

        self.table_widget.setRowCount(len(mock_incidents))

        for row_idx, data in enumerate(mock_incidents):
            for col_idx, text in enumerate(data):
                item = QTableWidgetItem(text)

                if col_idx == 1:
                    if "Critical" in text:
                        item.setForeground(QColor("#f87171"))
                    else:
                        item.setForeground(QColor("#4ade80"))

                self.table_widget.setItem(row_idx, col_idx, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = BlazeAlertApp()
    window.show()
    sys.exit(app.exec())