from assembler import *
from runtime import *

def main():
    with open('examples/rpn.s') as f:
        string = f.read()

    tk = Tokenizer()
    (tokens, labels) = tk.get_tokens(string)

    asm = Assembler(tokens, labels)
    output = asm.emit_assembly()
    # hexdump
    print('Hexdump ---------------------')
    for i, _ in enumerate(output):
        if i % 8 == 0:
            print('{:04x}: '.format(0x600 + i), end='')
        byte = output[i]
        print('{:02x}'.format(byte), end=' ')
        if i % 8 == 7 or i == len(output) - 1:
            print()
    print('-----------------------------')

    print()
    vsm = VirtualStackMachine(bytes(output))
    vsm.run(True)




if __name__ == '__main__':
    main()
