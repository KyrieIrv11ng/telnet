from SetSwitch import *
import sys
if __name__ == '__main__':
    HOST_IP = sys.argv[1]
    PASSWORD_LOGIN = sys.argv[2]
    PASSWORD_ENABLE = sys.argv[3]
    VLAN1 = sys.argv[4]
    INTERFACE1 = sys.argv[5]
    VLAN2 = sys.argv[6]
    INTERFACE2 = sys.argv[7]
    INTERFACE_ROUTER = sys.argv[8]
    setSwitch(HOST_IP,PASSWORD_LOGIN,PASSWORD_ENABLE,VLAN1,VLAN2,INTERFACE1,INTERFACE2,INTERFACE_ROUTER)
