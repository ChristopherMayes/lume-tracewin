import dataclasses
from dataclasses import dataclass

class Element:
    # Cast types
    def __post_init__(self):
        """
        Cast all fields
        """
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                #raise ValueError(f'Expected {field.name} to be {field.type}, '
                 #                f'got {repr(value)}')
                setattr(self, field.name, field.type(value))   
    
    @property
    def ele_type(self):
        return self.__class__.__name__.lower()
    
    @property
    def as_tracewin(self):
        """
        Return a TraceWin line for the element
        """
        
        x = self.ele_type.upper() + ' '
        x += ' '.join(map(str, dataclasses.asdict(self).values()) )
        
        return x
        
    
# Make this alias    
Command = Element
        
@dataclass    
class DummyElement:
    ele_type : str
    line : str
    
@dataclass
class Aperture(Element):  
    """
    dx: X half width (mm) or radius hole (pepperpot)
    dy: Y half width (mm) or distance between hole (pepperpot)
    n: Type :
        0 : Rectangular aperture
        1 : Circular aperture
        2 : Pepperpot mode
        3 : Rectangular aperture with dx & dy corresponding to a beam fraction intercepted by the aperture (adjusted with 0.1 mm step) if value <1, otherwise dx or dy are used as type=0
        4 : Horizontal finger with dx=finger center position, dy=total finger width.
        5 : vertical finger with dx=finger center position, dy=total finger width.
        6 : Ring aperture if particle radius, r>dy or r<dx with (dx<dy) particle is lost.
    
    """    
    dx : float
    dy : float
    n : int

        
@dataclass
class Drift(Element):
    """
    L: Length (mm)
    R: Aperture (mm)
    Ry: Aperture (mm)
    Rx_shift: Horizontal aperture shift (mm)
    Ry_shift: Vertical aperture shift (mm)
    """
    L : float
    R : float
    Ry : float
    Rx_shift : float = 0
    Ry_shift : float = 0
        

@dataclass
class Field_Map(Element):
    """
     geom: Field map type
     L: Field map length (mm)
     theta : RF input field phase (°)
     R :  Aperture (mm)
     kb  : Magnetic field intensity factor
     ka : Electric field intensity factor
     ki: Space charge compensation factor
     ka: Aperture flag
     filename : File name without extension (abs. or relative path) 
     p: 
         0: theta is relative phase
         1: theta is absolute phase
    """      
    geom : int
    L : float
    theta : float
    R : float
    kb : float
    ke : float
    ki : float
    ka : int
    filename : str
    p : int = 0
        
 

                
@dataclass
class Quad(Element):
    L : float # Length (mm)
    G : float
    R : float
    theta : float = 0
    g3 : float = 0
    g4 : float = 0        
    g5 : float = 0
    g6 : float = 0 
    GRF : float = 0    
           
    definition = (
    'Length (mm)',
    'Magnetic field gradient (T/m)',
    'Aperture (mm) ',
    'Skew Angle (°)',
    'Sextupole gradient (T/m2) or relative sex. component',
    'Octupole gradient (T/m3) or relative oct. component',
    'Decapole gradient (T/m4) or relative deca. component',
    'Dodecapole gradient (T/m5) or relative dode. component',
    'Good field radius (mm)')

    
    
@dataclass
class Thin_Steering(Element):    
    """
    BLx or ELx : x-component (T.m or V)
    Bly or ELy: y-component (T.m or V)
    r : Aperture (mm)
    elec : 
        0: magnetic deviation (default)
        1: electric deviation
    """    
    BLx : float 
    BLy : float
    r : float
    elec : int = 0
    
    
    
    
    
    
# Commands    
    
@dataclass
class Chopper(Command):
    """
    
    CHOPPER N, U(V), D(mm), C(mm), p(0/1)
    
    The chopper is inserted in the N elements placed just after the instruction "Chopper" (keeping the same length). U is the voltage between axis and plates and C is the chopper transverse position. +/-D is the distance between axis and plates
    """
    
    N : int
    U : float
    D : float
    C : float
    p : int
        
       
    
    
@dataclass
class Field_Map_Path(Command):    
    """
    FIELD_MAP_PATH path
    Set at the top of the structure file (*.dat), it allows to indicate the directory where is store thefield map
    file. This path can be absolute of relatice to the project file path.
    """     
    path : str
        
  
@dataclass
class Freq(Command):  
    """
    FREQ f(Mhz)
    FREQ command changes the R.F. frequency of the following structure, the beam frequency is not
    affected. By default, the RF frequency is the beam frequency defined in the TraceWIN GUI.
    """      
    f : float
        
@dataclass
class Lattice(Command):
    """
    LATTICE n1 n2
    LATTICE command defines the periodic focusing lattices, n1 is the number of element per basic lattice, n2 is the number of lattice per macro-lattice (usually 1). The number of element per macro-lattice is then n1n2. The basic lattice is used for set the phase advances according to SET_ADV commands. The macro-lattice is used for the phase advance calculation and corresponding matching. All following elements are considered as part of the next lattices until reaching the commands LATTICE_END or END.
    """       
    n1 : int
    n2 : int
        
@dataclass
class Lattice_End(Command):        
    """
    LATTICE_END command ends the periodic focusing lattices.   
    """    
    description : str = ''
        
        
@dataclass
class Set_Sync_Phase(Command):         
    """
    SET_SYNC_PHASE
    The phase given in an RF element preceded by the SET_SYNC_PHASE command is the synchronous phase of the generatrix particle, rather than the absolute phase (by default). It applies to following elements:
    FIELD_MAP 
    RFQ_CEL
    CAVSIN
    NCELLS
    """   
    description : str = ''
        
        
        
        


     
