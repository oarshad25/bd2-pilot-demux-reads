#!/usr/bin/env python3

# Inspect positions of barcode/RC/masks inside reads

# It prints where the forward barcode, its RC and the four masks are found (first 200 reads)
# so we can see whether barcodes are near the start/end or internal.

from pathlib import Path
from collections import Counter

# variables
FASTQ = Path("results/dorado_demux/4711ffe3-b530-43e0-92b0-adc70229608b_NB96-custom_barcode21.fastq")
FASTA = Path("data/barcode_sequences.fa")
BARID = "CB21"

MASK1F = "GTTTTCCCAGTCACGAC"
MASK1R = "TTTCTGTTGGTGCTGATATTGC"
MASK2F = "GAAGATAGAGCGACAGGCAAGT"
MASK2R = "GTCATAGCTGTTTCCTG"

# load barcode
barseq=None
with FASTA.open() as fh:
    name=None
    for line in fh:
        line=line.strip()
        if not line: continue
        if line.startswith(">"):
            name=line[1:].strip()
        else:
            if name==BARID:
                barseq=line.strip()
                break
if barseq is None:
    raise SystemExit(f"Barcode {BARID} not found in {FASTA}")

rc = barseq[::-1].translate(str.maketrans("ACGT","TGCA"))
print(f"Barcode {BARID}: {barseq}  RC: {rc}\n")

counts = Counter()
examples = []
with FASTQ.open() as fh:
    read_idx=0
    while read_idx < 200:
        h = fh.readline().strip()
        if not h:
            break
        s = fh.readline().strip()
        _ = fh.readline()
        _ = fh.readline()
        read_idx += 1
        def pos(seq, sub):
            p = seq.find(sub)
            return p+1 if p>=0 else None
        p_bar = pos(s, barseq)
        p_rc  = pos(s, rc)
        p_m1f = pos(s, MASK1F)
        p_m1r = pos(s, MASK1R)
        p_m2f = pos(s, MASK2F)
        p_m2r = pos(s, MASK2R)
        if p_bar: counts['bar_fwd'] += 1
        if p_rc:  counts['bar_rc'] += 1
        if p_m1f: counts['m1f'] += 1
        if p_m1r: counts['m1r'] += 1
        if p_m2f: counts['m2f'] += 1
        if p_m2r: counts['m2r'] += 1
        if len(examples) < 30:
            examples.append({'i':read_idx,'len':len(s),'bar':p_bar,'rc':p_rc,'m1f':p_m1f,'m1r':p_m1r,'m2f':p_m2f,'m2r':p_m2r})
print("Presence in first up to 200 reads:")
for k in ['bar_fwd','bar_rc','m1f','m1r','m2f','m2r']:
    print(f"  {k}: {counts[k]}")
print("\nSample positions (first up to 30 reads):")
for ex in examples:
    print(f"read#{ex['i']:3d} len={ex['len']:3d}  bar={ex['bar']!s:>3}  rc={ex['rc']!s:>3}  m1f={ex['m1f']!s:>3} m1r={ex['m1r']!s:>3}  m2f={ex['m2f']!s:>3} m2r={ex['m2r']!s:>3}")
