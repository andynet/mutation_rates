from gwf import Workflow
from templates import *
import json

# change to yaml
config = json.load(open('config.json'))
gwf = Workflow()


def filter_and_index(data):

    tmp = vcf_filter(data)
    gwf.target_from_template(f'vcf_filter.{data}', tmp)
    out = tmp[1][0]

    tmp = vcf_tabix(out)
    gwf.target_from_template(f'vcf_tabix.{out}', tmp)

    return out


# filter and index raw data
out1 = filter_and_index(config['raw_vcf'])
out2 = filter_and_index(config['known_vcf'])
reference = config['reference']

gwf.target_from_template('install_gatk', install_gatk(config['install_dir']))

var_rec = run_variant_recalibrator(callset=out1, resourceset=out2, reference=reference)
gwf.target_from_template('run_variant_recalibrator', var_rec)

tmp2 = apply_recalibration(gatk_path, callset, reference, recal, tranches, out_vcf)
gwf.target_from_template('apply_recalibration', tmp2)

# awk -F '\t' '{if($0 ~ /\#/) print; else if($7 == "PASS") print}'
#       chimpanzees.chr9.vcf.gz.recalibrated_snps_raw_indels.vcf > chimp_chr9.PASS.vcf
# bgzip -c chimp_chr9.PASS.vcf > chimp_chr9.PASS.vcf.gz

# hapi approach
# python vcf_to_ped.py --vcf chimp_chr9.PASS.vcf --prefix ./chimp_chr9
# ./hapi-mr -i ../hapi_input/chimp_sub.dat ../hapi_input/chimp_sub.map ../hapi_input/chimp_sub.ped;

# shapeit approach
# plink2 --vcf chimp_chr9.PASS.vcf --out file
# shapeit --input-bed file.bed file.bim file.fam \
#         --input-map file.gmap \
#         --duohmm \
#         --output-max gwas-duohmm \
#         --output-graph gwas-duohmm.graph
