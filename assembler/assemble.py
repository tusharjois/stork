class Assembler:
    def __init__(self, tokens, labels):
        self.tokens = tokens
        self.labels = labels
        self.pc = 0x0600  # starting program counter of vsm
        self.to_emit = []

    def _index_labels(self):
        pass

    def emit_assembly(self):
        for token in self.tokens:  # TODO: data
            if token.token_type == 'IntLiteral' or \
                token.token_type == 'HexLiteral':
                self.to_emit.append(token.value & 0xff)  # lo
                self.to_emit.append(token.value >> 8)  # hi
                self.pc += 2
            elif token.token_type == 'Reference':
                try:
                    ref_token = self.labels[token.value]
                    self.to_emit.append(ref_token.addr & 0xff)  # lo
                    self.to_emit.append(ref_token.addr >> 8)  # hi
                    self.pc += 2
                except KeyError:
                    raise ValueError('Undefined label {} at line \
                        {}'.format(token.value, token.line))
            else:
                self.to_emit.append(token.value)
                self.pc += 1

        return self.to_emit

    def write_to_file(self, file_name):
        result = emit_assembly()
        with open(file_name, 'wb') as f:
            f.write(bytes(result))

