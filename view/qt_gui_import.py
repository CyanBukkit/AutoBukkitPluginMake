import os
import sys
from platform import platform

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QMessageBox, QPushButton, QLineEdit, QFileDialog,
    QCheckBox, QTextEdit, QListWidget, QVBoxLayout, QLabel, QWidget, QProgressBar
)

from core.deep_core import deep_seek_code
from core.kimi_core import kimi_
from role.developer import delete_files_in_folder, command_to_handle
from role.planner import use_planner, remove_empty_line, convert_to_command
from view.history import HistoryWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__),  'main.ui')  # 绝对路径
        uic.loadUi(ui_path, self)  # 加载 UI 文件

        # 找到输入框和按钮
        self.mcversion_input = self.findChild(QLineEdit, 'mcversion_input')
        self.need_input = self.findChild(QLineEdit, 'need_input')

        self.is_bukkit = self.findChild(QCheckBox, 'is_bukkit')
        self.is_forge = self.findChild(QCheckBox, 'is_forge')
        self.is_fabric = self.findChild(QCheckBox, 'is_fabric')
        self.is_sponge = self.findChild(QCheckBox, 'is_sponge')

        self.project_name_input = self.findChild(QLineEdit, 'project_name_input')
        self.version_input = self.findChild(QLineEdit, 'version_input')
        self.info_input = self.findChild(QTextEdit, 'info_input')
        self.text_info = self.findChild(QLineEdit, 'text_info')

        # 假设你的按钮的对象名称是 pushButton
        self.pushButton = self.findChild(QPushButton, 'push_button')  # 需要根据实际按钮名称更改
        if self.pushButton is None:
            print("未找到按钮对象")
        else:
            self.pushButton.clicked.connect(self.collect_inputs)

        self.help_text = self.findChild(QPushButton, 'help_text')
        if self.help_text is None:
            print("未找到 help_text 对象")
        else:
            self.help_text.clicked.connect(self.help_text_clicked)

        self.history_button = self.findChild(QPushButton, 'history_button')  # 假设按钮名称为 history_button
        if self.history_button is None:
            print("未找到 history_button 对象")
        else:
            self.history_button.clicked.connect(self.open_history_window)

    def open_history_window(self):
        dialog = HistoryWindow(self,
                               mcversion_input=self.mcversion_input,
                               need_input=self.need_input,
                               version_input=self.version_input,
                               info_input=self.info_input,
                               project_name_input=self.project_name_input)  # 传递需要的输入字段
        dialog.exec_()  # 显示模态窗口

    def help_text_clicked(self):
        os.system("start https://www.cyanbukkit.net/index.php?resources/%E4%B8%80%E9%94%AEbukkit%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91.169/")
        QMessageBox.information(self, '待查看', '查看浏览器的')

    def collect_inputs(self):
        # 打开文件夹选择目录
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if not folder_path:
            return
        try:
            # 获取输入框信息
            need = self.need_input.text()
            version = self.version_input.text()
            minecraft_version = self.mcversion_input.text()
            # 平台信息
            other_info = "\n 另外，这个项目是%platform%插件需要具有%platform%的所有特征 记得创建build.gradle.kts 导入%platform%相关的的依赖"
            plat_form = []
            if self.is_bukkit.isChecked():
                plat_form.append("bukkit")
            if self.is_forge.isChecked():
                plat_form.append("forge")
            if self.is_fabric.isChecked():
                plat_form.append("fabric")
            if self.is_sponge.isChecked():
                plat_form.append("sponge")
            plat_form = ",".join(plat_form)
            other_info = other_info.replace("%platform%", plat_form)
            # 项目信息
            description = self.info_input.toPlainText()
            project_name = self.project_name_input.text()
            # 构造需要的输入信息
            need_input = (f"需求：{need}\n"
                          f"版本：{version}\n"
                          f"MineCraft版本： {minecraft_version}\n"
                          f"平台： {plat_form}\n"
                          f"需求描述：{description}\n"
                          f"项目名字: {project_name}\n"
                          f"开发路径: {folder_path}\n"
                          )
            # 显示结果
            QMessageBox.information(self, '输入的信息', need_input + "点击Ok开始创建")
            # 把需求写到history文件夹
            new_history_file = os.path.join("history", f"{project_name}_{version}.txt")
            with open(new_history_file, 'w', encoding='utf-8') as file:
                file.write(f'{need}|||{version}|||{minecraft_version}|||{description}|||{project_name}|||{folder_path}')
            need_input = need_input + other_info
            # 开始创建
            progress_window = QWidget()
            progress_window.setWindowTitle("进度")
            layout = QVBoxLayout()
            progress_bar = QProgressBar()
            progress_bar.setMaximum(100)  # 设置进度条的最大值为100
            layout.addWidget(progress_bar)
            progress_window.setLayout(layout)
            progress_window.show()
            # 执行现有逻辑
            planner = kimi_(use_planner(need_input))
            print("已经获得的计划生成计划对应的电脑软件操作指令：")
            bot_command_list = remove_empty_line(deep_seek_code(convert_to_command(planner, folder_path)))
            print("清空开发文件夹中的所有文件...")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            delete_files_in_folder(folder_path)
            # 进度条 + 执行指令
            commands = bot_command_list.split('\n')
            total_commands = len(commands)
            for i, command in enumerate(commands):
                command_to_handle(command, bot_command_list)
                # 更新进度条
                progress_percentage = int((i + 1) / total_commands * 100)
                progress_bar.setValue(progress_percentage)
            # 打开文件夹
            os.system(f"start {folder_path}")
            progress_window.close()
            QMessageBox.information(self, "成功", "创建完成")
        except Exception as e:
            QMessageBox.critical(self, '错误', f"是不是都空着？\n{e}")


def main_gui():
    # 创建history文件夹
    if not os.path.exists("history"):
        os.mkdir("history")
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
