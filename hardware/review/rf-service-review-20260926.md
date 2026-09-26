# RF_Service independent one-pass review — 2026-09-26

Scope: `hardware/tools/add_rf_service.py`, `hardware/tools/nfc_matching_estimate.py`, `hardware/design/NFC.md`, native `RF_Service.esch2`, and `/private/tmp/ruri-rf-service-check.enet`. Read-only review of CAD; no GUI/MCP used, no CAD edits. Antenna spiral/bridge copper is a known next implementation step, not an undiscovered review defect. This is not a manufacturing release or RF performance certification.

## Findings requiring correction before RF layout / manufacturing gate

### RF-1 — R60/R61 minimum power rating is insufficiently specified (medium)

Both native components and generator specify `1.5R / 1% / >=0.1W` on R0603. Do not select an ordinary 0.1 W resistor on this requirement. The coil circulating current can exceed transmitter DC supply current; the 250 mA TX supply limit does not make a 0.1 W damper safe.

Using the project's own model and exact reported L = 1.028440711 µH, 1.5 Ω antenna loss, 5 pF parallel capacitance, C1 = 62 pF, C2 = 200 pF, 160 nH/750 pF EMC, and 1.5 Ω each damper:

- An ideal 2.7 V full bridge has first-harmonic differential RMS voltage `2*sqrt(2)/pi*2.7 = 2.431 V`.
- Model predicts input real power about 0.540 W and antenna-branch RMS current about 0.3387 A.
- Each damper dissipates `I²R = 0.1721 W`.
- Even 2.0 V RMS drive gives approximately 0.1165 W per damper with this model.

This is a conservative screening calculation, not a prediction of the real nonlinear PN7160 driver; driver loss, RF loading and DPC change the result. It is sufficient to show that the currently permitted 0.1 W part has no supported margin. Specify and source a resistor rated at least 0.25 W with temperature derating appropriate to the enclosed board, reserving its actual footprint (often 0805 or a rated high-power 0603), then measure RF-on temperature and current. A lower rated part requires a demonstrated lower drive envelope, not just a nominal TX current limit.

NXP AN13219 section 4.1.3.4 calls for damping to control antenna Q, and section 4.1.3.5 targets 210–230 mA TX supply current with a 250 mA ceiling. It does not equate that current with antenna current. Source: https://www.nxp.com/docs/en/application-note/AN13219.pdf

### RF-2 — ANT1 terminals have default solder-paste expansion (low, manufacturing metadata)

The embedded antenna footprint UUID `ab360fa267c1a6f7`, pads 1 and 2, has `topPasteExpansion: null` and `bottomPasteExpansion: null`. These are ordinary top SMD pads (0.4 × 0.4 mm) with open mask and default paste behavior. Excluding ANT1 from BOM does not necessarily remove stencil apertures. The terminal pads are PCB copper, not assembled components; explicitly suppress paste as already done for TP1–TP10, and confirm the paste Gerber contains no ANT1 apertures. Keep mask exposure only where wanted for measurements/solder access. The eventual spiral can remain soldermask-covered according to the final antenna layout plan.

## Verified circuit and metadata

- Native RF path: U8 TX1 → L2 → RF_EMC_A → C42 → RF_MATCH_A → R60 → ANT_A; mirrored TX2/L3/C43/R61/ANT_B. C40/C41 shunt the EMC nodes; C44/C45 shunt the matching nodes. This is the expected balanced network topology.
- Receiver default: RF_EMC_A → R62 2.2 kΩ → C46 1 nF → NFC_RXN; RF_EMC_B → R63 → C47 → NFC_RXP. TX1 pairs with RXN and TX2 with RXP, matching NXP AN13219 Fig. 37. Alternate antenna-side R64/R65 are 6.8 kΩ and DNP; pair selection instructions correctly forbid fitting both pairs. Alternative taps are after damping resistors, directly on coil terminals; receiver loading must be included during tuning of that configuration.
- AN13219 sections 6.1/6.2 explicitly recommend 2.2 kΩ at EMC as a starting point, 6.8 kΩ at antenna, and 1 nF AC coupling. The 816 mm² nominal outer rectangle is only slightly above the 800 mm² example threshold; it does not establish good ALM recovery. Retaining both options is appropriate. Default EMC pick-up may be changed to antenna pick-up after AGC/ALM testing.
- 160 nH / 750 pF gives 14.529 MHz filter resonance, within the 14.4–14.7 MHz symmetrical-tuning range. AN13219 Table 4 gives typical 11 Ω target for TVDD ≤3.3 V, so using 11 Ω with 2.7 V TXLDO is supported as an initial target.
- DPC requirement is explicit in docs and sheet. AN13892 sections 3–5 state symmetrical tuning requires DPC; new chips have it disabled by default; continuous-RF and PRBS test modes do not run DPC. Add this latter distinction to bench instructions so matching tests use monitored/current-limited RF excitation rather than assuming production-mode DPC protects continuous test mode. Source: https://www.nxp.com/docs/en/application-note/AN13892.pdf
- Matching script correctly labels geometric approximation, assumed loss/capacitance, receiver-load omission and nonlinear-driver omission. Computed 62/200 pF trial network impedance is about 10.685 − j1.666 Ω; it is not falsely marked tuned. Q estimate is about 19.47. Coil shape must still match the assumptions after physical spiral implementation.
- LQW18CNR16J00 is a 160 nH ±5% 1 A RF inductor, maximum DC resistance 0.1 Ω, 0603; this is consistent with the present assignment. Murata official list: https://www.murata.com/-/media/webrenewal/tool/library/common-pdf/static-model/component-list-ind-s-2602.ashx?cvid=20260515010000000000&la=en-gb
- All nominal RF capacitors are specified C0G 50 V. First-harmonic model at ideal 2.7 V drive gives approximate per-branch peaks C0 4.9 V, Cs 20.7 V, Cp 21.8 V, which provides initial nominal headroom. Loaded, detuned and external-reader field voltage remains to be measured; this calculation is not a universal 50 V stress proof. Actual CIDs/MPNs and current/ESR suitability remain sourcing work.
- Native no-BOM flags: R64/R65, C48–C51, ANT1 and TP1–TP10 all have `Add into BOM=no`, `Convert to PCB=yes`. The generator alone does not set all exclusions; `normalize_schematic_sources.py` is the required post-generation step and current native output confirms it was applied. Final populated BOM and pick-and-place export must retain these exclusions.
- TP footprint UUID `238161e3a1e5ba70` has a 1 mm top copper pad with top/bottom paste expansion -100 and mask default. Check actual paste Gerber after board export, since negative expansion behavior is a native-tool rendering matter.
- D5 pins 1/2 protect SD_MISO/SD_CS_N; D6 pins 1/2 protect SD_DAT1/SD_DAT2; all pin 3s are GND. D7 pin 1 protects VBUS_5V, pin 2 is unconnected, pin 3 is GND. Non-A TPD2EUSB30DRTR has 0–5.5 V recommended working range; A version only 0–3.6 V, so explicit no-A substitution instruction is correct. No extra supply pin or unpowered-rail backfeed is introduced. Native pin map agrees with TI table 5-1. Source: https://www.ti.com/lit/ds/symlink/tpd2eusb30.pdf (sections 5, 6.3). Layout still must put clamps at connectors with short discharge-to-ground paths; ESD ratings do not constitute input OVP.
- Maintenance pads connect GND, 3V18, ESP_EN, BOOT_N, NFC_DWL_REQ, VSYS, VBAT, 3V18_PERIPH, NFC_IRQ, and NFC_TVDD as named. DWL_REQ instruction uses 3V18 (=VDD_PAD), not battery voltage, before VEN rises; this follows AN12988 section 5.3. VEN is controlled through IO expander, so software must perform that edge for NFC update. USB ROM boot test needs physical access to BOOT/EN/GND; placement remains outstanding. Source: https://www.nxp.com/docs/en/application-note/AN12988.pdf

## Explicit remaining prototype work (not additional design defects)

Implement actual coil/bridge copper, all-layer keepout and feed return; ensure copper topology has no shortcut between terminals. Tune bare coil and final assembly using measured impedance; calibrate DPC and monitor supply current under metal/tag loading; check receiver AGC (NXP recommends decimal 500–800), RF component voltage/current/temperature, reader modes and Type-4 card-emulation/ALM over alignment and distance. Perform native DRC and independently inspect copper/mask/paste Gerbers and populated assembly outputs. None of these are proven by the native 346-pin-net assertion pass.

Review terminated after this pass as requested.
