#!/bin/bash
# run on cluster with 'sbatch -p normal --mem=384g -c 36 gatk_command.sh'
# awk -F '\t' '{if($0 ~ /\#/) print; else if($7 == "PASS") print}' chimpanzees.chr9.vcf.gz.recalibrated_snps_raw_indels.vcf > chimp_chr9.PASS.vcf

INPUT=chimpanzees.chr9.vcf.gz

java \
      -Xmx32g \
      -jar /com/extra/GATK/LATEST/jar-bin/GenomeAnalysisTK.jar \
              -T ApplyRecalibration \
              -R chr9.fa \
              -input ${INPUT} \
              -mode SNP \
              --ts_filter_level 99.0 \
              -recalFile ${INPUT}.recal \
              -tranchesFile ${INPUT}.tranches \
              -o ${INPUT}.recalibrated_snps_raw_indels.vcf \
              -nt 16

