# Demux reads

Demultiplex BD^2^ pilot data.

Demultiplex basecalled data using Dorado demux with a [custom barcode
configuration](https://software-docs.nanoporetech.com/dorado/latest/barcoding/custom_barcodes/) specified using an arrangement
and sequences fasta.

Although basecalling for the data was successful, demultiplexing failed using standard
demultiplexing (by jusyt specifying the kit used).
Thus, we do our own demultiplexing.

This workflow demuxes the basecalled fastq reads in a given directory
(specified by `reads_dir` in config), computes statistics on demuxed reads (no. of reads, N50 etc.)
and places the demultiplexed reads into seperate subdirectories for each barcode within
the specified output directory.

## Workflow overview

The workflow demultiplexes basecalled reads in a directory using `dorado demux`
and computes statistics on the demultiplexed fastq's using `seqkit stats`.

If it is desired to run/test the workflow on a sample of basecalled reads,
the workflow also aggreagtes all basecalled reads in the read directory and creates
a subsample.

1. Aggregate the original demultiplexed reads output of the sequencer.
2. Subsample to N reads.
3. Demultiplex the basecalled reads
4. Compute statistics on demultiplexed reads.
5. Copy the demultiplexed reads to specified output directory (in config) with seperate subdirectories for each barcode

```
out_dir/
    ├── barcode01/
    │     └── ...barcode01.fastq
    ├── barcode02/
    │     └── ...barcode02.fastq
    └── ...
```

For full dataset workflow proceeds from step 3.

## Running the workflow on BMRC

### Input data

1. *Read directory:* Path to directory of attempted demultiplexed reads by the sequencer using standard dorado demux configuration.
2. *Barcode configuration:* Barcode arrangement TOML and FASTQ.

### Running the workflow on full dataset

1. Get an interactive node:

```bash
srun --mem=32G --cpus-per-task=8 --time=24:00:00 --pty bash
```

2. Load Snakemake and launch the workflow:

```bash
module load snakemake
snakemake -c all --resources mem_mb=32000
```

### Running the workflow on a test dataset

To run it on a test dataset of basecalled reads downsampled to `N` reads,
change the input of `dorado_demux` rule by uncommenting the relevant line.

## Workflow output

The following output (subdirectories) are produced within the `results` directory
1. *merged_reads:* Aggregated reads across specified input directory
2. *sample_reads:* Subsample of merged reads
3. *dorado_demux:* Output of dorado demux (demultiplexed fastq's)
4. *seqkit_stats:* Statistics table of demultiplexed read fastqs.
5. *output_reads:* Output directory of demultiplexed reads with subdirectories for
   each barcode containing the reads fastq for the corresponding barcode

## Post workflow (run on laptop)

Use the quarto markdown located in `report` to generate a report
from demutiplexing stats and sample metadata.
