from enum import Enum

class ProjectRank(str, Enum):
    MEM = "PARTICIPANTE"
    DIR = "DIRECTOR DE PROYECTO"

class FellowRank(str, Enum):
    MIEMBRO = "Miembro"
    DIRECTOR = "Director"
    VI_PRE = "Vicepresidente"
    PRE = "Presidente"

class FellowArea(str, Enum):
    TI = "TECNOLOGÍA DE LA INFORMACIÓN"
    MKT = "MARKETING"
    PMO = "PROJECT MANAGEMENT OFFICE"
    LKTYFNZ = "LOGISTICA Y FINANZAS"
    GTH = "GESTION DEL TALENTO HUMANO"

class Roles(str, Enum):
    CRD = "COORDINADOR"
    DCT = "DIRECTOR DE PROYECTO"
    PTCP = "PARTICIPANTE"
