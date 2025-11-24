#!/usr/bin/env bash

# Count occurrences of barcode, RC and masks in reads assigned to barcode by demux

# --- set variables (edit only if your filenames differ) ---

# path to the FASTQ file with the reads assigned to the barcode
FASTQ="results/dorado_demux/4711ffe3-b530-43e0-92b0-adc70229608b_NB96-custom_barcode21.fastq"
# fasta of barcode sequences
FASTA="data/barcode_sequences.fa"
# id of barcode in barcode_sequences.fa
BARID="CB21"

# --- extract barcode sequence for BARID ---
BCSEQ=$(awk -v id="${BARID}" 'BEGIN{RS=">"} $0~id{n=split($0,a,"\n"); print a[2]; exit}' $FASTA)
echo "Barcode ${BARID}: $BCSEQ"

# --- counts: total assigned reads ---
TOTAL_LINES=$(wc -l < "$FASTQ")
READS=$((TOTAL_LINES/4))
echo "Assigned reads: $READS"

# --- exact barcode substring occurrences (forward) ---
MATCHES=$(awk -v seq="$BCSEQ" 'NR%4==2 { if (index($0, seq)>0) c++ } END{print c+0}' "$FASTQ")
echo "Exact barcode occurrences: $MATCHES"

# --- reverse complement of barcode and matches ---
RC=$(echo "$BCSEQ" | rev | tr 'ACGT' 'TGCA')
echo "RC: $RC"
RC_MATCHES=$(awk -v seq="$RC" 'NR%4==2 { if (index($0, seq)>0) c++ } END{print c+0}' "$FASTQ")
echo "RC occurrences: $RC_MATCHES"

# --- mask presence counts in assigned reads ---
MASK1F="GTTTTCCCAGTCACGAC"
MASK1R="TTTCTGTTGGTGCTGATATTGC"
MASK2F="GAAGATAGAGCGACAGGCAAGT"
MASK2R="GTCATAGCTGTTTCCTG"

for m in MASK1F MASK1R MASK2F MASK2R; do
  eval seq=\$$m
  cnt=$(awk -v seq="$seq" 'NR%4==2 { if (index($0, seq)>0) c++ } END{print c+0}' "$FASTQ")
  pct=0
  if [ "$READS" -gt 0 ]; then
    pct=$((100 * cnt / READS))
  fi
  echo "$m present in assigned reads: $cnt ($pct%)"
done

# --- summary line for convenience ---
echo "SUMMARY: assigned=$READS  exact_matches=$MATCHES  rc_matches=$RC_MATCHES"
