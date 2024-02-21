GOTO = """
0 1: OPC = PC - 1
1 2: PC = PC + 1; fetch
1 3: H = MBR << 8
1 4: H = MBR OR H
1 5: PC = OPC + H; fetch
1 6: goto Main1
"""

WIDE = """
0 1: PC = PC + 1; fetch
0 2: goto MBR OR 0x00 1 1
"""

INVOKEVIRTUAL = """
0 1: PC = PC + 1; fetch
1 2: H = MBRU << 8
1 3: H = MBRU OR H
1 4: MAR = CPP + H; rd
1 5: OPC = PC + 1
1 6: PC = MDR; fetch
1 7: PC = PC + 1; fetch
1 8: H = MBRU << 8
1 9: H = MBRU OR H
1 10: PC = PC + 1; fetch
1 11: TOS = SP - H
1 12: TOS = MAR = TOS + 1
1 13: PC = PC + 1; fetch
1 14: H = MBRU << 8
1 15: H = MBRU OR H
1 16: MDR = SP + H + 1; wr
1 17: MAR = SP = MDR
1 18: MDR = OPC; wr
1 19: MAR = SP = SP + 1
1 20: MDR = LV; wr
1 21: PC = PC + 1; fetch
1 22: LV = TOS; goto Main1
"""

IRETURN = """
0 1: MAR = SP = LV; rd
1 2: 
1 3: LV = MAR = MDR; rd
1 4: MAR = LV + 1
1 5: PC = MDR; rd; fetch
1 6: MAR = SP
1 7: LV = MDR
1 8: MDR = TOS; wr; goto Main1
"""

LDC_W1 = """
0 1: PC = PC + 1; fetch
0 2: H = MBRU << 8
1 1: H = MBRU OR H
1 2: MAR = H + CPP; rd; goto 0x15 0 3
"""

OUT = """
0 1: MAR = -1
0 2: MDR = TOS; wr
0 3: MAR = SP = SP - 1; rd
0 4: 
0 5: TOS = MDR; goto Main1
"""

IN = """
0 1: MAR = -1; rd
0 2: MAR = SP = SP + 1
0 3: TOS = MDR; wr
"""

ERR = """
0 1: MAR = -1
0 2: MDR = -1; wr; goto 0xFF 0 1
"""

# 0xA5
T = """
0 1: OPC = PC - 1; goto 0xA7 1 2
"""

# 0xA5
F = """
1 1: PC = PC + 1
1 2: PC = PC + 1; fetch
1 3: goto Main1
"""

IFEQ = """
0 1: MAR = SP = SP - 1; rd
0 2: OPC = TOS
1 3: TOS = MDR
1 4: OPC; ifeq; goto 0xA5 0 1
"""

IFLT = """
0 1: MAR = SP = SP - 1; rd
0 2: OPC = TOS
1 3: TOS = MDR
1 4: OPC; iflt; goto 0xA5 0 1
"""

IF_ICMPEQ = """
0 1: MAR = SP = SP - 1; rd
0 2: MAR = SP = SP - 1
0 3: H = MDR; rd
0 4: OPC = TOS
1 5: TOS = MDR
1 6: OPC - H; ifeq; goto 0xA5 0 1
"""

ISTORE = """
0 1: H = LV
0 2: MAR = MBRU + H;
0 3: MDR = TOS; wr
0 4: SP = MAR = SP - 1; rd
0 5: PC = PC + 1; fetch
0 6: TOS = MDR; goto Main1
"""

TMP = """
0 0: H = MBRU << 8
0 3:
"""


INPUT = TMP
PROGRAM_START = 0xF3

LINE_NAMES = {"Main1": "100000000"}

print(f"Find starting address at {PROGRAM_START // 64 * 64} | {PROGRAM_START % 64}")


from mutable_string import MutableString

B_BUS_INDEX = {
    "MDR": 0,
    "PC": 1,
    "MBR": 2,
    "MBRU": 3,
    "SP": 4,
    "LV": 5,
    "CPP": 6,
    "TOS": 7,
    "OPC": 8,
}

C_BUS_INDEX = {
    "H": 0,
    "OPC": 1,
    "TOS": 2,
    "CPP": 3,
    "LV": 4,
    "SP": 5,
    "PC": 6,
    "MDR": 7,
    "MAR": 8,
}


# #        ADDRESS
# print("1 0000 0110".replace(" ", ""), end="")

# # JUMP:   C N Z
# print("0 0 0".replace(" ", ""), end="")

# # SHIFTER: L8 R1
# print("0  0".replace(" ", ""), end="")
# # ALU:  F0 F1 ENA ENB INVA INC
# print("0  1  0   1   0    0".replace(" ", ""), end="")

# # C:   H   OPC TOS CPP LV  SP  PC  MDR MAR
# print("1   0   0   0   0   0   0   0   0   ".replace(" ", ""), end="")

# # Mem: WRITE READ FETCH
# print("0     0    0    ".replace(" ", ""), end="")

# # B
# print(f"{B_BUS_INDEX['MDR']:04b}")
# # 0 - MDR;
# # 1 - PC;
# # 2 - MBR;
# # 3 - MBRU;
# # 4 - SP;
# # 5 - LV;
# # 6 - CPP;
# # 7 - TOS;
# # 8 - OPC;


S8LL = 0
S1RA = 1
F0 = 2
F1 = 3
ENA = 4
ENB = 5
INVA = 6
INC = 7


INPUT = INPUT.strip()


index = 0

lines: list[str] = INPUT.splitlines()

from thelittlethings import EList

lines = EList(lines)

for line in lines:
    if line.strip() == "":
        lines.remove(line)


for i in range(len(lines)):

    line = lines[i]

    address = MutableString("000000000")

    jam = MutableString("000")

    alu = MutableString("00000000")

    c_bus = MutableString("000000000")

    mem = MutableString("000")

    b_bus = "0000"

    number, content = line.split(":")

    if i < len(lines) - 1:
        next_number, _ = lines[i + 1].split(":")
        parts = next_number.split(" ")
        address.string = f"{int(parts[0])}{int(parts[1]) - 1 + PROGRAM_START:08b}"

    components = content.split(";")
    for comp in components:
        comp = comp.strip()
        if "=" in comp:
            parts = comp.split("=")
            expr = parts[-1]

            tokens = expr.split(" ")
            tokens.remove("")

            current = 0

            # Match for an addition of H and another B-bus register

            can_add_1 = False

            for token in tokens:
                if token in B_BUS_INDEX:
                    b_bus = f"{B_BUS_INDEX[token]:04b}"
                    break

            if len(tokens) >= 3 and tokens[1] == "+":
                if tokens[0] in B_BUS_INDEX and tokens[2] == "H":
                    alu[F0] = "1"
                    alu[F1] = "1"
                    alu[ENA] = "1"
                    alu[ENB] = "1"
                    can_add_1 = True
                    current = 3
            if current == 0 and len(tokens) >= 3 and tokens[1] == "-":
                if tokens[0] in B_BUS_INDEX and tokens[2] == "H":
                    alu[F0] = "1"
                    alu[F1] = "1"
                    alu[ENA] = "1"
                    alu[ENB] = "1"
                    alu[INC] = "1"
                    alu[INVA] = "1"
                    current = 3
                elif tokens[0] in B_BUS_INDEX and tokens[2] == "1":
                    alu[F0] = "1"
                    alu[F1] = "1"
                    alu[ENB] = "1"
                    alu[INVA] = "1"
                    current = 3
            if current == 0 and len(tokens) >= 3 and tokens[1] == "AND":
                if tokens[0] in B_BUS_INDEX and tokens[2] == "H":
                    alu[ENA] = "1"
                    alu[ENB] = "1"
                    current = 3
            if current == 0 and len(tokens) >= 3 and tokens[1] == "OR":
                if tokens[0] in B_BUS_INDEX and tokens[2] == "H":
                    alu[F1] = "1"
                    alu[ENA] = "1"
                    alu[ENB] = "1"
                    current = 3
            if (
                current == 0
                and len(tokens) >= 2
                and tokens[0] == "NOT"
                and tokens[1] == "H"
            ):
                alu[F1] = "1"
                alu[ENA] = "1"
                alu[INVA] = "1"
                current = 2
            if (
                current == 0
                and len(tokens) >= 2
                and tokens[0] == "NOT"
                and tokens[1] in B_BUS_INDEX
            ):
                b_bus = f"{B_BUS_INDEX[tokens[1]]:04b}"
                alu[F0] = "1"
                alu[ENB] = "1"
                current = 2
            if current == 0 and tokens[0] == "-H":
                alu[F0] = "1"
                alu[F1] = "1"
                alu[ENA] = "1"
                alu[INC] = "1"
                alu[INVA] = "1"
                current = 2
            if current == 0 and tokens[0] == "H":
                alu[F1] = "1"
                alu[ENA] = "1"
                can_add_1 = True
                current = 1
            if current == 0 and tokens[0] in B_BUS_INDEX:
                alu[F1] = "1"
                b_bus = f"{B_BUS_INDEX[tokens[0]]:04b}"
                alu[ENB] = "1"
                can_add_1 = True
                current = 1
            if current == 0 and tokens[0] == "1":
                alu[F0] = "1"
                alu[F1] = "1"
                alu[INC] = "1"
                current = 1
            if current == 0 and tokens[0] == "0":
                alu[F0] = "1"
                alu[F1] = "1"
                current = 1
            if current == 0 and tokens[0] == "-1":
                alu[F0] = "1"
                alu[F1] = "1"
                alu[INVA] = "1"
                current = 1

            if can_add_1 and len(tokens[current:]) >= 2 and tokens[current] == "+":
                if tokens[current + 1] == "1":
                    alu[F0] = "1"
                    alu[F1] = "1"
                    alu[INC] = "1"
                    current += 2

            if (
                len(tokens[current:]) >= 2
                and tokens[current] == "<<"
                and tokens[current + 1] == "8"
            ):
                print(tokens[current:])
                alu[S8LL] = "1"
                current += 2
            if (
                len(tokens[current:]) >= 2
                and tokens[current] == ">>"
                and tokens[current + 1] == "1"
            ):
                alu[S1RA] = "1"
                current += 2

            to_be_assigned = parts[:-1]
            for token in to_be_assigned:
                c_bus[C_BUS_INDEX[token.strip()]] = "1"

        if "-" in comp:
            parts = comp.split("-")
            if parts[0].strip() in B_BUS_INDEX and parts[1].strip() == "H":
                alu[F0] = "1"
                alu[F1] = "1"
                alu[ENA] = "1"
                alu[ENB] = "1"
                alu[INC] = "1"
                alu[INVA] = "1"

        if comp in B_BUS_INDEX:
            b_bus = f"{B_BUS_INDEX[comp]:04b}"
            alu[F1] = "1"
            alu[ENB] = "1"

        if comp == "wr":
            mem[0] = "1"
        if comp == "rd":
            mem[1] = "1"
        if comp == "fetch":
            mem[2] = "1"

        if comp == "iflt":
            jam[2] = "1"
        if comp == "ifeq":
            jam[3] = "1"

        if comp.startswith("goto"):
            parts = comp.split(" ")
            if parts[1] in LINE_NAMES:
                address.string = LINE_NAMES[parts[1]]
            elif parts[1] == "MBR":
                jam[0] = "1"
                if len(parts) == 6 and parts[2] == "OR":
                    if parts[3].startswith("0b"):
                        address.string = f"{parts[3][2:] :>09}"
                    elif parts[3].startswith("0x"):
                        base_address = int(parts[3][2:], 16)
                        address.string = f"{int(parts[4])}{int(parts[5]) - 1 + base_address:08b}"                
                    else:
                        address.string = f"{int(parts[3])}{int(parts[4]) - 1 + PROGRAM_START:08b}"
            elif parts[1].startswith("0b"):
                address.string = f"{parts[1][2:] :>09}"
            elif parts[1].startswith("0x"):
                base_address = int(parts[1][2:], 16)
                address.string = f"{int(parts[2])}{int(parts[3]) - 1 + base_address:08b}"                
            else:
                address.string = f"{int(parts[1])}{int(parts[2]) - 1 + PROGRAM_START:08b}"

    print(f"{i+1} 0b{address}{jam}{alu}{c_bus}{mem}{b_bus}")
