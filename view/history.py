import os

from PyQt5.QtWidgets import QListWidget, QPushButton, QDialog, QVBoxLayout, QMessageBox


class HistoryWindow(QDialog):  # 继承QDialog以实现模态窗口
    def __init__(self, parent=None, need_input=None, version_input=None, mcversion_input=None, info_input=None, project_name_input=None):
        super().__init__(parent)
        self.setWindowTitle("历史记录")
        self.listbox = QListWidget(self)  # 使用QListWidget来展示历史记录
        self.import_button = QPushButton("导入", self)
        self.import_button.clicked.connect(self.import_selected)
        layout = QVBoxLayout()
        layout.addWidget(self.listbox)
        layout.addWidget(self.import_button)
        self.setLayout(layout)
        self.load_history()
        self.need_input = need_input
        self.version_input = version_input
        self.mcversion_input = mcversion_input
        self.info_input = info_input
        self.project_name_input = project_name_input

    def load_history(self):
        history_folder = "history"
        if not os.path.exists(history_folder):
            os.mkdir(history_folder)
            QMessageBox.information(self, "提示", "历史记录文件夹为空。")
            return

        for filename in os.listdir(history_folder):
            if filename.endswith(".txt"):  # 假设记录文件为txt格式
                self.listbox.addItem(filename)  # 添加文件名到列表中

    def import_selected(self):
        selected = self.listbox.currentItem()
        if not selected:
            QMessageBox.warning(self, "警告", "请先选择一个文件。")
            return
        filename = selected.text()
        filepath = os.path.join("history", filename)
        # 读取文件内容
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            content = content.split("|||")
            self.need_input.setText(content[0])
            self.version_input.setText(content[1])
            self.mcversion_input.setText(content[2])
            self.info_input.setText(content[3])
            self.project_name_input.setText(content[4])
            # QMessageBox.information(self, "完成", content)  # 这里可以根据需要进行处理