# Current routing checkpoint

This is an unfinished hardware draft, not a fabrication release.

The five front switches were moved away from the LCD. Their centres are
UP (42,31), DOWN (42,17), LEFT (35,24), RIGHT (49,24), OK (42,24), in mm.
The OK switch is rotated 90 degrees to avoid neighbouring pads. The upper
switch body clears the LCD envelope by 4.95 mm. All 161 component pad/body
bounds pass the conservative placement screen. Enclosure keycap dimensions
and assembly tolerances are still provisional.

Native JRouter and HRouter passes have been applied selectively. HRouter
additions with clearance conflicts on NFC_DWL_REQ, I2C_SCL and I2S_DIN were
rejected; the existing routes on those nets were preserved. Fixed pad and
via contacts with sub-0.01-mil rounding differences were aligned without
changing nets, pad locations, trace widths or via drills.

Latest native DRC: **0 external clearance errors, 2 USB footprint clearance
errors, 42 disconnected objects**. These are error-object counts, not counts
of missing individual wires. The detailed report is
`drc-key-spacing-refined.json`; older DRC reports are historical snapshots.
LEFT and OK signals have no remaining connection errors. UP, DOWN and RIGHT
each still have two disconnected objects, so their routing is not complete.

Three GND pour boundaries are present, but obsolete filled-copper caches
were removed and the pours need recomputation after the remaining routing.
USB locating-hole/pad clearance and exact connector qualification are still
open. Do not order boards from this checkpoint.

The saved schematic export passes 350 pin-to-net assertions. All 569 native
PCB pad-net assignments are unchanged by this mechanical adjustment.
The source project, placement plan, document-layer button guides and
mechanical SVG/PNG/DXF use the updated positions.
