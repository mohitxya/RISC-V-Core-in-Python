#riscv_program.py
# RISC-V test program: Arithmetic and memory operations
'''program = [
    0x00000013,  # NOP
    0x00000513,  # ADDI x10, x0, 5
    0x00000693,  # ADDI x13, x0, 6
    0x00b50633,  # ADD x12, x10, x11
    0x00b00023,  # SW x11, 0(x12)
    0x00c52083,  # LW x1, 0(x10)
]
program = [
    0x00000013,  # NOP
    0x00500513,  # ADDI x10, x0, 5
    0x00600693,  # ADDI x13, x0, 6
    0x00d50633,  # ADD x12, x10, x13
   # 0x00d62023,  # SW x13, 0(x12)
   # 0x00d52223, # new addition to test memory
    0x00052683,  # LW x13, 0(x10)
]'''
program=[0x00000013,  # NOP
    0x00500513,  # ADDI x10, x0, 5    (x10 = 5)
    0x00600693,  # ADDI x13, x0, 6    (x13 = 6)
    0x00d50633,  # ADD x12, x10, x13  (x12 = x10 + x13 = 11)
    0x00d62023,  # SW x13, 0(x12)     (Store 6 at address 11)
    0x00d52223,  # SW x13, 4(x10)     (Store 6 at address 9)
    0x00d52423,  # SW x13, 4(x10)     (Store 6 at address 4, ALIGNED)
    0x00452683,   # LW x13, 4(x10)     (Load from address 4 into x13, ALIGNED)
]
program2=[0x00500513,  # ADDI x10, x0, 5    (x10 = 5)
    0x00300693,  # ADDI x13, x0, 3    (x13 = 3)
    0x00D50633,  # ADD x12, x10, x13  (x12 = x10 + x13 = 5 + 3 = 8)
    0x00D506B3,  # SUB x13, x10, x13  (x13 = x10 - x13 = 5 - 3 = 2)
    0x00C6A263,  # BEQ x13, x12, 4    (if x13 == x12, skip next instruction)
    0x00150513,   
]
if __name__ == '__main__':
    from riscv_emulator_v1 import RiscVEmulator
    emulator = RiscVEmulator()
    emulator.load_program(program)
    emulator.run()
    # Check results
    print(f'Register x12 (should be 11): {emulator.registers[12]}')
    print(f'Register x13 (loaded from memory): {emulator.registers[13]}')
    print(f'Register x10: {emulator.registers[10]}')
