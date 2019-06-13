# Dzus panel template drawing
# Produces a DXF file which can be used as the basis for a
# flight simulator panel.

# (C) June 2019 A M Errington

# GPL v3.0 licence

# Input is the width of the panel in inches, and the height of the
# panel in Dzus units. One unit is 3/8"
# Also, a list of positions where a Dzus fastener will be installed.
# The DXF will include a 4mm hole in the panel for the fastener, and
# a rebate in the fascia.
# The original panels are measured in inches, but all measurements
# are converted to mm.

# Output is a DXF file that can be loaded into a CAD package to add
# holes for switches and indicators etc. The DXF file has separate
# layers for 'plate' (the backing support plate, typically 1.6mm aluminium),
# 'fascia', the thicker front panel, typically 6mm acrylic or other
# material, and 'decal' for text.

# Don't forget that the fascia is smaller than the plate by 1/32" on all
# sides. This means that location (0,0) is 1/32" away from the lower left
# corner of the fascia.

import ezdxf

# Parameters
# ==========
# In a later version these parameters will come in from the command line

# There is no thickness, this is a 2D drawing
w_inches = 5.75     # Width of panel in inches (default is 5.75")
h_units = 9         # Height of panel in Dzus units (3/8")

# Location of mounting holes on left, 0 is bottom, but 1 is first useful hole
# Set to [] for no holes.
left_mount = [1, 7]
# Location of mounting holes on right
right_mount = [1, 7]

# Output filename
filename = "panel.dxf"


def intomm(inches):
    return inches * 25.4

# Create a new drawing object
dwg = ezdxf.new('R2010')
msp = dwg.modelspace()

# Create some layers for ease of drafting in CAD software
dwg.layers.new(name='plate')
dwg.layers.new(name='plate_construction', dxfattribs={'linetype': 'Center'})

dwg.layers.new(name='fascia')
dwg.layers.new(name='fascia_construction', dxfattribs={'linetype': 'Center'})

dwg.layers.new(name='decal', dxfattribs={'lineweight': 50}) # Set lineweight for decals to 0.5mm (my not be supported by some CAD applications)
dwg.layers.new(name='decal_construction', dxfattribs={'linetype': 'Center'})


# Outer dimensions of plate (mm)
top = intomm(h_units * (3/8))
bottom = 0
left = 0
right = intomm(w_inches)


# PLATE
# =====
# Outline of plate
msp.add_line( (left, bottom), (right, bottom), dxfattribs={'layer': 'plate'}) # bottom edge
msp.add_line( (right, bottom), (right, top), dxfattribs={'layer': 'plate'})   # right edge
msp.add_line( (right, top), (left, top), dxfattribs={'layer': 'plate'})       # top edge
msp.add_line( (left, top), (left, bottom), dxfattribs={'layer': 'plate'})     # left edge

# Mounting holes in plate, if there are any
if left_mount:
    msp.add_line( (intomm(3/16), bottom-10), (intomm(3/16), top+10), dxfattribs={'layer': 'plate_construction'})

for pos in left_mount:
    msp.add_line( (left-10, intomm(pos * (3/8) + (3/16))), (right/2, intomm(pos * (3/8) + (3/16))), dxfattribs={'layer': 'plate_construction'})
    msp.add_circle( (intomm(3/16), intomm(pos * (3/8) + (3/16))), 2, dxfattribs={'layer': 'plate'})

if right_mount:
    msp.add_line( (right - intomm(3/16), bottom-10), (right - intomm(3/16), top+10), dxfattribs={'layer': 'plate_construction'})    

for pos in right_mount:
    msp.add_line( (right/2, intomm(pos * (3/8) + (3/16))), (right+10, intomm(pos * (3/8) + (3/16))), dxfattribs={'layer': 'plate_construction'})
    msp.add_circle( (right - intomm(3/16), intomm(pos * (3/8) + (3/16))), 2, dxfattribs={'layer': 'plate'})


# FASCIA
# ======
# Outline of fascia (inset by 1/32" all around, with r1/32" rounded corners,
# which is why the figure 2/32" appears. It's more explicit than 1/16").

# Bottom left corner
msp.add_arc( (intomm(2/32), intomm(2/32)),
             intomm(1/32), 180, 270, dxfattribs={'layer': 'fascia'})
# Bottom line
msp.add_line( (left + intomm(2/32), bottom + intomm(1/32)),
             (right - intomm(2/32), bottom + intomm(1/32)), dxfattribs={'layer': 'fascia'})
# Bottom right corner
msp.add_arc( (right - intomm(2/32), intomm(2/32)),
            intomm(1/32), 270, 0, dxfattribs={'layer': 'fascia'})

# Top left corner
msp.add_arc( (intomm(2/32), top - intomm(2/32)),
            intomm(1/32), 90, 180, dxfattribs={'layer': 'fascia'})
# Top line
msp.add_line( (left + intomm(2/32), top - intomm(1/32)),
             (right - intomm(2/32), top - intomm(1/32)), dxfattribs={'layer': 'fascia'})
# Top right corner
msp.add_arc( (right - intomm(2/32), top - intomm(2/32)),
            intomm(1/32), 0, 90, dxfattribs={'layer': 'fascia'})

# Horizontal and vertical construction lines across centre of fascia
msp.add_line( (right/2, bottom-10), (right/2, top+10),
              dxfattribs={'layer': 'fascia_construction'})
msp.add_line( (left-10, top/2), (right+10, top/2),
              dxfattribs={'layer': 'fascia_construction'})

# Rebates for mounting holes (if there are any)
# The fasteners are 3/8" diameter, with a 1/16" clearance all around.
# Radius is therefore 3/16" + 1/16".
# There is a 1/32" radius lead in and lead out from the rebate

# Left side, start at the bottom
last_x = left + intomm(1/32)
last_y = intomm(2/32)

if left_mount:
    msp.add_line( (intomm(3/16), bottom-10), (intomm(3/16), top+10),
                  dxfattribs={'layer': 'fascia_construction'})

for pos in left_mount:
    centre_x = intomm(3/16)
    centre_y = intomm(pos * (3/8) + (3/16))

    msp.add_line( (left-10, centre_y), (right/2, centre_y),
                  dxfattribs={'layer': 'fascia_construction'})

    msp.add_line( (last_x, last_y),
                  (left + intomm(1/32), centre_y - intomm((3/16) + (1/16) + (1/32)) ),
                  dxfattribs={'layer': 'fascia'})
    msp.add_arc( (left + intomm(2/32), centre_y - intomm((3/16) + (1/16) + (1/32)) ),
                intomm(1/32), 90, 180, dxfattribs={'layer': 'fascia'})
    msp.add_line( (left + intomm(2/32), centre_y - intomm((3/16) + (1/16)) ),
                  (left + intomm(3/16), centre_y - intomm((3/16) + (1/16)) ),
                  dxfattribs={'layer': 'fascia'})    
    msp.add_arc( (centre_x, centre_y),
                 intomm((3/16) + (1/16)), 270, 90, dxfattribs={'layer': 'fascia'})
    msp.add_line( (left + intomm(2/32), centre_y + intomm((3/16)+(1/16)) ),
                  (left + intomm(3/16), centre_y + intomm((3/16)+(1/16)) ),
                  dxfattribs={'layer': 'fascia'})
    msp.add_arc( (left + intomm(2/32), centre_y + intomm((3/16) + (1/16) + (1/32))),
                 intomm(1/32), 180, 270, dxfattribs={'layer': 'fascia'})

    #last_x = left + intomm(1/32)
    last_y = centre_y + intomm((3/16) + (1/16) + (1/32))
    
msp.add_line((last_x, last_y), (intomm(1/32), top - intomm(2/32)), dxfattribs={'layer': 'fascia'})

# Right side, start at the bottom
last_x = right - intomm(1/32)
last_y = intomm(2/32)

if right_mount:
    msp.add_line( (right - intomm(3/16), bottom-10), (right - intomm(3/16), top+10),
                  dxfattribs={'layer': 'fascia_construction'})    

for pos in right_mount:
    centre_x = right - intomm(3/16)
    centre_y = intomm(pos * (3/8) + (3/16))

    msp.add_line( (right/2, centre_y), (right+10, centre_y),
                  dxfattribs={'layer': 'fascia_construction'})

    msp.add_line( (last_x, last_y),
                  (right - intomm(1/32), centre_y - intomm((3/16) + (1/16) + (1/32)) ),
                  dxfattribs={'layer': 'fascia'})
    msp.add_arc( (right - intomm(2/32), centre_y - intomm((3/16) + (1/16) + (1/32)) ),
                 intomm(1/32), 0, 90, dxfattribs={'layer': 'fascia'})
    msp.add_line( (right - intomm(2/32), centre_y - intomm((3/16) + (1/16)) ),
                  (right - intomm(3/16), centre_y - intomm((3/16) + (1/16)) ),
                  dxfattribs={'layer': 'fascia'})
    msp.add_arc( (centre_x, centre_y),
                 intomm((3/16) + (1/16)), 90, 270, dxfattribs={'layer': 'fascia'})
    msp.add_line( (right - intomm(2/32), centre_y + intomm((3/16)+(1/16)) ),
                  (right - intomm(3/16), centre_y + intomm((3/16)+(1/16)) ),
                  dxfattribs={'layer': 'fascia'})
    msp.add_arc( (right - intomm(2/32), centre_y + intomm((3/16) + (1/16) + (1/32))),
                 intomm(1/32), 270, 0, dxfattribs={'layer': 'fascia'})

    #last_x = left + intomm(1/32)
    last_y = centre_y + intomm((3/16) + (1/16) + (1/32))

msp.add_line((last_x, last_y), (right - intomm(1/32), top - intomm(2/32)), dxfattribs={'layer': 'fascia'})


# PLATE
# =====
# Centreline for panel name
msp.add_line( (left-10, top - intomm(13/64)), (right+10, top - intomm(13/64)), dxfattribs={'layer': 'decal_construction'})


# Write the file
dwg.saveas(filename)

# Done!
