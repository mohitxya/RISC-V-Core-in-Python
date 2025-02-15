#riscv_program.py
# RISC-V test program: Arithmetic and memory operations
program = [
    0x00000013,  # NOP
    0x00000513,  # ADDI x10, x0, 5
    0x00000693,  # ADDI x13, x0, 6
    0x00b50633,  # ADD x12, x10, x11
    0x00b00023,  # SW x11, 0(x12)
    0x00c52083,  # LW x1, 0(x10)
]
if __name__ == '__main__':
    from riscv_emulator import RiscVEmulator
    emulator = RiscVEmulator()
    emulator.load_program(program)
    emulator.run()
    # Check results
    print(f'Register x12 (should be 11): {emulator.registers[12]}')
    print(f'Register x1 (loaded from memory): {emulator.registers[1]}')
