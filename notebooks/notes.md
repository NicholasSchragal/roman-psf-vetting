# Roman CorGI Reference Star Vetting Notes

## Useful Links

- [Roman Reference Target Vetting List](https://docs.google.com/spreadsheets/d/1p5r0VmjBCjXU25daJl5oJOPoPh1V79nuESbnwmca0s0/edit#gid=0)
- [Simbad list of VOTable values](https://simbad.u-strasbg.fr/Pages/guide/sim-fscript.htx)
- [MagAO-X Instrument Handbook](https://magao-x.org/docs/handbook/index.html)
- [Washington Visual Double Star Catalog](https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=B/wds/wds)



## Roman CPP - Observation Planning WG Meeting Notes

### 2024-05-28

My Notes:

- Back channel observations through MagAO-X, LBTI, and SHARK-NIR
    - One of them is an obvious binary, was missed in initial vetting
- Gemini-South $\rho$ Pup & $\beta$ TrA speckle imaging
    - Imaging suggests no companions
    - Inner angle on imaging $0.1"$.
        - $\rho$ Pup $\rightarrow$ 1.945 AU
        - $\beta$ TrA $\rightarrow$ 1.2 AU

Other thoughts:

- Go through and look at TESS light curves for all reference star candidates to see if there is any behavior suggestive of unseen companions in the LCs.
- Maybe also go through and re-visit the catalogs for double stars (WDS, Tycho) and double-check we didn't accidentally include any known double stars?
- Justin is going to get me the MagAO-X data and maybe some CHARA data to start reducing from Alex Greenbaum.

## TESS Light Curve Inspection Notes (Based off CHARA List)

Re-dos needed on the following systems & results:
- HD23630:
    - 1
    - 2
- HD33111:
    - 4
    - 6
    - 7
    - 8
- HD67523:
    - 7
    - 10
    - 11
- HD102647:
    - 7
    - 12
    - 13
- HD108767:
    - 8
- HD112185:
    - 19
- HD186882:
    - 0
- HD197345:
    - 2

No light curves were found for the following systems:
- HD175191
- HD218045
- HD149757

### HD 432 ($\beta$ Cassiopeiae, Caph)
- Marked in table as "good?"
    - 2 companions at 66" and 344" according to WDS.
- 13 days between two dips that look suspiciously like eclipses present in the following QLP LCs, but not present in other LCs:
    - 2019 58764
    - 2019 58790
    - 2020 58955
    - [This paper](https://ui.adsabs.harvard.edu/abs/1989ApJ...343..916T/abstract) indicates that it has previously been thought that this was a spectroscopic binary.
        - It intimates that [this paper](https://ui.adsabs.harvard.edu/abs/1982PASP...94..317Y/abstract) proved that the 2km/s variation observed in the 1917 paper mentioned in its introduction along with the 60 years of RV observations indicated that there would not be a binary companion.
        - Assuming that this is correct, it would indicate the presence of a roughly $0.045\;M_{J}$ planet on that 27 day orbit.
- Star has a very apparant 0.1 day oscillation period and a roughly day-long rotational period.

### HD 8538 ($\delta$ Cassiopeiae)
- Marked in table as "good?"
    - 1 companion at 136" according to WDS.
- QLP LCs indicate a 12-13 day period of *something*, one shows a deep dip, the other shows very little. It's probably nothing and could very well be based on the comparison star(s) selected.
    - It is also possible, seeing that this happened in HD 432, that this is a flaw in QLP. It is very possible QLP should not be trusted.
- [This paper cataloging EBs](https://ui.adsabs.harvard.edu/abs/2006A%26A...446..785M/abstract) indicates this might be an EB with a period of 759 days. ([Catalog](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/A%2BA/446/785))
    - Verify that this is equivalent to the WDS quoted 136" separation at this distance and with the mass of the primary.

### HD 23630 ($\eta$ Tauri, Alcyone)
- Marked in table as "bad?"
    - Note from WDS of a possible lunar occultatin binary observed
    - [Kervella 2019](https://ui.adsabs.harvard.edu/abs/2019A%26A...623A..72K/abstract) ([Catalog](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/A+A/623/A72)) reports a tangential velocity anomaly of $3325\pm 1289\;m/s$.
    - Well known to have multiple large-separation companions as it is in the Pleiades.
- Looks like it's some sort of variable star with a period of 2.29-2.30 d (or possibly just 1.15 d?)

### HD 33111 ($\beta$ Eridani, Cursa)
- Marked in table as "bad?"
    - WDS known companion @ 118"
    - [Kervella 2022](https://ui.adsabs.harvard.edu/abs/2022A%26A...657A...7K/abstract) ([Catalogs](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/A+A/657/A7)) suggests a tangential velocity anomaly of $1326\pm 48\;m/s$
- TESS SPOC observations gave a max power in the periodogram at 0.95 days, unclear what that may be from.

### HD 35468 ($\gamma$ Orionis, Bellatrix)
- Marked in table as "good?"
    - WDS knwon companion @ 178"
    - [Bell 2017](https://ui.adsabs.harvard.edu/abs/2017MNRAS.468.1198B/abstract) states it may have an unseen companion. 
- Doesn't seem to be anyting in the LCs, they all have different periods at max power.

### HD 35497 ($\beta$ Tauri, Elnath)
- Has a variability period of around 2.76 days, unclear what kind of variable it is, but it's pretty well-behaved.

### HD 36673 ($\alpha$ Leporis, Arneb)
- Only has 1 QLP LC

### HD 58350 ($\eta$ Canis Majoris, Aludra)
- Not clear what kind of variable star this is, it may have multiple frequencies buried in it.

### HD 58715 ($\beta$ Canis Minoris, Gomeisa)
- If this has an extremely short-period companion, it's probably fairly light and only has a period of probably 0.62 days (period of max power of 0.31 days)
    - I do think, based on the amplitude and the fact that the phasing is inconsistent, it's unlikely.

### HD 67523 ($\rho$ Puppis, Tureis)
- $\delta$ Scuti variable, period 0.14 days, amplitude $\sim 20\textrm{ ppt}$.

### HD 87901 ($\alpha$ Leo, Regulus)
- Only QLP LC
- Uhhhh, it potentially has a White Dwarf secondary???
    - Yeah, on a 40 day orbit according to [Gies 2020](https://ui.adsabs.harvard.edu/abs/2020ApJ...902...25G/abstract)
    





