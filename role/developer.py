import os
import re

from core.kimi_core import kimi_continue

import subprocess

def know_ledge(info, planner) -> str :
    return f"根据功能 {info} 生成一个完整的代码 你回复的内容只能是一个代码块 比如某某类只回复一个类的完整代码 原计划 {planner} "



def delete_files_in_folder(folder_path):
    if os.path.exists(folder_path):
        print(f"正在删除文件夹 {folder_path} 中的所有内容")
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"文件 {file_path} 已成功删除。")
            elif os.path.isdir(file_path):
                delete_files_in_folder(file_path)  # 递归删除子文件夹中的文件
                os.rmdir(file_path)  # 删除空文件夹
                print(f"文件夹 {file_path} 已成功删除。")
    else:
        print(f"文件夹 {folder_path} 不存在。")


def extract_code_blocks(markdown_text):
    """
    从Markdown文本中提取代码块及其语言类型。
    参数:
    markdown_text (str): 包含Markdown代码块的文本。
    返回:
    list: 提取的代码块及其语言类型列表。
    """
    # 使用正则表达式匹配Markdown代码块及其语言类型
    code_blocks = re.findall(r'```(\w+)\n([\s\S]*?)```', markdown_text)
    return code_blocks


def remove_extra_indentation(code):
    """
    删除代码块中多余的缩进。
    参数:
    code (str): 代码块内容。
    返回:
    str: 删除多余缩进后的代码块内容。
    """
    lines = code.split('\n')
    min_indent = float('inf')
    # 计算最小缩进
    for line in lines:
        if line.strip():  # 忽略空行
            indent = len(line) - len(line.lstrip())
            if indent < min_indent:
                min_indent = indent
    # 删除最小缩进
    if min_indent != float('inf'):
        lines = [line[min_indent:] if line.strip() else line for line in lines]
    return '\n'.join(lines)


# def get_file_extension(language):
#     """
#     根据语言类型获取文件扩展名。
#     参数:
#     language (str): 代码块的语言类型。
#     返回:
#     str: 对应的文件扩展名。
#     """
#     extensions = {
#         'python': 'py',
#         'javascript': 'js',
#         'java': 'java',
#         'c': 'c',
#         'yaml': 'yaml',
#         'cpp': 'cpp',
#         'kotlin': 'kt',  # 添加Kotlin的文件扩展名
#         # 可以继续添加其他语言类型和对应的文件扩展名
#     }
#     return extensions.get(language, 'txt')  # 默认返回'txt'



def write_code_to_file(code_blocks, folder_path):
    for lang, code in code_blocks:  # 删除多余的缩进
        code = remove_extra_indentation(code)
        folder_path = folder_path.replace('\\\\', '\\')
        folder_path = folder_path.replace('/', '\\')

        # 确保父目录存在
        os.makedirs(os.path.dirname(folder_path), exist_ok=True)

        print(f"代码块已写入文件: {folder_path} 内容 {lang}")
        with open(folder_path, 'w', encoding='utf-8') as file:  # 指定编码为UTF-8
            file.write(code)  # 直接写入原始代码块内容



def put_markdown_code_to_file(markdown_text, folder_path):
    """
    这也是最后开发那一步 由程序员 AI 回复 代码数据时使用
    参数:
    language (str): 代码块的语言类型。
    返回:
    str: 对应的文件扩展名。
    """
    code_blocks = extract_code_blocks(markdown_text)
    # 将代码块写入对应语言类型的文件
    write_code_to_file(code_blocks, folder_path)




def command_to_handle(command, planner):
    """
    将命令转换为操作去掉用法
    比如
      创建文件夹 E:\JavaKotlin\devTest\JoinKeyPlugin
      创建文件夹 E:\JavaKotlin\devTest\JoinKeyPlugin\src
      创建文件夹 E:\JavaKotlin\devTest\JoinKeyPlugin\src\main
      创建文件夹 E:\JavaKotlin\devTest\JoinKeyPlugin\src\main\java
      创建文件夹 E:\JavaKotlin\devTest\JoinKeyPlugin\src\main\resources
      代码结构 E:\JavaKotlin\devTest\JoinKeyPlugin\src\main\java\com\example\joinkey | 包含插件主类和事件监听器，实现插件核心功能
      代码结构 E:\JavaKotlin\devTest\JoinKeyPlugin\src\main\resources | 包含配置文件和资源文件，定义插件配置和资源内容
    :param command:
    :return:
    """
    if "创建文件夹" in command:
        folder_name = command.split("创建文件夹")[1].strip()
        folder_name = folder_name.split("|")[0].strip()
        folder_name = folder_name.replace('\\\\', '\\')  # 将反斜杠替换为正斜杠
        folder_name = folder_name.replace('/', '\\')  # 将反斜杠替换为正斜杠
        print(f"创建文件夹 - {folder_name}")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    elif "代码结构" in command:
        code = command.split("代码结构")[1].strip()
        info = code.split("|")
        need_text = info[1].strip()
        path = info[0].strip()
        path = path.replace('\\\\', '\\')
        path = path.replace('/', '\\')
        print(f"Kimi生成代码 - {path}, 功能{need_text}")
        kimi_code = kimi_continue(know_ledge(code, planner))
        put_markdown_code_to_file(kimi_code, info[0].strip())
    elif "执行指令" in command:
        command_str = command.split("执行指令")[1].strip()
        split_str = command_str.split("|")
        in_here = split_str[0].strip()
        in_here = in_here.replace('\\\\', '\\')
        in_here = in_here.replace('/', '\\')
        command_str = split_str[1].strip()
        print(f"执行命令{command_str} 路径{in_here}")
        execute_shell_command(command_str, in_here)
        # print(f"返回控制台的输出")



# 执行shell命令 command 是命令 与 folder_path 是在哪个目录下运行 命令   返回控制台的输出

def execute_shell_command(command, fold_path):
    # 设置新的控制台窗口
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    # 在新窗口中执行命令
    subprocess.Popen(f'start cmd /k "cd /d {fold_path} && {command}"', cwd=fold_path, shell=True, startupinfo=startupinfo)




def create_folder_if_not_exists(file_path):
    """
    根据文件路径检测并创建文件夹。

    参数:
    file_path (str): 文件的完整路径。
    """
    # 提取文件路径中的目录部分
    directory = os.path.dirname(file_path)

    # 如果目录不存在，则创建它
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"文件夹 '{directory}' 已创建。")
    else:
        print(f"文件夹 '{directory}' 已存在。")

# 利用os创建文件
def create_file(folder_path, file_name) :
    if not os.path.exists(folder_path) :
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)
    # 如果文件不存在，则创建文件
    if not os.path.exists(file_path) :
        file = open(file_path, "w")
        file.close()