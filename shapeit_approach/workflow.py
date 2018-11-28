from gwf import Workflow
import yaml
import os


def convert_vcf_to_bim(vcf, prefix):

    tmp = vcf.replace('.gz', '')

    inputs = [f'{vcf}']
    outputs = [f'{prefix}.bed', f'{prefix}.bim', f'{prefix}.fam']
    options = {'memory': '8g'}
    spec = f'''
        bgzip -cd {vcf} > {tmp}
        plink2 --vcf {tmp} --out {prefix}
    '''

    return inputs, outputs, options, spec


def create_gmap(vcf, prefix):

    inputs = [f'{vcf}']
    outputs = [f'{prefix}.vcf', f'{prefix}_map.txt']
    options = {'memory': '8g'}
    spec = f'''
        python scripts/prepare_input.py --vcf {vcf} --prefix {prefix}
    '''

    return inputs, outputs, options, spec


def run_shapeit(shapeit_exe, bed, bim, fam, gmap, out):

    inputs = [f'{bed}', f'{bim}', f'{fam}', f'{gmap}']
    outputs = [f'{out}.graph']
    options = {}
    spec = f'''
        {shapeit_exe}   --input-bed {bed} {bim} {fam}   \
                        --input-map {gmap}              \
                        --duohmm                        \
                        --output-max {out}              \
                        --output-graph {out}.graph      \
                        --force
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
        input_vcf = input_vcf.replace('.gz', '')

        name = f'create_map_{base}'
        template = create_gmap(input_vcf, prefix)
        workflow.target_from_template(name, template)

        out = bed.replace('.bed', '')
        gmap = template[1][1]

        name = f'run_shapeit_{base}'
        template = run_shapeit(shapeit_exe, bed, bim, fam, gmap, out)
        workflow.target_from_template(name, template)


gwf = Workflow()
main(gwf)

# I will need this
# https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html#bed
