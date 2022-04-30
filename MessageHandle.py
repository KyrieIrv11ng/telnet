import re


# 清理从Linux终端返回的字符串，一行
def handleMsgFromLinux(msg):
    return re.sub(r'\[.*?@.*?]# ', r"$$delete$$", msg)

# 清理从Router返回的字符串，一行
def handleMsgFromRouter(msg):
    return re.sub(r'(Router.*?#)|(\(.*?\)#)|(Router)', r"$$delete$$", msg)

# 清理从Router返回的字符串，一行
def handleMsgFromSwitch(msg):
    return re.sub(r'(Switch.*?#)|(\(.*?\)#)|(Switch)', r"$$delete$$", msg)

# 处理返回的字符串列表，msgs是一个list
def handleAllMsg(msgs):
    all_commands = list()
    for msg in msgs:
        for one_cmd in msg.split("\n"):
            all_commands.append(one_cmd)
    handle_commands = list()
    for com in all_commands:
        if com != r"$$delete$$":
            handle_commands.append(com.replace(r"$$delete$$", ""))
    return handle_commands
