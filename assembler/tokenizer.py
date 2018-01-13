class Token:
    def __init__(self):
        self.token_type = ''
        self.value = None
        self.line = 0
        self.label = ''
        self.addr = 0x0

    def __repr__(self):
        return ("{} <{}> @ 0x{:04x}").format(self.token_type,
            self.value, self.addr)

class Tokenizer:
    INSTR_OPCODES = {
        '.' : 0x00,
        '!' : 0x01,
        '+' : 0x02,
        '-' : 0x03,
        '+C' : 0x04,
        '-C' : 0x05,
        '>R' : 0x06,
        '@' : 0x07,
        'AND' : 0x08,
        'DROP' : 0x09,
        'DUP' : 0x0A,
        'OR' : 0x0B,
        'OVER' : 0x0C,
        'R>' : 0x0D,
        'SHR' : 0x0E,
        'SHL' : 0x0F,
        'SWAP' : 0x10,
        'XOR' : 0x11,
        '[IF]' : 0x12,
        '[CALL]' : 0x13,
        '[EXIT]' : 0x14,
        '[LIT]' : 0x15,
        '[SYS]' : 0x16,
        '[NOP]' : 0x17
    }

    def __init__(self):
        self.tokens = []
        self.labels = {}  # for keeping track of labels

    def get_tokens(self, string):
        lines = string.split('\n')
        
        if lines[0] is '.data':
            pass # TODO

        label = None  # last found label
        pc = 0x0600


        for pos, val in enumerate(lines):
            instr = val.lstrip() # remove tabs
            instr = instr.split('#')[0]
            instr = instr.rstrip(' \t')
            if len(instr) == 0 or instr[0] == '#':
                continue

            if instr[-1] == ':':  # label
                if label is not None:
                    raise ValueError('label {} at line {} shadows \
                        label {} at line {}'.format(label,
                        pos, instr[-1], pos+1))
                label = instr[:-1]
            elif instr in self.INSTR_OPCODES:
                new_token = Token()
                new_token.token_type = instr 
                new_token.value = self.INSTR_OPCODES[instr]
                new_token.line = pos + 1
                new_token.addr = pc
                pc += 1

                if label is not None:
                    new_token.label = label
                    self.labels[label] = new_token
                    label = None
                    
                self.tokens.append(new_token)
            elif instr[0].isalpha():  # label
                new_token = Token()
                new_token.token_type = "Reference"
                new_token.value = instr
                new_token.line = pos + 1
                new_token.addr = pc
                pc += 2  # addresses are 16-bit
                self.tokens.append(new_token)
            elif len(self.tokens) > 0 and self.tokens[-1].token_type \
                == '[LIT]':  # literal 
                new_token = Token()
                new_token.label = label
                new_token.line = pos + 1
                try:
                    new_token.value = int(instr)
                    new_token.token_type = "IntLiteral"
                except ValueError:
                    try:
                        new_token.value = int(instr, base=16)
                        new_token.token_type = "HexLiteral"
                    except ValueError:
                        raise ValueError('undefined literal {} at line \
                            {}'.format(instr, pos+1))
                # TODO: check size of int and update, also negative #s
                new_token.addr = pc
                pc += 2
                self.tokens.append(new_token)
            else:
                raise ValueError('undefined control sequence {} at line {}'
                        .format(instr, pos+1))

        return (self.tokens, self.labels)










