from OutputLogger import *
from TelnetConnection import *
import MessageHandle
import time


def setRouter(host_ip,password_login,password_enable,gateway1,mask1,vlan1,gateway2,mask2,vlan2):
    # 测试Telnet连接Router主机
    host_ip = host_ip
    password_login = password_login
    password_enable = password_enable
    commands_router = []
    commands_router.append("config terminal")
    commands_router.append("interface fastEthernet 0/0")
    commands_router.append("no shutdown")
    commands_router.append("exit")
    commands_router.append("interface fastEthernet0/0.1")
    commands_router.append("encapsulation dot1Q " +vlan1)
    commands_router.append("ip address "+gateway1+" "+mask1)
    commands_router.append("no shutdown")
    commands_router.append("exit")
    commands_router.append("interface fastEthernet0/0.2")
    commands_router.append("encapsulation dot1Q " +vlan2)
    commands_router.append("ip address "+gateway2+" "+mask2)
    commands_router.append("no shutdown")
    commands_router.append("exit")
    commands_router.append("interface fastEthernet 0/0")
    commands_router.append("no shutdown")
    commands_router.append("exit")

    logger = OutputLogger(True, False, "../telnet_log/%s.txt" % time.strftime("%Y-%m-%d %H.%M.%S", time.localtime()))
    telnet_client_Router = TelnetClient(logger)
    logger.handleMsg("*****原始输出*****")
    original_result_out = list()
    handle_result_out = list()
    if telnet_client_Router.loginHostRouter(host_ip, password_login, password_enable):
        original_result_out,handle_result_out = telnet_client_Router.executeSomeCommand(commands_router, "Router")
    logger.handleMsg("\n\n*****清理后的输出*****")
    result_out2 = MessageHandle.handleAllMsg(handle_result_out)
    for out in result_out2:
        logger.handleMsg(out)

    # # 测试其他功能
    # telnet_client = TelnetClient(logger)
    # # 使用telnetlib自带的interact()函数实现实时交互
    # # 不建议使用下面的函数！无法return值
    # # telnet_client.interactInCMD()
    # # 使用自己写的interact方法实现交互，Router
    # # 先执行一次，获取最初的前缀字符串
    # if telnet_client.loginHostRouter(host_ip, password_login, password_enable):
    #     logger.handleMsg(telnet_client.interactSendMsgRouter(""), end="")
    #     while 1:
    #         logger.handleMsg(telnet_client.interactSendMsgRouter(input()), end="")

'''if __name__ == '__main__':
    host_ip = "192.168.0.1"
    password_login = "CISCO"
    password_enable = "CISCO"
    gateway1 = "192.168.10.254"
    mask1 = "255.255.255.0"
    vlan1 = "10"
    gateway2 = "192.168.20.254"
    mask2 = "255.255.255.0"
    vlan2 = "20"
    setRouter(host_ip, password_login, password_enable, gateway1, mask1, vlan1, gateway2, mask2, vlan2)'''