from gwf import Workflow
import yaml
import os


def convert_vcf_to_bim(vcf, prefix):

    tmp = vcf.replace('.gz', '')

    inputs = [f'{vcf}']
    outputs = [f'{prefix}.bed', f'{prefix}.bim', f'{prefix}.fam']
    options = {}
    spec = f'''
        bgzip -cd {vcf} > {tmp}
        plink2 --vcf {tmp} --out {prefix}
    '''

    return inputs, outputs, options, spec


def main(workflow):

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    project_dir = config['project_dir']
    chromosomes = config['chromosomes'].split(',')
    generic_input_vcf = config['generic_input_vcf']
    shapeit_exe = config['shapeit_exe']
    pedigree = config['pedigree']

    shapeit_dir = f'{project_dir}/data_shapeit'
    os.makedirs(shapeit_dir, mode=0o775, exist_ok=True)

    for _chr in chromosomes:
        input_vcf = generic_input_vcf.replace('CHROMOSOME', _chr)
        base = os.path.basename(input_vcf)

        chr_dir = f'{shapeit_dir}/{_chr}'
        os.makedirs(chr_dir, mode=0o775, exist_ok=True)

        tmp = base.replace('.vcf.gz', '')
        prefix = f'{chr_dir}/{tmp}'

        name = f'convert_vcf_to_bim{base}'
        template = convert_vcf_to_bim(input_vcf, prefix)
        workflow.target_from_template(name, template)

        bed, bim, fam = template[1]

        # name = f'insert_pedigree_{base}'
        # template = insert_pedigree(ped, pedigree, connected_ped)
        # workflow.target_from_template(name, template)
        #
        # name = f'run_hapi_{base}'
        # template = run_hapi(hapi_exe, dat, _map, connected_ped, chr_dir)
        # workflow.target_from_template(name, template)


gwf = Workflow()
main(gwf)

from gwf import Workflow

# prepare_input.py --vcf ../example/chimp_chr9_50.vcf --prefix ../example/tmp

# shapeit   --force                                                 \
#           --input-vcf ./example/tmp.vcf                           \
#           --input-map ./example/tmp_map.txt                       \
#           --output-max ./example/tmp.haps ./example/tmp.sample

## I will need this
## https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html#bed

# shapeit -B gwas-nomendel \
#         -M genetic_map.txt \
#         --duohmm \
#         --output-max gwas-duohmm \
#         --output-graph gwas-duohmm.graph

# ./duohmm -H duohmm-example \
#          -M genetic_map_chr10_combined_b37.txt \
#          -O duohmm-example-corrected

# shapeit approach
    # plink2 --vcf chimp_chr9.PASS.vcf --out file
    # shapeit --input-bed file.bed file.bim file.fam \
    #         --input-map file.gmap \
    #         --duohmm \
    #         --output-max gwas-duohmm \
    #         --output-graph gwas-duohmm.graph