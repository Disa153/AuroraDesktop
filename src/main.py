import sys
import random
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QLinearGradient, QPen, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QSlider, QComboBox,
    QCheckBox, QButtonGroup, QMessageBox
)

STYLE = """
QWidget { color: #f3f5ff; font-family: 'Segoe UI'; font-size: 14px; }
QMainWindow, QWidget#central { background: #0b1220; }
QFrame#sidebar { background: #101a2a; border-right: 1px solid #29364b; }
QFrame#card, QWidget#preview { background: #172338; border: 1px solid #2b3b54; border-radius: 14px; }
QLabel#muted { color: #9eacc2; }
QLabel#heading { font-size: 25px; font-weight: 700; }
QLabel#section { font-size: 17px; font-weight: 650; }
QPushButton { background: #26354c; border: 1px solid #354761; border-radius: 9px; padding: 10px 13px; text-align: left; }
QPushButton:hover { background: #354665; }
QPushButton:checked { background: #493777; border: 1px solid #a58aff; }
QPushButton#primary { background: #7957df; border: 0; font-weight: 650; padding: 12px; }
QSlider::groove:horizontal { height: 6px; background: #34435a; border-radius: 3px; }
QSlider::sub-page:horizontal { background: #9b7cff; border-radius: 3px; }
QSlider::handle:horizontal { background: white; width: 16px; margin: -6px 0; border-radius: 8px; }
QComboBox { background: #26354c; border: 1px solid #354761; border-radius: 8px; padding: 8px; }
QCheckBox { spacing: 9px; }
"""

class EffectPreview(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(240)
        self.effect = "Snow"
        self.intensity = 70
        self.speed = 50
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(35)
        self.set_effect(self.effect)

    def set_effect(self, effect):
        self.effect = effect
        self.particles = [
            [random.uniform(0, max(1, self.width())),
             random.uniform(0, max(1, self.height())),
             random.uniform(1, 3.2), random.uniform(.7, 2.0)]
            for _ in range(max(10, self.intensity * 2))
        ]
        self.update()

    def tick(self):
        if self.effect == "None":
            self.update()
            return
        factor = .3 + self.speed / 40
        for p in self.particles:
            p[1] += p[2] * factor
            p[0] += random.uniform(-.55, .55)
            if p[1] > self.height() + 5:
                p[1] = -5
                p[0] = random.uniform(0, max(1, self.width()))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        grad = QLinearGradient(0, 0, self.width(), self.height())
        grad.setColorAt(0, QColor("#152746"))
        grad.setColorAt(.55, QColor("#28536b"))
        grad.setColorAt(1, QColor("#0b1729"))
        painter.fillRect(self.rect(), grad)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#dcecff"))
        painter.drawEllipse(self.width() - 105, 28, 46, 46)
        painter.setBrush(QColor("#1a3048"))
        painter.drawPolygon([
            self.rect().bottomLeft(),
            self.rect().bottomLeft() + __import__("PySide6").QtCore.QPoint(int(self.width()*.24), -int(self.height()*.30)),
            self.rect().bottomLeft() + __import__("PySide6").QtCore.QPoint(int(self.width()*.48), 0),
            self.rect().bottomLeft() + __import__("PySide6").QtCore.QPoint(int(self.width()*.72), -int(self.height()*.22)),
            self.rect().bottomRight()
        ])
        if self.effect != "None":
            opacity = max(.15, self.intensity / 100)
            color = QColor("#ffffff")
            color.setAlphaF(opacity)
            for x, y, size, _ in self.particles:
                if self.effect == "Rain":
                    painter.setPen(QPen(QColor(220, 235, 245, 130), 1.4))
                    painter.drawLine(int(x), int(y), int(x-3), int(y+9))
                else:
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(color)
                    painter.drawEllipse(int(x), int(y), int(size), int(size))
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        painter.drawText(16, self.height()-16, f"Live preview  •  {self.effect}")

class AuroraWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aurora Desktop")
        self.resize(1120, 760)
        self.setMinimumSize(850, 620)
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        outer = QHBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(18, 24, 18, 18)
        logo = QLabel("✦  AURORA")
        logo.setStyleSheet("font-size:22px;font-weight:800;color:#bda8ff;")
        side.addWidget(logo)
        sub = QLabel("DESKTOP EXPERIENCE")
        sub.setObjectName("muted")
        side.addWidget(sub)
        side.addSpacing(28)

        self.stack = QStackedWidget()
        self.nav = []
        for i, title in enumerate(["Главная", "Эффекты", "Оформление", "Панель Dock", "Настройки"]):
            b = QPushButton(title)
            b.setCheckable(True)
            b.clicked.connect(lambda checked=False, index=i: self.navigate(index))
            self.nav.append(b)
            side.addWidget(b)
        side.addStretch()
        version = QLabel("Prototype 0.1.0\nPySide6 • Windows 10/11")
        version.setObjectName("muted")
        side.addWidget(version)
        outer.addWidget(side)
        outer.addWidget(self.stack, 1)

        self.preview = EffectPreview()
        self.stack.addWidget(self.home_page())
        self.stack.addWidget(self.effects_page())
        self.stack.addWidget(self.appearance_page())
        self.stack.addWidget(self.dock_page())
        self.stack.addWidget(self.settings_page())
        self.navigate(0)

    def page(self, title, subtitle=None):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(28, 24, 28, 24)
        l.setSpacing(14)
        h = QLabel(title); h.setObjectName("heading"); l.addWidget(h)
        if subtitle:
            s = QLabel(subtitle); s.setObjectName("muted"); s.setWordWrap(True); l.addWidget(s)
        return w, l

    def card(self, layout, widget):
        f = QFrame(); f.setObjectName("card")
        box = QVBoxLayout(f); box.setContentsMargins(15, 12, 15, 12); box.addWidget(widget)
        layout.addWidget(f)
        return f

    def home_page(self):
        w, l = self.page("Добро пожаловать в Aurora", "Настрой атмосферу рабочего стола Windows в одном месте.")
        self.preview.setObjectName("preview")
        l.addWidget(self.preview)
        for title, desc in [
            ("Атмосферные эффекты", "Снег, дождь, туман и другие визуальные эффекты."),
            ("Персонализация", "Акцентные цвета и оформление интерфейса."),
            ("Dock", "Макет панели быстрого запуска приложений.")
        ]:
            row = QWidget(); h = QHBoxLayout(row); h.setContentsMargins(0,0,0,0)
            labels = QVBoxLayout(); a=QLabel(title); a.setObjectName("section"); b=QLabel(desc); b.setObjectName("muted")
            labels.addWidget(a); labels.addWidget(b); h.addLayout(labels); h.addStretch()
            self.card(l, row)
        l.addStretch()
        return w

    def effects_page(self):
        w, l = self.page("Атмосферные эффекты", "Выбери эффект и настрой его интенсивность.")
        self.preview.setMinimumHeight(260); l.addWidget(self.preview)
        combo = QComboBox(); combo.addItems(["Snow", "Rain", "Fog", "Leaves", "Storm", "None"])
        combo.currentTextChanged.connect(self.preview.set_effect)
        self.card(l, combo)
        for label, attr in [("Интенсивность", "intensity"), ("Скорость", "speed")]:
            row=QWidget(); v=QVBoxLayout(row); top=QHBoxLayout(); name=QLabel(label); value=QLabel("70%" if attr=="intensity" else "50%"); top.addWidget(name); top.addStretch(); top.addWidget(value); v.addLayout(top)
            slider=QSlider(Qt.Orientation.Horizontal); slider.setRange(0,100); slider.setValue(getattr(self.preview,attr))
            def changed(x, key=attr, out=value):
                setattr(self.preview,key,x); out.setText(f"{x}%")
                if key=="intensity": self.preview.set_effect(self.preview.effect)
            slider.valueChanged.connect(changed); v.addWidget(slider); self.card(l,row)
        l.addStretch(); return w

    def appearance_page(self):
        w,l=self.page("Оформление","Настрой визуальный стиль Aurora.")
        combo=QComboBox(); combo.addItems(["Aurora Violet","Ocean Blue","Emerald","Sunset"])
        colors=["#9b7cff","#55c9e8","#46d6a0","#ff718b"]
        combo.currentIndexChanged.connect(lambda i:self.set_accent(colors[i]))
        self.card(l,combo)
        glass=QCheckBox("Стеклянные элементы интерфейса"); glass.setChecked(True); self.card(l,glass)
        note=QLabel("Пока настройки меняют оформление приложения. Интеграция с системными эффектами Windows будет добавлена отдельно.")
        note.setObjectName("muted"); note.setWordWrap(True); l.addWidget(note); l.addStretch()
        return w

    def dock_page(self):
        w,l=self.page("Панель Dock","Предварительный макет панели быстрого запуска.")
        check=QCheckBox("Включить панель Dock"); check.setChecked(True); self.card(l,check)
        row=QWidget(); h=QHBoxLayout(row); h.setContentsMargins(20,18,20,18); h.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for icon in ["🌐","📁","🎮","🎵","⚙️"]:
            b=QLabel(icon); b.setAlignment(Qt.AlignmentFlag.AlignCenter); b.setFixedSize(58,58); b.setStyleSheet("background:#34445d;border-radius:13px;font-size:24px;"); h.addWidget(b)
        self.card(l,row)
        note=QLabel("Это визуальный макет. Запуск приложений из Dock и размещение поверх рабочего стола ещё не реализованы.")
        note.setObjectName("muted"); note.setWordWrap(True); l.addWidget(note); l.addStretch()
        return w

    def settings_page(self):
        w,l=self.page("Настройки","Параметры запуска и поведения приложения.")
        for label, default in [("Запускать вместе с Windows",False),("Сворачивать в системный трей",True),("Проверять обновления автоматически",True)]:
            c=QCheckBox(label); c.setChecked(default); self.card(l,c)
        note=QLabel("Переключатели пока демонстрационные и не меняют параметры Windows.")
        note.setObjectName("muted"); l.addWidget(note); l.addStretch()
        return w

    def set_accent(self,color):
        self.setStyleSheet(STYLE + f" QPushButton#primary {{ background:{color}; }} QSlider::sub-page:horizontal {{ background:{color}; }}")

    def navigate(self,index):
        self.stack.setCurrentIndex(index)
        for i,b in enumerate(self.nav): b.setChecked(i==index)

def main():
    app=QApplication(sys.argv)
    app.setApplicationName("Aurora Desktop")
    app.setStyle("Fusion")
    window=AuroraWindow()
    window.setStyleSheet(STYLE)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
