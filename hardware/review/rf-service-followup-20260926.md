# RF_Service bounded follow-up — 2026-09-26

Scope limited to revised RF damping model, replacement resistor footprints, and ANT1 no-paste metadata. Read only; no CAD changes or GUI/MCP. Parent native netlist re-export remains pending.

## RF-1 resolved for the prototype design gate

Generator and current native RF_Service source now specify R60/R61/R66/R67 as 1 Ω, 1%, 0.25 W, C17928, sharing native R1206 footprint `cdcb5e0533824b1a`. Generator connects R60+R66 in branch A and R61+R67 in branch B through distinct RF_DAMP_A/B nets, yielding 2 Ω per branch. The final native exported connectivity should confirm the new intermediate nets and both resistor pairs.

The matching estimator consistently uses Rq=2 Ω per branch. For its explicitly assumed L=1.028440711 µH, antenna R=1.5 Ω and 5 pF self-capacitance:

- Approximate damped coil Q = 15.9315, within NXP's typical 15–20 range (AN13219 §4.1.3.4).
- Current 62/200 pF trial network: differential input ≈8.825−j1.831 Ω. With an ideal 2.7 V bridge fundamental of 2.431 V RMS, coil current ≈0.33416 A RMS; each 1 Ω resistor dissipates ≈0.11166 W, 44.7% of 0.25 W rating.
- Calculated 11 Ω match at C1≈70.638 pF / C2≈190.397 pF: coil current ≈0.30638 A RMS, each 1 Ω resistor ≈0.09387 W, 37.5% of rating.

This resolves the prior inadequately specified 0.1 W rating with useful nominal margin. It remains a screening model: verify actual resistor manufacturer derating for the maximum local temperature, RF RMS current and resistor temperature under tuned, loaded and detuned conditions. The unmodified 62/200 pF initial values are no longer close to an 11 Ω real match after the damping change; they are correctly labelled trial values, so measured tuning remains mandatory. Initial modeled RF input real power is about 0.642 W, leaving little margin to a 2.7 V ×250 mA transmitter budget before driver losses; do not assume the unchanged trial values automatically meet the DC current limit. Calibrate DPC and monitor supply current from the first RF-on test. Continuous test modes do not run DPC per AN13892 §5.

## RF-2 resolved at source metadata level

Current embedded ANT1 footprint UUID `580d67a9eeaff5dd` has pads 1 and 2 both set to `topPasteExpansion=-100`, `bottomPasteExpansion=-100`. ANT1 retains `Add into BOM=no`. Generator applies the same suppression before placing the antenna. Confirm no ANT1 paste apertures in the eventual Gerber; no copper-coil implementation or performance claims are implied here.

## Replacement resistor paste inspected — no additional defect

The R1206 library pads have automatic paste expansion `-3937.008`, but this is intentional: the footprint includes two explicit FILL polygons on layer 7, whose LAYER record identifies TOP_PASTE_MASK. These provide shaped apertures over each resistor land. An interim message flagged the negative pad expansion without considering those fills; that concern was explicitly retracted after inspection of the complete footprint. Preserve the library's custom paste shapes and verify them in final stencil output. Do not restore automatic full-pad paste on top of them merely because the expansion is negative.

No additional defect identified in this bounded follow-up. Original wider RF performance and manufacturing checks remain pending as recorded in the first review. Review stopped here.
