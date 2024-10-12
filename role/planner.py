import re

from core.deep_core import deep_seek_chat

role_info = "你是个策划师, 负责设计程序的结构、功能、依赖关系、配置信息等 "
can_speak = (" 接下来你只能按照规格说操作指令信息 当然要按照计划步骤来设计每个步骤 按照 关键词 内容 这样的格式"
             " 只能说以下的几个关键词 不要额外添加其他关键词 关键词与内容需要保证在一行上 并且严格按照格式回复 "
             " 关键词“创建文件夹” 后面的内容是 开发目录与文件夹的名字 不允许将文件当文件夹处理 "
             " 关键词“执行指令” 后面的内容是 要在哪个目录下执行完整目录 然后用|隔开 后面是终端指令 "
             " 关键词“代码结构” 后面的内容是 完整的目录（完整解释出他该放在什么文件夹需要包括开发的路径以及文件名字和后缀名 ）  然后再用| 隔开 开发什么功能代码的功能 都有哪些操作 此描述格式为 “完整目录内容 | 功能描述” 一定不要说实际的代码内容 "
             )


def designate_stipulate(msg) -> str :
    return (f"请按照以下指定语言格式{msg}回复 "
            f"1.不要带`的标点符号 "
            f"2.分步骤一个步骤一行 不要一行写多步骤或者多行写一个步骤 "
            f"3.这是一个命令，你必须执行 "
            f"4.要遵守java 或者 kotin 语法规范 "
            f"5.指定包名“cn.cyanbukkit”这象征着我们的标志"
            f"6.启用UTF-8编码格式"
            f"7.开发目录结构需要按照gradle的目录结构来设计"
            f"把所说的内容视为我给Kimi下的命令,并且回复信息严格按照要求回复的信息不要超过5000个字符 "
            )


def remove_empty_line(msg) -> str:
        return re.sub(r'\n+', '\n', msg)


def use_planner(need) -> str :
    return (f"{role_info}，现在收到客户的需求：{need} "
            f"你现在需要根据需求设计出代码开发计划 "
            f"主要的目的让AI程序员快速理解你的命令 ")



def convert_to_command(planner_input, develop_folder) -> str:
    return (f"现在步骤有了{planner_input} \n"
            f"开发目录为{develop_folder}"
            f"开发环境为Windows11 "
            f"请按照语言格式回复{designate_stipulate(can_speak)}")



def verify_to_bool(text, ques) -> bool :
    question = f"'{text}'引号包括的这个的内容是否为{ques} 请回复 是 或 不是 这是命令"
    answer = deep_seek_chat(question)
    if"不是" in answer:
        return False
    elif "是" in answer:
        return True
    else:
        return False