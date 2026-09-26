# PN7160 core independent review — 2026-09-26

Read-only, one pass. Scope: `hardware/tools/add_nfc.py` host/power/clock/card-mode design. No UI, native engineering document, or library was modified. This is a circuit-source review, not an independent exported-netlist check and not an RF matching/layout sign-off. Termination: deliver evidence-backed findings and a verdict once.

## Verdict

**FIX FIRST: F1 before freezing the NFC power/firmware interface.** Other core connections can proceed into layout. No pin-map, decoupling-topology, or powered-Type-4-card-mode blocker was found. RF matching remains outside this review.

## F1 — SERIOUS: the stated VSYS undervoltage safeguard is not implemented, and TXLDO Check is not its substitute

**Observed:** `add_nfc.py:20` requires RF disabled below VSYS=3.1 V. Pin 13 receives VSYS, while pins 12/28 receive regulated 3V18. Existing ADC divider R44/R45 measures the battery terminal, not VSYS. Thus neither that ADC reading nor PN7160's internal VBAT monitor directly measures VDD_UP. The minimum VSYS in the supplied design brief is 2.8 V; programmed TXLDO=2.7 V then lacks the required 0.3 V headroom.

**Manufacturer evidence:** [AN12988](https://www.nxp.com/docs/en/application-note/AN12988.pdf), §7.3.2 and p20: TXLDO must be below VDD_UP−0.3 V; its Byte9 check must be disabled for a VDD_UP supply other than the supported 3.6/5 V expectations. [AN13892](https://www.nxp.com/docs/en/application-note/AN13892.pdf), §9: RF_TXLDO_ERROR_NTF reports failure to start; the illustrated check selects the expected 3.6/5 V supply. It is not documented as a programmable 3.1 V comparator or continuous brownout guard.

**Failure scenario:** at low battery, or supply sag caused by simultaneous loads, the firmware assumes the nominal annotation protects RF operation while the actual TX supply has insufficient headroom; NFC read/card response may fail. Enabling the unsuitable 3.6 V check can instead prevent valid operation around 3.1–3.3 V.

**Cheapest correction, no new GPIO:** keep this topology, explicitly disable the unsuitable check according to NXP's configuration guidance, and replace the VSYS-ADC claim with a conservative battery-voltage enable policy. Its threshold must be derived from `Vbat_min >= 3.1 V + worst-case BQ battery-path drop + ADC error + transient margin`, measured under the maximum combined load. USB PGOOD alone is not proof of a stiff VSYS when input current limiting and battery supplementation are active. Preserve error-notification handling, but do not describe it as the undervoltage safeguard. Record the bound and bring-up test before enabling RF. Alternatively, move VDD_UP to 3V18 only after redoing the regulator, rail-noise and current budget for RF load; this is not an automatic recommendation.

## Checked and found correct

- U8 HVQFN40 pin numbering, ground pins and exposed pad match the [PN7160 datasheet](https://www.nxp.com/docs/en/data-sheet/PN7160_PN7161.pdf), Table 7. Pins 12/28, 14/18/22 and 26/27/31 are correctly grouped. Internal 1.8 V outputs are not fed from 3V18. VBAT/VDD_PAD=3V18 and separate VSYS supply for VDD_UP are within the permitted ranges when operated above the RF headroom limit.
- C29–C37 reproduce the nine decouplers and positions in AN12988 Fig.1/Table9. Exact purchased capacitors still need ±10% or better tolerance and DC-bias evaluation; the value strings alone do not establish effective capacitance.
- ANT1/ANT2/VDD_HF left open matches AN12988 Fig.1. Datasheet §11.4.4 assigns their rectifier to the special Power Off field-detection use case. This does not remove powered Type 4 card emulation through the regular RF interface. The existing “no batteryless card” limitation is appropriate.
- I2C ADR0/ADR1 grounded select 0x28. Common always-on I/O power avoids cross-rail level shifting. VEN host control via TCA9535 and its pulldown are suitable. WKUP_REQ grounded is compatible with host-interface wake. GPIO47 works as an awake interrupt; no deep-sleep card-service promise was reviewed.
- R59=100k tolerates the datasheet ±1 µA DWL input leakage with at most approximately 0.1 V, below VIL=0.8 V. A real accessible DWL test pad still needs to replace the placeholder text before layout release; it does not require another MCU GPIO.
- [AN14518](https://www.nxp.com/docs/en/application-note/AN14518.pdf), §7.2/Table9, explicitly lists XRCGB27M120F3M10R0 and requires pins 2/4 NC. Its active 1/3 connections are correct. Two 16 pF capacitors are acceptable only as the documented initial tuning population. Account explicitly for PN7160's 2 pF typical input capacitance on each oscillator pin plus PCB parasitics. AN14518 asks for measured −5 to 0 ppm offset and startup robustness; retain these as sample acceptance tests, not pre-layout achievements.
- Type4 ISO-DEP A/B scope is correct. Reader support for MIFARE Classic does not establish Classic card emulation. Unknown existing access cards remain compatibility-unverified.

## Limits / unverified, not additional blockers

Native pin-to-net resolution, exact component availability/assembly BOM, crystal footprint dimensions, PCB parasitics, regulator transient response, RF current, matching, and enclosure effects were not measured in this bounded review. No claim of final NFC range or production readiness is made.

## Builder disposition received after review

The builder selected the no-new-GPIO hardware correction: move U8.13 and C31 from VSYS to always-on 3V18, retain CFG2/TXLDO=2.7 V, disable the inapplicable TXLDO Check and remove the unimplemented VSYS threshold text. This removes the reviewed variable-VSYS premise. Conditional margin is `V3V18_min > 3.0 V` including regulator tolerance, DC load and transient droop. The added RF supply current must be included in the shared regulator/rail and input-source budget before that fix is considered closed. This disposition is recorded, not re-reviewed or claimed validated.
