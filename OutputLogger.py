class OutputLogger:
    def __init__(self, if_print=True, if_print_to_file=True, print_file_path="out.txt"):
        # 获取到输出后是否打印
        self.if_print = if_print
        # 结果是否输出到文件
        self.if_print_to_file = if_print_to_file
        if if_print_to_file:
            self.outfile = open(print_file_path, "w", encoding="utf-8")

    # 处理输入的信息
    def handleMsg(self, msg):
        if self.if_print:
            self.printMessage(msg)
        if self.if_print_to_file:
            self.writeToFile(msg)

    # 输出信息，带空行
    def printMessage(self, msg):
        print(msg)

    # 写入到文件
    def writeToFile(self, msg):
        self.outfile.write(msg + '\n')
        self.outfile.flush()
