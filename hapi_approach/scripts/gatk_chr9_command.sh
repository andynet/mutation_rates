#!/bin/bash

# preparation:
#     input:
#         chimpanzees.chr9.vcf.gz
#         chimpanzees.chr9.vcf.gz.tbi
#         known_chimp.chr9.vcf.gz
#         known_chimp.chr9.vcf.gz.tbi
#         chr9.fa
#         chr9.fai
#         chr9.dict
#
# run on cluster with 'sbatch -p normal --mem=384g -c 36 gatk_command.sh'
# vcftools --vcf myvcf.vcf --plink --out myplink

INPUT=chimpanzees.chr9.vcf.gz

java \
	-Xmx32g \
	-jar /com/extra/GATK/LATEST/jar-bin/GenomeAnalysisTK.jar \
		-T VariantRecalibrator 	\
		-R chr9.fa \
		-input ${INPUT} \
		-resource:chimp,known=false,training=true,truth=true,prior=15.0 known_chimp.chr9.vcf.gz \
		-an DP \
		-an QD \
		-an FS \
		-an SOR \
		-an MQ \
		-an MQRankSum \
		-an ReadPosRankSum \
		-an InbreedingCoeff \
		-mode SNP \
		-tranche 100.0 -tranche 99.9 -tranche 99.0 -tranche 90.0 \
		-recalFile ${INPUT}.recal \
		-tranchesFile ${INPUT}.tranches \
		-rscriptFile ${INPUT}_plots.R \
		-nt 16 

# java \
# 	-Xmx32g \
# 	-jar /com/extra/GATK/LATEST/jar-bin/GenomeAnalysisTK.jar \
#         	-T ApplyRecalibration \
#        	-R /project/MutationRates/NewVariantCalling/ref-genomes/panTro5.fa \
#         	-input ${INPUT} \
#        	-mode SNP \
#         	--ts_filter_level 99.0 \
#         	-recalFile ${INPUT}.recal \
#         	-tranchesFile ${INPUT}.tranches \
#         	-o ${INPUT}.recalibrated_snps_raw_indels.vcf \
# 		-nt 16

