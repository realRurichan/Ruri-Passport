# Current routing checkpoint

The routing and native electrical DRC checkpoint is complete. This is not
a fabrication release; manufacturing and assembly qualifications remain open.

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

Latest native strict DRC: **0 violations**, after completing the key, LCD,
NFC, microphone, charger and 3V18 routes, rebuilding all three ground pours,
and correcting the USB footprint. The current report is
`drc-routed-poured.json`; all other DRC reports are historical snapshots.
No global clearance rules were relaxed and no errors were ignored.

Top, Inner1 and Bottom GND pours were rebuilt and saved. The Inner1 layer
remains the ground reference. The last isolated DOWN-switch ground pad was
connected after rerouting the nearby CHG_ISET branch. Microphone BCLK was
reworked to allow the DIN escape; the ESP supply completion uses 0.40 mm
traces. Route additions and removed-object records accompany this report.

The USB4105 footprint now follows GCT Rev B1 pad, locating-hole and shell-slot
dimensions in both schematic and PCB sources. Its nominal 0.1751 mm NPTH
copper clearance passes the existing 6 mil electrical rule but still requires
JLC DFM acceptance against the usual 0.20 mm manufacturing clearance. See
`usb-footprint-correction-20260926.md`; USB-1 is not a closed manufacturing item.
Final Gerber/drill review, power/return-path review, sourcing, assembly and
full two-unit quote are still required. Do not order from this checkpoint.

The native JLC04161H-7628 physical stackup has now been applied and read back:
35 um outer copper, 15.2 um inner copper, 0.2104/1.065/0.2104 mm dielectrics.
The exported DFM draft passes the selected independent geometry checks in
`gerber-draft-check.json` (four copper files, NPTHs, USB slots, pads, paste,
and main outline). These focused checks do not replace complete DFM/CAM.

The saved schematic export passes 350 pin-to-net assertions. All 569 native
PCB pad-net assignments are unchanged by this mechanical adjustment.
The source project, placement plan, document-layer button guides and
mechanical SVG/PNG/DXF use the updated positions.
