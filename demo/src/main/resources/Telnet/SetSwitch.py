from OutputLogger import *
from TelnetConnection import *
import MessageHandle
import time


def setSwitch(host_ip,password_login,password_enable,vlan1,vlan2,interface1,interface2,router_interface):
    # 测试Telnet连接Switch主机
    host_ip = host_ip
    password_login = password_login
    password_enable = password_enable
    commands_switch = []
    commands_switch.append("config terminal")
    commands_switch.append("vtp mode transparent")
    commands_switch.append(vlan1)
    commands_switch.append("exit")
    commands_switch.append(vlan2)
    commands_switch.append("exit")
    commands_switch.append("interface fastEthernet "+interface1)
    commands_switch.append("switchport mode access")
    commands_switch.append("switchport access "+vlan1)
    commands_switch.append("exit")
    commands_switch.append("interface fastEthernet " + interface2)
    commands_switch.append("switchport mode access")
    commands_switch.append("switchport access " + vlan2)
    commands_switch.append("exit")
    commands_switch.append("interface fastEthernet "+router_interface)
    commands_switch.append("switchport trunk encapsulation dot1q")
    commands_switch.append("switchport mode trunk")
    commands_switch.append("switchport trunk allowed vlan all")
    commands_switch.append("exit")
    commands_switch.append("exit")
    commands_switch.append("show vlan")

    logger = OutputLogger(True, False, "../telnet_log/%s.txt" % time.strftime("%Y-%m-%d %H.%M.%S", time.localtime()))
    telnet_client_Switch = TelnetClient(logger)
    logger.handleMsg("*****原始输出*****")
    original_result_out = list()
    handle_result_out = list()
    if telnet_client_Switch.loginHostSwitch(host_ip, password_login, password_enable):
        original_result_out,handle_result_out = telnet_client_Switch.executeSomeCommand(commands_switch, "Switch")
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
    host_ip = "192.168.0.2"
    password_login = "CISCO"
    password_enable = "CISCO"
    vlan1 = "vlan 10"
    vlan2 = "vlan 20"
    interface1 = "0/1"
    interface2 = "0/11"
    router_interface = "0/24"
    setSwitch(host_ip, password_login, password_enable, vlan1, vlan2, interface1, interface2, router_interface)'''
