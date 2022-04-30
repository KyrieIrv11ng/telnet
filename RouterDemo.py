from SetRouter import *
import sys
if __name__ == '__main__':
    HOST_IP = sys.argv[1]
    PASSWORD_LOGIN = sys.argv[2]
    PASSWORD_ENABLE = sys.argv[3]
    GATEWAY1 = sys.argv[4]
    MASK1 = sys.argv[5]
    VLAN1 = sys.argv[6]
    GATEWAY2 = sys.argv[7]
    MASK2 = sys.argv[8]
    VLAN2 = sys.argv[9]
    setRouter(HOST_IP,PASSWORD_LOGIN,PASSWORD_ENABLE,GATEWAY1,MASK1,VLAN1,GATEWAY2,MASK2,VLAN2)
