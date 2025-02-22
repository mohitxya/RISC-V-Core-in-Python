from mpipe import OrderedStage, Pipeline

OPCODES ={'LUI': 0b0110111,
    'AUIPC': 0b0010111,
    'JAL': 0b1101111,
    'JALR': 0b1100111,
    'BRANCH': 0b1100011,
    'LOAD': 0b0000011,
    'STORE': 0b0100011,
    'ALU_IMM': 0b0010011,
    'ALU_REG': 0b0110011,
}

FUNCT3_CODES={'ADD_SUB': 0b000,
    'SLL': 0b001,
    'SLT': 0b010,
    'SLTU': 0b011,
    'XOR': 0b100,
    'SRL_SRA': 0b101,
    'OR': 0b110,
    'AND': 0b111,
}

FP_OPCODES = {
    'FADD_S': 0b1010011,  # Floating-point add single-precision
    'FSUB_S': 0b1010011,  # Floating-point subtract single-precision
    'FMUL_S': 0b1010011,  # Floating-point multiply single-precision
    'FDIV_S': 0b1010011,  # Floating-point divide single-precision
}


class RiscVEmulator:
    def __init__(self,memory_size=1024):
        self.registers=[0]*32
        self.f_registers=[0.0]*32
        self.pc=0
        self.memory=[0]*memory_size

    def load_program(self,program):
        self.memory[:len(program)]=program
    def fetch(self):
        instruction=self.memory[self.pc]
        self.pc+=1
        return instruction
    def decode(self,instruction):
        opcode=instruction & 0x7F
        rd=(instruction>>7) & 0x1F
        funct3=(instruction>>12)& 0x07
        rs1=(instruction>>15)& 0x1F
        rs2=(instruction>>20) & 0x1F
        funct7=(instruction>>25) & 0x7F
        imm = instruction>>20
        return opcode, rd, funct3, rs1, rs2, funct7, imm
        
    def execute(self,opcode,rd,funct3,rs1,rs2,funct7, imm):
        if opcode==OPCODES['LUI']:
            # used to load a 20-bit immediate value into the upper 20 bits of a destination # register, while setting the lower 12 bits to zero. 
            # load upper intermediate.
            self.registers[rd]=imm<<12
        elif opcode==OPCODES['AUIPC']:
            self.pc+= self.pc + (imm<<12)
            # add upper intermediate to PC. 
        elif opcode==OPCODES['JAL']:
            self.registers[rd]=self.pc
            self.pc+=imm
        elif opcode==OPCODES['ALU_IMM']:
            if funct3==FUNCT3_CODES['ADD_SUB']:
                self.registers[rd]=self.registers[rs1]+imm

            # could add more ALU operations
        elif opcode==OPCODES['ALU_REG']:
            if funct3==FUNCT3_CODES['ADD_SUB']:
                if funct7==0b0000000:
                    self.registers[rd]=self.registers[rs1]+self.registers[rs2]
                elif funct7==0b0100000:
                    self.registers[rd]=self.registers[rs1]-self.registers[rs2]
        elif opcode==OPCODES['LOAD']:
            if funct3==0b010:
                self.registers[rd]=self.read_memory(self.registers[rs1] + imm, 4)
        elif opcode==OPCODES['STORE']:
            if funct3==0b010:
                self.write_memory(self.registers[rs1] + imm, self.registers[rs2],4)
        elif opcode==OPCODES['BRANCH']:
            offset=(imm<<1)
            if funct3==0b000: #BEQ
                if self.registers[rs1]==self.registers[rs2]:
                    self.pc+=offset
            elif funct3 == 0b001: #BNE
                if self.registers[rs1] != self.registers[rs2]:
                    self.pc+=offset
        elif opcode == OPCODES['ALU_REG']:
            if funct3 == 0b000 and funct7 == 0b0000001:
                self.registers[rd] = self.registers[rs1] * self.registers[rs2]
            elif funct3 == 0b000 and funct7 == 0b0000001:
                self.registers[rd] = self.registers[rs1] // self.registers[rs2]
    def execute_fp(self, opcode, rd, fucnt3, rs1, rs2, funct7, imm):
        if opcode == FP_OPCODES['FADD_S']:
            self.f_registers[rd] = self.f_registers[rs1] + self.f_registers[rs2]
        elif opcode == FP_OPCODES['FSUB_S']:
            self.f_registers[rd] = self.f_registers[rs1] - self.f_registers[rs2]
        # Add more floating-point operations (FMUL_S, FDIV_S) as needed...
    def read_memory(self, address, size):
        value=0
        for i in range(size):
            value |=self.memory[address + i]<<(i*8)
        return value
    def write_memory(self,address, value, size):
        for i in range(size):
            self.memory[address+i]=(value>>(i*8))&0xFF
    def simulate_pipeline():
    # Instruction Fetch (IF), Instruction Decode (ID), Execute (EX), Memory Access (MEM), Write-Back (WB)
        pipeline_stages = ['IF', 'ID', 'EX', 'MEM', 'WB']
        for stage in pipeline_stages:
            print(f"Executing stage: {stage}")
    def jit_compile(instruction):
        pass
    def branch_prediction():
        pass
    def run(self):
        while self.pc < len(self.memory):  # Ensure we don’t read beyond memory
            instruction = self.fetch()  # Step 1: Fetch instruction
            if instruction == 0x00000013:  # Halt on NOP (optional)
                continue
            opcode, rd, funct3, rs1, rs2, funct7, imm = self.decode(instruction)  # Step 2: Decode
            self.execute(opcode, rd, funct3, rs1, rs2, funct7, imm)  # Step 3: Execute


