import telnetlib
import time
import MessageHandle as msg_handle

class TelnetClient:
    def __init__(self, logger):
        self.tn = telnetlib.Telnet()
        # 日志记录对象
        self.logger = logger
        # 是否是第一次执行interact交互
        self.if_first_interact = True

    # 发送命令，原子指令
    # 输入的命令必须是经过encode过的指令
    def writeCMD(self, command):
        self.tn.write(command)
        time.sleep(0.1)

    # telnet登录主机，Linux
    def loginHostLinux(self, host_ip, username, password):
        try:
            self.tn.open(host_ip, port=23)
        except:
            self.logger.handleMsg('%s网络连接失败' % host_ip)
            return False
        # 等待login出现后输入用户名，最多等待20秒
        self.tn.read_until(b'login', timeout=20)
        self.writeCMD((username + '\n').encode())
        # 等待Password出现后输入用户名，最多等待20秒
        self.tn.read_until(b'Password', timeout=20)
        self.writeCMD((password + '\n').encode())
        # 延时1秒再收取返回结果，给服务端足够响应时间
        time.sleep(1)
        # 获取登录结果
        command_result = self.tn.read_very_eager().decode()
        if 'Login incorrect' not in command_result:
            self.logger.handleMsg('%s登录成功' % host_ip)
            # # 开始发送心跳包，防止telnet连接断开
            # _thread.start_new_thread(self.sendHeartbeat, (30,))
            return True
        else:
            self.logger.handleMsg('%s登录失败，用户名或密码错误' % host_ip)
            return False

    # telnet登录主机，Router
    def loginHostRouter(self, host_ip, password_login, password_enable):
        try:
            self.tn.open(host_ip, port=23)
        except:
            self.logger.handleMsg('%s网络连接失败' % host_ip)
            return False
        # 等待Password出现后输入用户名，最多等待20秒
        self.tn.read_until(b'Password', timeout=20)
        self.writeCMD((password_login + '\n').encode())
        # 进入enable模式，需要再次输入密码
        self.tn.read_until(b'Router>', timeout=20)
        self.writeCMD('enable\n'.encode())
        self.tn.read_until(b'Password', timeout=20)
        self.writeCMD((password_enable + '\n').encode())
        # 延时1秒再收取返回结果，给服务端足够响应时间
        time.sleep(1)
        # 获取登录结果
        command_result = self.tn.read_very_eager().decode()
        if 'Router#' in command_result:
            self.logger.handleMsg('%s登录成功' % host_ip)
            # # 开始发送心跳包，防止telnet连接断开
            # _thread.start_new_thread(self.sendHeartbeat, (30,))
            return True
        else:
            self.logger.handleMsg('%s登录失败，用户名或密码错误' % host_ip)
            return False
    def loginHostSwitch(self, host_ip, password_login, password_enable):
        try:
            self.tn.open(host_ip, port=23)
        except:
            self.logger.handleMsg('%s网络连接失败' % host_ip)
            return False
        # 等待Password出现后输入用户名，最多等待20秒
        self.tn.read_until(b'Password', timeout=20)
        self.writeCMD((password_login + '\n').encode())
        # 进入enable模式，需要再次输入密码
        self.tn.read_until(b'Switch>', timeout=20)
        self.writeCMD('enable\n'.encode())
        self.tn.read_until(b'Password', timeout=20)
        self.writeCMD((password_enable + '\n').encode())
        # 延时1秒再收取返回结果，给服务端足够响应时间
        time.sleep(1)
        # 获取登录结果
        command_result = self.tn.read_very_eager().decode()
        print(command_result)
        if 'Switch#' in command_result:
            self.logger.handleMsg('%s登录成功' % host_ip)
            # # 开始发送心跳包，防止telnet连接断开
            # _thread.start_new_thread(self.sendHeartbeat, (30,))
            return True
        else:
            self.logger.handleMsg('%s登录失败，用户名或密码错误' % host_ip)
            return False



    # 发送心跳包，以保持telnet的连接
    def sendHeartbeat(self, delay_time):
        while 1:
            time.sleep(delay_time)
            self.writeCMD('\n'.encode())

    # 执行传输过来的一条指令，返回所有原始输出结果
    def executeOneCommand(self, command, cmd_type):
        if cmd_type == "Linux":
            self.writeCMD((command + '\n').encode())
            original_result = self.tn.read_until(b']# ', timeout=30).decode()
            original_result = original_result.replace("\r\n", "\n")
            handle_result = ""
            for str in original_result.split('\n'):
                handle_result += msg_handle.handleMsgFromLinux(str) + '\n'
            handle_result = handle_result[:-1]
            self.logger.handleMsg(original_result)
            return original_result, handle_result
        elif cmd_type == "Router":
            self.writeCMD((command + '\n').encode())
            original_result = self.tn.read_until(b'Router', timeout=30).decode()
            original_result = original_result.replace("\r\n", "\n")
            handle_result = ""
            for str in original_result.split('\n'):
                if str == command:
                    handle_result += r"$$delete$$\n"
                    continue
                handle_result += msg_handle.handleMsgFromRouter(str) + '\n'
            handle_result = handle_result[:-1]
            self.logger.handleMsg(original_result)
            return original_result, handle_result
        elif cmd_type == "Switch":
            self.writeCMD((command + '\n').encode())
            original_result = self.tn.read_until(b'Switch', timeout=30).decode()
            original_result = original_result.replace("\r\n", "\n")
            handle_result = ""
            for str in original_result.split('\n'):
                if str == command:
                    handle_result += r"$$delete$$\n"
                    continue
                handle_result += msg_handle.handleMsgFromRouter(str) + '\n'
            handle_result = handle_result[:-1]
            self.logger.handleMsg(original_result)
            return original_result, handle_result
        else:
            return "", ""

    # 执行传输过来的命令集合，返回所有原始输出结果
    def executeSomeCommand(self, commands, cmd_type):
        original_result_list = list()
        handle_result_list = list()
        for com in commands:
            original_result,handle_result=self.executeOneCommand(com, cmd_type)
            original_result_list.append(original_result)
            handle_result_list.append(handle_result)
        return original_result_list,handle_result_list

    # 实时交互的Telnet命令
    def interactInCMD(self):
        self.tn.interact()

    # Telnet-Linux交互，发送命令，并获取返回值
    def interactSendMsgLinux(self, msg):
        if self.if_first_interact:
            self.if_first_interact = False
            self.writeCMD('\n'.encode())
            return self.tn.read_very_eager().decode()
        else:
            self.writeCMD((msg + '\n').encode())
            return self.tn.read_until(b']# ', timeout=30).decode()

    # Telnet-Router交互，发送命令，并获取返回值
    def interactSendMsgRouter(self, msg):
        if self.if_first_interact:
            self.if_first_interact = False
            self.writeCMD('\n'.encode())
            return self.tn.read_very_eager().decode()
        else:
            self.writeCMD((msg + '\n').encode())
            return self.tn.read_until(b'Router', timeout=30).decode()

    def interactSendMsgSwitch(self, msg):
        if self.if_first_interact:
            self.if_first_interact = False
            self.writeCMD('\n'.encode())
            return self.tn.read_very_eager().decode()
        else:
            self.writeCMD((msg + '\n').encode())
            return self.tn.read_until(b'Switch', timeout=30).decode()

    # 退出telnet
    def logoutHost(self):
        self.writeCMD("logout\n".encode())
