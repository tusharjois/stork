import sys

class VirtualStackMachine:
    def __init__(self, code):
        self.data_stack = []
        self.return_stack = [0x0]
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
        
        while self.ir != 0x00:
            if debug:
                self._print_debug()
                # TODO breakpoints input()

            if self.ir == 0x01:    # !
                self.mar = self.tosreg
                self.memory[self.mar] = self.data_stack.pop()
                self.tosreg = self.data_stack.pop()

            elif self.ir == 0x02:  # +
                self.tosreg = self.tosreg + self.data_stack.pop()

            elif self.ir == 0x03:  # -
                self.tosreg = self.data_stack.pop() - self.tosreg

            elif self.ir == 0x04:  # *
                self.return_stack.append((self.tosreg * \
                    self.data_stack[-1]) & 0xff)
                self.return_stack.append((self.tosreg * \
                    self.data_stack.pop()) >> 8)
                self.data_stack.append(self.return_stack.pop())
                self.tosreg = self.return_stack.pop()

            elif self.ir == 0x05:  # / TODO
                self.return_stack.append((self.data_stack[-1] // \
                    self.tosreg) & 0xff)
                self.return_stack.append((self.data_stack.pop() // \
                    self.tosreg) >> 8)
                self.data_stack.append(self.return_stack.pop())
                self.tosreg = self.return_stack.pop()

            elif self.ir == 0x06:  # >R
                self.return_stack.append(self.tosreg)
                self.tosreg = self.data_stack.pop()

            elif self.ir == 0x07:  # @
                self.mar = self.tosreg
                self.tosreg = self.memory[self.mar]

            elif self.ir == 0x08:  # AND
                self.tosreg = self.tosreg & self.data_stack.pop()

            elif self.ir == 0x09:  # DROP
                self.tosreg = self.data_stack.pop()

            elif self.ir == 0x0A:  # DUP
                self.data_stack.append(self.tosreg)

            elif self.ir == 0x0B:  # OR
                self.tosreg = self.tosreg | self.data_stack.pop()

            elif self.ir == 0x0C:  # OVER
                self.return_stack.append(self.tosreg)
                self.tosreg = self.data_stack.pop()
                self.data_stack.append(self.tosreg)
                self.data_stack.append(self.return_stack.pop())

            elif self.ir == 0x0D:  # R>
                self.data_stack.append(self.tosreg)
                self.tosreg = self.return_stack.pop()

            elif self.ir == 0x0E:  # SHR
                self.tosreg = self.tosreg >> self.data_stack.pop()

            elif self.ir == 0x0F:  # SHL
                self.tosreg = self.tosreg << self.data_stack.pop()

            elif self.ir == 0x10:  # SWAP
                self.return_stack.append(self.tosreg)
                self.tosreg = self.data_stack.pop()
                self.data_stack.append(self.return_stack.pop())

            elif self.ir == 0x11:  # XOR
                self.tosreg = self.tosreg ^ self.data_stack.pop()

            elif self.ir == 0x12:  # [IF]
                if self.tosreg == 0:
                    self.mar = self.pc
                    self.pc = self.memory[self.mar]  # lo
                    self.mar += 1 
                    self.pc += self.memory[self.mar] << 8  # hi
                else:
                    self.pc += 2
                self.tosreg = self.data_stack.pop()

            elif self.ir == 0x13:  # [CALL]
                self.return_stack.append(self.pc + 2)
                self.mar = self.pc
                self.pc = self.memory[self.mar]
                self.mar += 1 
                self.pc += self.memory[self.mar] << 8  # hi

            elif self.ir == 0x14:  # [EXIT]
                self.pc = self.return_stack.pop()

            elif self.ir == 0x15:  # [LIT]
                self.mar = self.pc
                self.data_stack.append(self.tosreg)
                self.tosreg = self.memory[self.mar] # lo
                self.mar += 1 
                self.tosreg += self.memory[self.mar] << 8  # hi
                self.pc += 2

            elif self.ir == 0x16:  # [SYS]
                self._syscall()

            elif self.ir == 0x17:  # [NOP]
                continue

            else:
                raise ValueError('Unknown instruction at PC' + \
                    ' 0x{:04x}'.format(self.pc-1))
        
            # Fetch next instruction
            self.mar = self.pc
            self.ir = self.memory[self.mar]
            self.pc += 1

        if debug:
            self._print_debug()
            # TODO input()


    def _syscall(self):
        if self.tosreg == 0x1:    # print number from stack
            print("{}".format(self.data_stack.pop()))
        elif self.tosreg == 0x2:  # print string
            self.tosreg = self.data_stack.pop()
            self.mar = self.data_stack.pop()
            count = 0
            for i in range(0, self.tosreg):
                print(chr(self.memory[self.mar + i]), end='')
                count += 1
            self.tosreg = count
        elif self.tosreg == 0x3:  # read int to stack
            get_line = input()
            self.tosreg = int(get_line)
        elif self.tosreg == 0x4:  # read string
            get_line = input()
            self.tosreg = self.data_stack.pop()
            self.mar = self.data_stack.pop()
            for i in range(0, self.tosreg):
                if i >= len(get_line):
                    self.memory[self.mar + i] = 0x0
                else:
                    self.memory[self.mar + i] = ord(get_line[i])
        elif self.tosreg == 0x5:  # open
            pass
        elif self.tosreg == 0x6:  # file_read
            pass
        elif self.tosreg == 0x7:  # file_write
            pass
        else:
            self.tosreg = 0x0  # error code

    def _print_debug(self):
        # we need to subtract because we inc pc before entering the loop 
        print("PC: 0x{:04x} -------".format(self.pc - 1), file=sys.stderr)
        print("Data Stack:", file=sys.stderr)
        print('    0x{:04x}'.format(self.tosreg), file=sys.stderr)
        for elem in reversed(self.data_stack):
            print('    0x{:04x}'.format(elem), file=sys.stderr)
        print(file=sys.stderr)
        print('Return Stack:', file=sys.stderr)
        for elem in reversed(self.return_stack):
            print('    0x{:04x}'.format(elem), file=sys.stderr)
        print(file=sys.stderr)
        print('------------------', file=sys.stderr)
        print(file=sys.stderr)



