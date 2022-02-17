from tracewin.elements import *

ele_parser = {}
ele_parser['quad'] = Quad
ele_parser['aperture'] = Aperture
ele_parser['chopper'] = Chopper
ele_parser['drift'] = Drift
ele_parser['field_map'] = Field_Map
ele_parser['field_map_path'] = Field_Map_Path
ele_parser['freq'] =  Freq
ele_parser['lattice'] = Lattice
ele_parser['lattice_end'] = Lattice_End
ele_parser['set_sync_phase'] = Set_Sync_Phase
ele_parser['thin_steering'] = Thin_Steering


def parse_lattice_line(line, commentchar=';'):
    """
    Parse a single TraceWin lattice line
    
    """
    
    line = line.strip()

    # Split into actual element and description (anything after ;)
    x = line.split(commentchar)
    d = {}
    if len(x) == 1:
        # no description
        description = ''
        
    else:
        description = commentchar.join(x[1:])
    line = x[0].strip()

    
    # Look for name. 
    if ':' in line:
        s = line.split(':')
        name = s[0].strip()
        # Blank name -> marker
        if len(s) == 1:
            line = ''
        else:
            line = ':'.join(s[1:])
        
    else:
        name = None
    
    # Values
    v = line.split()
    if len(v) == 0:
        ele_type = 'marker'
    else:
        ele_type = v[0].lower()
    
    
    d['ele_type'] = ele_type
    d['name'] = name
    d['description'] = description
    d['v'] = v
    if ele_type in ele_parser:
        f = ele_parser[ele_type]
        ele = f(*v[1:])
    else:
        ele = DummyElement(ele_type, line)
        
    ele.description = description

    return ele