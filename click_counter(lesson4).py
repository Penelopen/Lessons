import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont

click_cnt = [0] # Список для хранения лишь одного значения
def on_click():
    click_cnt[0] += 1 # Почему-то с обычным счётчиком вылетает...
    label.setText(f"Счетчик: {click_cnt[0]}") if click_cnt[0] < 10 else label.setText(f"{' '*12}Ура!\nВы дотыкали до {click_cnt[0]}")

app = QApplication(sys.argv)

# Рисуем окно
window = QWidget()
window.setWindowTitle("Счетчик кликов")
window.setGeometry(400, 200, 800, 600)

# Слой со счётчиком
layout = QHBoxLayout()
label = QLabel('Счетчик: 0', parent=window)
font = QFont("Tahoma", 16)
font.setBold(True)
label.setFont(font)
label.setStyleSheet("color: #008000;")
label.setGeometry(300, 300, 400, 100)
window.setLayout(layout)

# Кнопонька
button = QPushButton("Кликни меня", window)
button.setFont(font)
button.setGeometry(300, 200, 300, 40)  # Установка позиции и размера кнопки
button.clicked.connect(on_click)

# Магия
window.show()
app.exec()