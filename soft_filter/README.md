# filtering

wget https://github.com/broadinstitute/gatk/releases/download/4.0.11.0/gatk-4.0.11.0.zip
unzip gatk-4.0.11.0.zip

#!/bin/bash

source /com/extra/bcftools/LATEST/load.sh

bcftools view   \
    -O z                                                                                                                                    `# output vcf.gz`   \
    -r chr1,chr10,chr11,chr12,chr13,chr14,chr15,chr16,chr17,chr18,chr19,chr20,chr21,chr22,chr2A,chr2B,chr3,chr4,chr5,chr6,chr7,chr8,chr9    `# regions`         \
    -v snps                                                                                                                                 `# select SNP`      \
    -m 2                                                                                                                                    `# min alleles 2`   \
    -M 2                                                                                                                                    `# max alleles 2`   \
    ../data_raw/chimp.known.vcf.gz > chimp.known.filtered.vcf.gz

bcftools view   \
    -O z                                                                                                                                    `# output vcf.gz`   \
    -r chr1,chr10,chr11,chr12,chr13,chr14,chr15,chr16,chr17,chr18,chr19,chr20,chr21,chr22,chr2A,chr2B,chr3,chr4,chr5,chr6,chr7,chr8,chr9    `# regions`         \   
    -v snps                                                                                                                                 `# select SNP`      \   
    -m 2                                                                                                                                    `# min alleles 2`   \   
    -M 2                                                                                                                                    `# max alleles 2`   \   
    ../data_raw/chimp.raw.vcf.gz > chimp.raw.filtered.vcf.gz

source /com/extra/tabix/LATEST/load.sh

tabix -p vcf chimp.raw.filtered.vcf.gz
tabix -p vcf chimp.known.filtered.vcf.gz

less chimp.raw.filtered.vcf.gz | grep -v "^#" | cut -f1 | uniq -c > chimp.raw.filtered.chrom
less chimp.known.filtered.vcf.gz | grep -v "^#" | cut -f1 | uniq -c > chimp.known.filtered.chrom

sbatch -p normal --mem=384g -c 36 -t 18000 VariantRecalibrator.sh

