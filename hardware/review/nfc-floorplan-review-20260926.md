# NFC / mechanical floorplan review — 2026-09-26

Read-only, one pass. Termination criterion: deliver one bounded list of evidenced issues, feasible layout choices and a verdict; no edits to the EDA project or UI. This reviews the proposed coordinates supplied by the design agent, not a finished PCB export. Distances below are geometric calculations, not RF measurements.

## Verdict

**The bottom-right PCB NFC loop is reasonable to draw into an engineering prototype. The available evidence does not require an external FPC antenna. It is NOT an RF-validated design. FIX FIRST before layout release: F1 ESP antenna clearance and F2 the mechanical NFC keepout. Plan F3 matching / DPC / RX tuning before claiming reader or card-emulation performance.**

The original 30 × 27 mm loop at x56..86, y1.5..28.5 is physically separate from the stated screen and battery. Its 810 mm² outer area, 4 turns, 0.4 mm width, 0.3 mm spacing and 35 µm copper fall within NXP AN13219 Table 2 recommendations. Passing that table is not a guarantee of range or card-emulation coupling. The ~1 µH goal must be checked from actual artwork and then measured in the enclosure.

## Findings

### F1 — SERIOUS: proposed front-left key encroaches on ESP antenna clearance guidance

The ESP module is x4..22, y0..25, antenna facing the bottom edge. Its actual antenna outline / feed location has not yet been rederived from the module drawing. For any bottom-edge antenna zone whose right edge is x22, the left key at (32,14), with a 6 mm body, starts at x29: only 7 mm horizontal separation. Depending on the antenna-zone height, its distance is still likely below the manufacturer-recommended 15 mm. This is a verified geometric concern, **not a claim that Wi-Fi will fail**. The final exact violation needs the real module antenna polygon.

Espressif recommends extending the antenna beyond the baseboard, or cutting away baseboard material around / beneath it when it cannot protrude. The final enclosure should provide 15 mm clearance in all directions, with range / throughput tested on the complete product. A ground-plane keepout alone is not the complete recommendation.

Cheapest fix: explicitly place the true antenna polygon and its 15 mm mechanical keepout before freezing the D-pad and USB location. Move / rotate the module or adjust the key layout. A cutout / antenna overhang can preserve the main board dimensions; it still requires the enclosure and key metals to respect clearance. Do not assume simply moving the module left by 4 mm closes this finding. No additional electronic part is inherently required.

### F2 — SERIOUS qualification item: NFC is clear in projection but immediately adjacent to large metal

Calculated from the proposal: loop top y28.5 to LCD bottom y29 = **0.5 mm** planar gap, and to battery bottom y30 = **1.5 mm**. LCD backing is reportedly ~3 mm above the top copper; the exact metal outline, battery pouch / tabs, support posts, LCD FPC fold, key brackets, fasteners and wiring are not frozen. The NFC keepout must include them on both sides and all copper layers. The proposed all-layer keepout is a good start.

AN13219 §3 explains that nearby metal reduces inductance and Q through eddy currents, and recommends ferrite in a close metallic environment. It does **not** give a universal minimum edge-to-edge gap that lets this 0.5 mm + 3 mm-Z layout be certified by inspection. Thus neither “certain failure” nor “3 mm is safe” is supported.

Lowest-cost improvement worth drawing before routing: use a slightly wider, shorter loop, e.g. **34 × 24 mm at x53..87, y1..25**, outer area 816 mm². This increases projected LCD gap to 4 mm and battery gap to 5 mm. A 6 mm right key centred at (48,14) ends x51, leaving 2 mm to the new loop. That is only a candidate envelope: key pads / metal enclosure and needed antenna feed / ground setback still need checking. It preserves the component count and does not establish RF sufficiency. Avoid deciding matching values until this envelope is frozen.

If the final assembly puts metal above or below the loop, preserve room for a qualified 13.56 MHz ferrite sheet covering the whole loop, and remeasure with it installed. Ferrite is not a drop-in after matching because it changes L and R. An external ferrite-backed FPC is a fallback only if the PCB solution cannot satisfy mechanical / measured RF requirements; it is not yet compelled by evidence.

### F3 — SERIOUS if omitted: small-loop matching must support loading and card-emulation receive sensitivity

AN13892 §3 uses an 800 mm² antenna as its example of a small antenna requiring symmetrical matching plus DPC. Symmetrical matching without DPC risks TXLDO overcurrent. DPC is disabled by default and needs antenna-specific configuration; this hardware choice creates a required bring-up firmware step even though application software comes later.

AN13219 §6.2 distinguishes RX taps at the EMC filter and at the antenna; the small-antenna tap can improve receive amplitude and ALM clock recovery but changes Q. This proposal is only 10–16 mm² above the guide’s nominal 800 mm² split. Do not interpret the threshold as a robust guarantee that the filter tap is adequate. Cheapest layout mitigation: include selectable, normally-unpopulated alternative RX tap footprints and measured-value tuning components. When selecting direct antenna taps, the latest guide explicitly says the nominal 0-ohm placeholders must actually be populated with suitable kilo-ohm resistors (example 6.8 kΩ), not 0 Ω.

The bring-up procedure must measure L/R/C without matching populated, in the final housing with screen and battery installed; then derive matching, configure DPC, check TX current under tag loading, and test reader plus powered card-emulation communication with representative devices. AN13219 §4.1.2.2 calls for the final mechanical environment during VNA measurement. Arbitrary existing access-card compatibility is not established by this antenna review.

## Checked and acceptable at this concept stage

- The original NFC loop does not overlap the proposed LCD / battery / D-pad rectangles in XY. This is an envelope check only.
- NFC 810 mm² external outline meets the cited recommended size range; width, spacing, turns and copper thickness also fit it.
- The NFC and ESP antenna envelopes are separated horizontally by 34 mm in the original proposal; there is no literal mutual antenna overlap.
- A PCB coil removes an external antenna and connector from the BOM. This is a component-count saving, not a verified quote or a guarantee that tuning cost disappears.

## Sources

- NXP [AN13219 Rev. 1.6, 25 June 2026](https://www.nxp.com/docs/en/application-note/AN13219.pdf): Table 2 / §2.1.2 p4; metal/ferrite §3 pp8–12; final-housing VNA §4.1.2.2 p15; RX taps §6.2 p38. Read local `/private/tmp/ruri-pn7160-antenna.pdf` and text extraction.
- NXP [AN13892 Rev. 1.2](https://www.nxp.com/docs/en/application-note/AN13892.pdf): §3 pp6–7, DPC default and setup pp8–9. Read local `/private/tmp/ruri-pn7160-hw.pdf` and text extraction.
- Espressif [ESP32-S3 PCB Layout Design, module positioning](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html#general-principles-of-pcb-layout-for-modules-positioning-a-module-on-a-base-board), retrieved 2026-09-26: antenna placement, baseboard cutouts, enclosure clearance, final range / throughput check.

## Unverified — do not present as findings

Actual finished-device NFC range, whether the original 0.5 mm + 3 mm-Z arrangement would work at useful range, exact loop inductance/Q/SRF, the effectiveness of an optional ferrite sheet, and the exact ESP antenna keepout violation before importing the true antenna geometry are not measured here.
