class Token:
    def __init__(self):
        self.token_type = ''
        self.value = None
        self.label = ''

class Tokenizer:
    INSTR_OPCODES = {
        '!' : 0x01,
        '+' : 0x02,
        '-' : 0x03,
        '*' : 0x04,
        '/' : 0x05,
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

    def get_tokens(self, string)
        lines = string.split('\n')
        
        if lines[0] is '.data':
            pass # TODO

        label = None  # last found label
        labels = {}  # for keeping track of labels


        for pos, val in enumerate(lines):
            instr = val.split('\t').pop()  # remove tabs
            if instr[-1] is ':':  # label
                if label is not None:
                    raise ValueError('label {} at line {} shadows \
                        label {} at line {}'.format(label,
                        pos-1, instr[-1], pos))
                label = instr[:-1]
            elif instr in INSTR_OPCODES:
                new_token = Token()
                new_token.token_type = instr 
                new_token.value = INSTR_OPCODES[instr]

                if label is not None:
                    new_token.label = label
                    labels[label] = new_token
                    label = None
                    
                self.tokens.append(new_token)
            elif len(self.tokens) > 0 and self.tokens[-1].token_type \
                is '[LIT]':  # literal 
                try:
                    new_token = Token()
                    new_token.token_type = "int"
                    new_token.value = int(instr)
                    new_token.label = label
                    self.tokens.append(new_token)
                except ValueError:
                    raise ValueError('undefined literal {} at line \
                        {}'.format(val, pos))
            elif instr[0].isalpha():  # label
                new_token = Token()
                new_token.token_type = "reference"
                new_token.value = instr
                self.tokens.append(new_token)
            else:
                raise ValueError('undefined control sequence {} at \
                    line {}'.format(val, pos)

        return self.tokens










