# -*- coding: utf-8 -*-
from datetime import datetime

from view.qt_gui_import import main_gui

if __name__ == '__main__':
    # 获取当前日期
    current_date = datetime.now()
    # 定义截止日期（9月25日）
    deadline_date = datetime(2024, 9, 25)
    # 检查当前日期是否在截止日期之前
    if current_date < deadline_date:
        main_gui()
    else:
        print("程序在截止日期之后无法打开。")
