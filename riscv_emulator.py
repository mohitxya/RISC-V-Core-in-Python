OPCODES = {
    'LUI': 0b0110111,
    'AUIPC': 0b0010111,
    'JAL': 0b1101111,
    'JALR': 0b1100111,
    'BRANCH': 0b1100011,
    'LOAD': 0b0000011,
    'STORE': 0b0100011,
    'ALU_IMM': 0b0010011,
    'ALU_REG': 0b0110011,
}

FUNCT3_CODES = {
    'ADD_SUB': 0b000,
    'SLL': 0b001,
    'SLT': 0b010,
    'SLTU': 0b011,
    'XOR': 0b100,
    'SRL_SRA': 0b101,
    'OR': 0b110,
    'AND': 0b111,
}

FP_OPCODES = {
    'FADD_S': 0b1010011,
    'FSUB_S': 0b1010011,
    'FMUL_S': 0b1010011,
    'FDIV_S': 0b1010011,
}


class RiscVEmulator:
    def __init__(self, memory_size=1024):
        self.registers = [0] * 32
        self.f_registers = [0.0] * 32
        self.pc = 0
        self.memory = [0] * memory_size

    def load_program(self, program):
        address = 0
        for instr in program:
            self.memory[address] = instr & 0xFF
            self.memory[address + 1] = (instr >> 8) & 0xFF
            self.memory[address + 2] = (instr >> 16) & 0xFF
            self.memory[address + 3] = (instr >> 24) & 0xFF
            address += 4

    def fetch(self):
        addr = self.pc
        if addr + 3 >= len(self.memory):
            raise IndexError("PC out of bounds")
        instruction = (self.memory[addr] |
                       (self.memory[addr + 1] << 8) |
                       (self.memory[addr + 2] << 16) |
                       (self.memory[addr + 3] << 24))
        self.pc += 4
        return instruction

    def decode(self, instruction):
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x07
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        imm = 0

        if opcode in [OPCODES['LUI'], OPCODES['AUIPC']]:
            imm = instruction & 0xFFFFF000
        elif opcode == OPCODES['JAL']:
            imm = ((instruction >> 31) << 20) | ((instruction >> 21) << 1) | ((instruction >> 20) << 11) | ((instruction >> 12) << 12)
            imm = self.sign_extend(imm, 20)
        elif opcode in [OPCODES['JALR'], OPCODES['LOAD'], OPCODES['ALU_IMM']]:
            imm = instruction >> 20
            imm = self.sign_extend(imm, 12)
        elif opcode == OPCODES['STORE']:
            imm = ((instruction >> 25) << 5) | ((instruction >> 7) & 0x1F)
            imm = self.sign_extend(imm, 12)
        elif opcode == OPCODES['BRANCH']:
            imm = ((instruction >> 31) << 12) | ((instruction >> 25) << 5) | ((instruction >> 8) << 1) | ((instruction >> 7) << 11)
            imm = self.sign_extend(imm, 12)
        else:
            imm = instruction >> 20

        return opcode, rd, funct3, rs1, rs2, funct7, imm

    def sign_extend(self, value, bits):
        sign_bit = 1 << (bits - 1)
        return (value & (sign_bit - 1)) - (value & sign_bit)

    def execute(self, opcode, rd, funct3, rs1, rs2, funct7, imm):
        if opcode == OPCODES['LUI']:
            self.registers[rd] = imm
        elif opcode == OPCODES['AUIPC']:
            self.registers[rd] = self.pc + imm
            self.pc = self.registers[rd]
        elif opcode == OPCODES['JAL']:
            self.registers[rd] = self.pc
            self.pc += imm
        elif opcode == OPCODES['ALU_IMM']:
            if funct3 == FUNCT3_CODES['ADD_SUB']:
                self.registers[rd] = self.registers[rs1] + imm
        elif opcode == OPCODES['ALU_REG']:
            if funct3 == FUNCT3_CODES['ADD_SUB']:
                if funct7 == 0b0000000:
                    self.registers[rd] = self.registers[rs1] + self.registers[rs2]
                elif funct7 == 0b0100000:
                    self.registers[rd] = self.registers[rs1] - self.registers[rs2]
        elif opcode == OPCODES['LOAD']:
            if funct3 == 0b010:
                address = self.registers[rs1] + imm
                value = self.read_memory(address, 4)
                if value & 0x80000000:
                    value -= 0x100000000
                self.registers[rd] = value
        elif opcode == OPCODES['STORE']:
            if funct3 == 0b010:
                address = self.registers[rs1] + imm
                self.write_memory(address, self.registers[rs2], 4)
        elif opcode == OPCODES['BRANCH']:
            offset = imm
            if funct3 == 0b000:  # BEQ
                if self.registers[rs1] == self.registers[rs2]:
                    self.pc += offset - 4  # Subtract 4 because PC already incremented by 4
            elif funct3 == 0b001:  # BNE
                if self.registers[rs1] != self.registers[rs2]:
                    self.pc += offset - 4

    def read_memory(self, address, size):
        value = 0
        for i in range(size):
            value |= self.memory[address + i] << (i * 8)
        return value

    def write_memory(self, address, value, size):
        for i in range(size):
            self.memory[address + i] = (value >> (i * 8)) & 0xFF

    def run(self):
        while self.pc < len(self.memory):
            instruction = self.fetch()
            if instruction == 0x00000013:  # NOP
                continue
            opcode, rd, funct3, rs1, rs2, funct7, imm = self.decode(instruction)
            self.execute(opcode, rd, funct3, rs1, rs2, funct7, imm)


# Correct test program

