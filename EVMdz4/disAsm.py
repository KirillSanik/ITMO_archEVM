import sys

def readBitsLE(cntB):
    global currPos
    numRes = 0
    cnt = 0
    for i in range(currPos, currPos + cntB):
        numRes = numRes + bites[i]*16**(cnt)
        cnt = cnt + 2
    currPos = currPos + cntB
    return numRes

def readBitsBE(cntB):
    global currPos
    numRes = 0
    cnt = 2 * (cntB - 1)
    for i in range(currPos, currPos + cntB):
        numRes = numRes + bites[i]*16**(cnt)
        cnt = cnt - 2
    currPos = currPos + cntB
    return numRes

def DecToHex(num, size):
    return "0x" + hex(num)[2:].rjust(size * 2, "0").upper()

def printF(text):
    print(text.ljust(20), end = "")
    return

def endL():
    print()
    return

eiClass = 0
eiData = 0
eType = 0
eEntry = 0
indProgHead = 0
indSecHead = 0
singleSizeProg = 0
cntProgHead = 0
singleSizeSec = 0
cntSecHead = 0
indSHSTRNDX = 0

def parseHeader():

    global currPos
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead
    
    print("ELF header")
    print("----------")

    printF("Name")
    printF("Offset")
    printF("NumValue")
    printF("Value")
    endL()

    printF("EI_MAG")
    printF(DecToHex(currPos, 4))
    elfFile = DecToHex(readBitsBE(4), 4)
    if elfFile != "0x7F454C46":
        print("\n Данный файл не является ELF")
        exit(0)
    printF(elfFile)
    printF("ELF")
    endL()

    printF("EI_CLASS")
    printF(DecToHex(currPos, 4))
    eiClass = readBitsBE(1)
    printF(DecToHex(eiClass, 1))
    typeClass = ["NONE", "32 BIT", "64 BIT"]
    printF(typeClass[eiClass])
    endL()
    if eiClass != 1:
        print("Данный файл не является 32x битным")
        exit(0)
    
    printF("EI_DATA")
    printF(DecToHex(currPos, 4))
    eiData = readBitsBE(1)
    printF(DecToHex(eiData, 1))
    typeData = ["NONE", "Little-Endian", "Big-Endian"]
    printF(typeData[eiData])
    endL()
    if eiData != 1:
        print("\n Данный файл не является Little-Endian")
        exit(0)

    printF("EI_VERSION")
    printF(DecToHex(currPos, 4))
    printF(DecToHex(readBitsLE(1), 1))
    printF("EV_CURRENT")
    endL()

    printF("EI_OSABI")
    printF(DecToHex(currPos, 4))
    eiOsabi = readBitsLE(1)
    printF(DecToHex(eiOsabi, 1))
    typeOsabi = ["UNIX System V ", "HP-UX", "NetBSD", "GNU ELF", "Solaris",
                 "AIX", "IRIX", "FreeBSD", "Tru64 UNIX", "Modesto", "OpenBSD",
                 "OpenVMS", "Non-Stop Kernel", "Amiga Research OS", "FenixOS",
                 "CloudABI", "OpenVOS"]
    if eiOsabi > 17:
        printF("Uknown")
    else:
        printF(typeOsabi[eiOsabi])
    endL()

    printF("EI_OSABIVER")
    printF(DecToHex(currPos, 4))
    printF(DecToHex(readBitsLE(1), 1))
    endL()

    currPos = 16
    printF("E_TYPE")
    printF(DecToHex(currPos, 4))
    eType = readBitsLE(2)
    printF(DecToHex(eType, 2))
    typeE = ["ET_NONE", "ET_REL", "ET_EXEC", "ET_DYN", "ET_CORE"]
    if eType > 4:
        printF("Unknown")
    else:
        printF(typeE[eType])
    endL()

    printF("E_MACHINE")
    printF(DecToHex(currPos, 4))
    eMachine = readBitsLE(2)
    printF(DecToHex(eMachine, 2))
    if eMachine == 0xF3:
        printF("RISC-V")
    else:
        printF("Unknown")
    endL()

    printF("E_VERSION")
    printF(DecToHex(currPos, 4))
    eVer = readBitsLE(4)
    printF(DecToHex(eVer, 4))
    if eVer != 1:
        printF("NONE")
    else:
        printF("EV_Current")
    endL()

    printF("E_ENTRY")
    printF(DecToHex(currPos, 4))
    eEntry = readBitsLE(4)
    printF(DecToHex(eEntry, 4))
    endL()

    ## Где таблица загаловков программы Program header's offset
    printF("E_PHOFF")
    printF(DecToHex(currPos, 4))
    indProgHead = readBitsLE(4)
    printF(DecToHex(indProgHead, 4))
    endL()

    ## Где таблица загаловков cекций Section header's offset
    printF("E_SHOFF")
    printF(DecToHex(currPos, 4))
    indSecHead = readBitsLE(4)
    printF(DecToHex(indSecHead, 4))
    endL()

    printF("E_FLAGS")
    printF(DecToHex(currPos, 4))
    printF(DecToHex(readBitsLE(4), 4))
    endL()

    printF("E_EHSIZE")
    printF(DecToHex(currPos, 4))
    printF(DecToHex(readBitsLE(2), 2))
    endL()

    ## размер заголовка программы Size of program header
    printF("E_PHENTSIZE")
    printF(DecToHex(currPos, 4))
    singleSizeProg = readBitsLE(2)
    printF(DecToHex(singleSizeProg, 2))
    endL()

    ## количество заголовков программы Cnt of program header's
    printF("E_PHNUM")
    printF(DecToHex(currPos, 4))
    cntProgHead = readBitsLE(2)
    printF(DecToHex(cntProgHead, 2))
    endL()

    ## размер заголовка секции Size of section header
    printF("E_SHENTSIZE")
    printF(DecToHex(currPos, 4))
    singleSizeSec = readBitsLE(2)
    printF(DecToHex(singleSizeSec, 2))
    endL()

    ## количество заголовков секции Cnt of section header's
    printF("E_SHNUM")
    printF(DecToHex(currPos, 4))
    cntSecHead = readBitsLE(2)
    printF(DecToHex(cntSecHead, 2))
    endL()

    ## index of E_SHSTRNDX
    printF("E_SHSTRNDX")
    printF(DecToHex(currPos, 4))
    indSHSTRNDX = readBitsLE(2)
    printF(DecToHex(indSHSTRNDX, 2))
    endL()

    endL()
    return

indNames = 0
sizeNames = 0

def findSHRTAB():

    global currPos, indNames, sizeNames
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead

    currPos = indSecHead + indSHSTRNDX * singleSizeSec + 4 * 4
    indNames = readBitsLE(4)
    sizeNames = readBitsLE(4)

    return

def getName(num, indStart):

    global currPos, indNames, sizeNames
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead

    prevCurrPos = currPos
    currPos = indStart + num

    resStr = ""

    tempChar = readBitsLE(1)
    while tempChar != 0:
        resStr += chr(tempChar)
        tempChar = readBitsLE(1)

    currPos = prevCurrPos

    return resStr

indSymtab = 0
sizeSymtab = 0
indText = 0
sizeText = 0
indNamesSym = 0
addrText = 0

def parseSecHeader():

    global currPos, indNames, sizeNames, indSymtab, indText, sizeSymtab, sizeText
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX, indNamesSym
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead, addrText

    findSHRTAB()
    
    print("Section header table")
    print("--------------------")

    printF("Nr")
    printF("Name")
    printF("Type")
    printF("Offset")
    printF("Size")
    endL()

    for i in range(cntSecHead):
        currPos = indSecHead + i * singleSizeSec
        
        printF(str(i))
        
        sh_name = readBitsLE(4)
        name = getName(sh_name, indNames)
        printF(name)
        
        sh_type = readBitsLE(4)
        typeSh = ["SHT_NULL", "SHT_PROGBITS", "SHT_SYMTAB", "SHT_STRTAB", "SHT_RELA",
                  "SHT_HASH", "SHT_DYNAMIC", "SHT_NOTE", "SHT_NOBITS", "SHT_REL", "SHT_SHLIB",
                  "SHT_DYNSYM", "SHT_INIT_ARRAY", "SHT_FINI_ARRAY", "SHT_PREINIT_ARRAY",
                  "SHT_GROUP", "SHT_SYMTAB_SHNDX"]
        if sh_type > 18:
            printF("Unknown")
        else:
            printF(typeSh[sh_type])

        currPos = currPos + 4
        
        sh_addr = readBitsLE(4)
        sh_offset = readBitsLE(4)
        printF(DecToHex(sh_offset, 4))

        sh_size = readBitsLE(4)
        printF(DecToHex(sh_size, 4))
        endL()

        if name == ".text":
            indText = sh_offset
            sizeText = sh_size
            addrText = sh_addr

        if name == ".symtab":
            indSymtab = sh_offset
            sizeSymtab = sh_size

        if name == ".strtab":
            indNamesSym = sh_offset
            

    endL()
    return

namesOfCommand = {}

def parseSymtab():

    global currPos, indNames, sizeNames, indSymtab, indText, sizeSymtab, sizeText
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX, namesOfCommand
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead

    output.write(".symtab\n")

    output.write("Symbol ")
    output.write("Value".ljust(15))
    output.write("Size".rjust(6) + " ")
    output.write("Type".ljust(8) + " ")
    output.write("Bind".ljust(8) + " ")
    output.write("Vis".ljust(8) + " ")
    output.write("Index".rjust(6) + " ")
    output.write("Name\n")

    currPos = indSymtab

    for i in range(sizeSymtab//16):
        name = getName(readBitsLE(4), indNamesSym)
        value = readBitsLE(4)
        size = readBitsLE(4)     
        info = readBitsLE(1)
        vis = readBitsLE(1)
        index = readBitsLE(2)

        output.write("[" + str(i).rjust(4) + "] ")
        
        output.write(hex(value).ljust(15) + " ")

        output.write(str(size).rjust(6) + " ")

        infBind = info >> 4
        infType = (info) & (0xf)

        if infType == 2:
            namesOfCommand[value] = name
        
        numToBind = {
            0 : "LOCAL",
            1 : "GLOBAL",
            2 : "WEAK",
            10 : "LOOS",
            12 : "HIOS",
            13 : "LOPROC",
            15 : "HIPROC"
        }
        numToType = {
            0 : "NOTYPE",
            1 : "OBJECT",
            2 : "FUNC",
            3 : "SECTION",
            4 : "FILE",
            5 : "COMMON",
            6 : "TLS",
            10 : "LOOS",
            12 : "HIOS",
            13 : "LOPROC",
            15 : "HIPROC"
        }
        output.write(numToType[infType].ljust(8) + " ")
        output.write(numToBind[infBind].ljust(8) + " ")

        numToVis = ["DEFAULT", "INTERNAL", "HIDDEN", "PROTECTED"]
        output.write(numToVis[vis].ljust(8) + " ")
        
        numToInd = {
            0 : "UNDEF",
            0xff00 : "LORESERVE",
            0xff01 : "AFTER",
            0xff02 : "AMD64_LCOMMON",
            0xff1f : "HIPROC",
            0xff20 : "LOOS",
            0xff3f : "HIOS",
            0xfff1 : "ABS",
            0xfff2 : "COMMON",
            0xffff : "XINDEX"
        }
        if numToInd.get(index) == None:
            output.write(str(index).rjust(6) + " ")
        else:
            output.write(numToInd[index].rjust(6) + " ")
        
        output.write(name + "\n")

    output.write("\n")
    return

def toABI(num):
    intNum = int(num, 2)
    if 10 <= intNum <= 17:
        return "a" + str(intNum % 10)
    elif intNum == 1:
        return "ra"
    elif 5 <= intNum <= 7 or 28 <= intNum <= 31:
        return "t" + str(intNum % 19 - 5)
    elif 8 <= intNum <= 9 or 18 <= intNum <= 27:
        intNum = intNum - 8
        if intNum > 1:
            intNum = intNum - 8
        return "s" + str(intNum)
    elif intNum == 2:
        return "sp"
    elif intNum == 3:
        return "gp"
    elif intNum == 4:
        return "tp"
    elif intNum == 0:
        return "zero"
    else:
        return "x" + str(intNum)

def dopTwo(num):
    intNum = -(int(num[0]) * 2**(len(num) - 1))

    for i in range(1, len(num)):
        intNum = intNum + int(num[i]) * 2**(len(num) - 1 - i)
    
    return str(intNum)

currAddr = 0

def printTypeI(binCom, typeCom):
    
    global currPos, indNames, sizeNames, indSymtab, indText, sizeSymtab, sizeText
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX, currAddr
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead, namesOfCommand

    ItypeN = typeCom[-1:]
    ItypeCom = binCom[17:20] + typeCom[-1:]

    comOfI = {
        '0001': "jalr",
        '0002': "lb",
        '0012': "lh",
        '0102': "lw",
        '1002': "lbu",
        '1012': "lhu",
        '0003': "addi",
        '0103': "slti",
        '0113': "sltiu",
        '1003': "xori",
        '1103': "ori",
        '1113': "andi",
        '0013': "slli",
        '1013': "srli_srai",
        '0014': "csrrw",
        '0104': "csrrs",
        '0114': "csrrc",
        '1014': "csrrwi",
        '1104': "csrrsi",
        '1114': "csrrci",
        '0004': "ecall_ebreak"
    }
    
    command = comOfI.get(ItypeCom)

    metk = ""
    if namesOfCommand.get(currAddr) != None:
        metk = namesOfCommand.get(currAddr) + ":"

    output.write(metk.rjust(10) + " ")

    if ItypeN == "1" or ItypeN == "2":
        rd = toABI(binCom[20:25])
        rs1 = toABI(binCom[12:17])
        imm = dopTwo(binCom[0:12])
        output.write(command + " " + rd + ", " + imm + "(" + rs1 + ")\n")
    elif ItypeN == "3":
        rd = toABI(binCom[20:25])
        rs1 = toABI(binCom[12:17])
        if ItypeCom == "0013" or ItypeCom == "1013":
            imm = str(int(binCom[7:12], 2))
            if ItypeCom == "1013" and binCom[1] == '1':
                command = "srai"
            elif ItypeCom == "1013":
                command = "srli"
        else:
            imm = dopTwo(binCom[0:12])
        output.write(command + " " + rd + ", " + rs1 + ", " + imm + "\n")
    elif ItypeN == "4" and ItypeCom != "0004":
        csrFlag = {
            0x001: "fflags",
            0x002: "frm",
            0x003: "fcsr",
            0xC00: "cycle",
            0xC01: "time",
            0xC02: "instret",
            0xC80: "cycleh",
            0xC81: "timeh",
            0xC82: "instreth"
        }
        rd = toABI(binCom[20:25])
        csr = int(binCom[0:12])
        if len(command) > 5:
            zimm = str(int(binCom[12:17], 2))
            output.write(command + " " + rd + ", " + csrFlag.get(csr) + ", " + zimm + "\n")
        else:
            rs1 = toABI(binCom[12:17])
            output.write(command + " " + rd + ", " + csrFlag.get(csr) + ", " + rs1 + "\n")
    else:
        if binCom[11] == '1':
            output.write("ebreak" + "\n")
        else:
            output.write("ecall" + "\n")
    
    return

def printTypeU(binCom, typeCom):

    global currPos, indNames, sizeNames, indSymtab, indText, sizeSymtab, sizeText
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX, currAddr
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead, namesOfCommand

    UtypeN = typeCom[-1:]
    
    imm = dopTwo(binCom[0:20] + "0" * 12)
    rd = toABI(binCom[20:25])

    command = "auipc"
    if UtypeN == "1":
        command = "lui"

    metk = ""
    if namesOfCommand.get(currAddr) != None:
        metk = namesOfCommand.get(currAddr) + ":"

    output.write(metk.rjust(10) + " ")
        
    output.write(command + " " + rd + ", " + imm + "\n")

    return

def printTypeJ(binCom, typeCom):

    global currPos, indNames, sizeNames, indSymtab, indText, sizeSymtab, sizeText
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX, currAddr
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead, namesOfCommand

    rd = toABI(binCom[20:25])
    imm = int("0" * 11 + binCom[0] + binCom[12:20] + binCom[11] + binCom[1:11] + "0", 2)
    command = "jal"

    metk = ""
    output.write(metk.rjust(10) + " ")

    metkImm = ""
    if namesOfCommand.get(currAddr + imm) != None:
        metkImm = " " + namesOfCommand.get(currAddr + imm)
    
    output.write(command + " " + rd + ", " + str(imm) + metkImm + "\n")

    return

def printTypeB(binCom, typeCom):

    global currPos, indNames, sizeNames, indSymtab, indText, sizeSymtab, sizeText
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX, currAddr
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead, namesOfCommand

    BtypeCom = binCom[17:20]

    comOfB = {
        '000': "beq",
        '001': "bne",
        '100': "blt",
        '101': "bge",
        '110': "bltu",
        '111': "bgeu"
    }

    command = comOfB.get(BtypeCom)
    rs1 = toABI(binCom[12:17])
    rs2 = toABI(binCom[7:12])
    imm = dopTwo(binCom[0] * 20 + binCom[24] + binCom[1:7] + binCom[20:24] + "0")

    metk = ""

    output.write(metk.rjust(10) + " ")

    output.write(command + " " + rs1 + ", " + rs2 + ", " + imm + " LOC_" + hex(currAddr)[2:] + "\n")

    return

def printTypeS(binCom, typeCom):

    global currPos, indNames, sizeNames, indSymtab, indText, sizeSymtab, sizeText
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX, currAddr
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead, namesOfCommand

    StypeCom = binCom[17:20]

    comOfS = {
        '000': "sb",
        '001': "sh",
        '010': "sw",
    }
    
    command = comOfS.get(StypeCom)
    rs1 = toABI(binCom[12:17])
    rs2 = toABI(binCom[7:12])
    imm = dopTwo(binCom[0] * 21 + binCom[1:7] + binCom[20:25])

    metk = ""
    if namesOfCommand.get(currAddr) != None:
        metk = namesOfCommand.get(currAddr) + ":"

    output.write(metk.rjust(10) + " ")

    output.write(command + " " + rs2 + ", " + imm + "(" + rs1 + ")\n")

    return

def printTypeR(binCom, typeCom):

    global currPos, indNames, sizeNames, indSymtab, indText, sizeSymtab, sizeText
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX, currAddr
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead, namesOfCommand

    RtypeCom = binCom[1] + binCom[17:20]
    
    comOfR = {
        '0000': "add",
        '1000': "sub",
        '0001': "sll",
        '0010': "slt",
        '0011': "sltu",
        '0100': "xor",
        '0101': "srl",
        '1101': "sra",
        '0110': "or",
        '0111': "and"
    }
    
    command = comOfR.get(RtypeCom)
    rd = toABI(binCom[20:25])
    rs1 = toABI(binCom[12:17])
    rs2 = toABI(binCom[7:12])

    metk = ""
    if namesOfCommand.get(currAddr) != None:
        metk = namesOfCommand.get(currAddr) + ":"

    output.write(metk.rjust(10) + " ")

    output.write(command + " " + rd + ", " + rs1 + ", " + rs2 + "\n")

    return

def printCommand():

    global currPos, indNames, sizeNames, indSymtab, indText, sizeSymtab, sizeText
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX, addrText, namesOfCommand
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead, currAddr

    typeOfCom = {
        '0110011': 'R',
        '0010011': 'I3',
        '0000011': 'I2',
        '1110011': 'I4',
        '1100111': 'I1',
        '0100011': 'S',
        '1100011': 'B',
        '0110111': 'U1',
        '0010111': 'U2',
        '1101111': 'J'
    }

    currCom = readBitsLE(4)
    binCom = bin(currCom)[2:].rjust(32, "0")

    if binCom[-2:] == "11":
        sizeText = sizeText - 4
        
        output.write(hex(currAddr)[2:].rjust(8, "0") + " ")

        currTypeOfCom = "Unknown"
        if typeOfCom.get(binCom[-7:]) != None:
            currTypeOfCom = typeOfCom.get(binCom[-7:])
        #print("Type = " + currTypeOfCom, end = " : ")
        
        if currTypeOfCom[:1] == "I":
            printTypeI(binCom, currTypeOfCom)
        elif currTypeOfCom[:1] == "U":
            printTypeU(binCom, currTypeOfCom)
        elif currTypeOfCom[:1] == "J":
            printTypeJ(binCom, currTypeOfCom)
        elif currTypeOfCom[:1] == "B":
            printTypeB(binCom, currTypeOfCom)
        elif currTypeOfCom[:1] == "S":
            printTypeS(binCom, currTypeOfCom)
        elif currTypeOfCom[:1] == "R":
            printTypeR(binCom, currTypeOfCom)
        else:
            output.write(currTypeOfCom + "\n")
    else:
        sizeText = sizeText - 2
        currPos = currPos - 2
        output.write("Unknown\n")
        
    
    return

def parseText():
    
    global currPos, indNames, sizeNames, indSymtab, indText, sizeSymtab, sizeText
    global eiClass, eiData, eType, eEntry, indProgHead, indSHSTRNDX, currAddr, namesOfCommand
    global indSecHead, singleSizeProg, cntProgHead, singleSizeSec, cntSecHead, addrText

    currPos = indText
    currAddr = addrText
    
    cnt = 0
    output.write(".text\n")
    while sizeText > 0:
        #print(cnt, end = " ")
        cnt = cnt + 1
        printCommand()
        currAddr = currAddr + 4
        
    return
try:
    file = open(sys.argv[1], 'rb')

    bites = file.read()
except Exception as e:
    print("С файлом на чтение проблемы")
    exit(0)

output = open(sys.argv[2], 'w')
currPos = 0

try:
    parseHeader()

    parseSecHeader()

    parseSymtab()

    parseText()
except Exception as e:
    print("Проблемы с выводом/состоянием elf файла")
    exit(0)
