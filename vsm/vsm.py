class VirtualStackMachine:
    def __init__(self, code):
        self.data_stack = []
        self.return_stack = []
        self.tosreg = 0x0
        self.pc = 0x0600
        self.mar = 0x0
        self.memory = [0x0] * 0x10000
        self.ir = 0x0
        
        for i in range(0,len(code)):
            self.memory[self.pc + i] = code[i]


    def run(self, debug=False):
        self.mar = self.pc
        self.ir = self.memory[self.mar]
        self.pc += 1
        
        while self.ir not 0x00:
            if debug:
                self._print_debug()

            if self.ir is 0x01:    # !
                self.mar = self.tosreg
                self.memory[self.mar] = self.data_stack.pop()
                self.tosreg = self.data_stack.pop()

            elif self.ir is 0x02:  # +
                self.tosreg = self.tosreg + self.data_stack.pop()

            elif self.ir is 0x03:  # -
                self.tosreg = self.data_stack.pop() - self.tosreg

            elif self.ir is 0x04:  # * TODO
                pass

            elif self.ir is 0x05:  # / TODO
                pass

            elif self.ir is 0x06:  # >R
                self.return_stack.append(self.tosreg)
                self.tosreg = self.data_stack.pop()

            elif self.ir is 0x07:  # @
                self.mar = self.tosreg
                self.tosreg = self.memory[self.mar]

            elif self.ir is 0x08:  # AND
                self.tosreg = self.tosreg & self.data_stack.pop()

            elif self.ir is 0x09:  # DROP
                self.tosreg = self.data_stack.pop()

            elif self.ir is 0x0A:  # DUP
                self.data_stack.append(self.tosreg)

            elif self.ir is 0x0B:  # OR
                self.tosreg = self.tosreg | self.data_stack.pop()

            elif self.ir is 0x0C:  # OVER
                self.return_stack.append(self.tosreg)
                self.tosreg = self.data_stack.pop()
                self.data_stack.append(self.tosreg)
                self.data_stack.append(self.return_stack.pop())

            elif self.ir is 0x0D:  # R>
                self.data_stack.append(self.tosreg)
                self.tosreg = self.return_stack.pop()

            elif self.ir is 0x0E:  # SHR
                self.tosreg = self.tosreg >> self.data_stack.pop()

            elif self.ir is 0x0F:  # SHL
                self.tosreg = self.tosreg << self.data_stack.pop()

            elif self.ir is 0x10:  # SWAP
                self.return_stack.append(self.tosreg)
                self.tosreg = self.data_stack.pop()
                self.data_stack.append(self.return_stack.pop())

            elif self.ir is 0x11:  # XOR
                self.tosreg = self.tosreg ^ self.data_stack.pop()

            elif self.ir is 0x12:  # [IF]
                if self.tosreg is 0:
                    self.mar = self.pc
                    self.pc = self.memory[self.mar]
                else:
                    self.pc += 1
                self.tosreg = self.data_stack.pop()

            elif self.ir is 0x13:  # [CALL]
                self.return_stack.append(self.pc)
                self.mar = self.pc
                self.pc = self.memory[self.mar]

            elif self.ir is 0x14:  # [EXIT]
                self.pc = self.return_stack.pop()

            elif self.ir is 0x15:  # [LIT]
                self.mar = self.pc
                self.pc += 1
                self.data_stack.append(self.tosreg)
                self.tosreg = self.memory[self.mar]

            elif self.ir is 0x16:  # [SYS]
                self._syscall()

            else:
                pass  # TODO: error
        
            # Fetch next instruction
            self.mar = self.pc
            self.ir = self.memory[self.mar]
            self.pc += 1

        if debug:
            self._print_debug()


    def _syscall(self):
        if self.tosreg is 0x1:    # print number
            self.mar = self.data_stack.pop()
            print("{}".format(self.memory[self.mar], end='')
        elif self.tosreg is 0x2:  # print string
            self.mar = self.data_stack.pop()
            count = 0
            for i in range(0, self.tosreg)
                print(chr(self.memory[self.mar + i]), end='')
                count += 1
            self.tosreg = count
        elif self.tosreg is 0x3:  # read input
            get_line = input()
            self.tosreg = self.data_stack.pop()
            self.mar = self.data_stack.pop()
            for i in range(0, self.tosreg):
                if i >= self.tosreg:
                    self.memory[self.mar + i] = 0x0
                self.memory[self.mar + i] = get_line[i]
        elif self.tosreg is 0x4:  # open
            pass
        elif self.tosreg is 0x5:  # read
            pass
        elif self.tosreg is 0x6:  # write
            pass
        else:
            self.tosreg = 0x0  # error code


    def _print_debug(self):
        print("Data Stack:")
        print("\t", self.tosreg, end='')
        for elem in self.data_stack:
            print(elem, end='')
        print()
        print("Return Stack:\n\t", end='')
        for elem in self.return_stack:
            print(elem, end='')
        print()
        print("PC: {:04x}".format(self.pc))
        print()



