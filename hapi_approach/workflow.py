from gwf import Workflow
import yaml
import os


def convert_vcf(vcf, prefix):

    inputs = [f'{vcf}']
    outputs = [f'{prefix}.dat', f'{prefix}.map', f'{prefix}.ped']
    options = {}
    spec = f'''
        python scripts/vcf_to_ped.py {vcf} --prefix {prefix}
    '''

    return inputs, outputs, options, spec


def run_hapi(hapi_exe, dat, _map, ped, out_dir):

    inputs = [f'{dat}', f'{_map}', f'{ped}']
    outputs = [f'{ped}.finished']
    options = {}
    spec = f'''
        {hapi_exe} -i {dat} {_map} {ped}    \
                   -d {out_dir}

        touch {ped}.finished
    '''

    return inputs, outputs, options, spec


def main(workflow):

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    project_dir = config['project_dir']
    chromosomes = config['chromosomes'].split(',')
    generic_input_vcf = config['generic_input_vcf']
    hapi_exe = config['hapi_exe']

    hapi_dir = f'{project_dir}/data_hapi_approach'
    os.makedirs(hapi_dir, mode=0o775, exist_ok=True)

    for _chr in chromosomes:
        input_vcf = generic_input_vcf.replace('CHROMOSOME', _chr)
        base = os.path.basename(input_vcf)

        chr_dir = f'{hapi_dir}/{_chr}'
        os.makedirs(chr_dir, mode=0o775, exist_ok=True)

        tmp = base.replace('.vcf', '')
        prefix = f'{chr_dir}/{tmp}'

        name = f'convert_vcf_{base}'
        template = convert_vcf(input_vcf, prefix)
        print(template[3].strip())
        workflow.target_from_template(name, template)

        dat, _map, ped = template[1]

        name = f'run_hapi_{base}'
        template = run_hapi(hapi_exe, dat, _map, ped, chr_dir)
        print(template[3].strip())
        workflow.target_from_template(name, template)


gwf = Workflow()
main(gwf)


# hapi approach
    # python vcf_to_ped.py --vcf chimp_chr9.PASS.vcf --prefix ./chimp_chr9
    # ./hapi-mr -i ../hapi_input/chimp_sub.dat ../hapi_input/chimp_sub.map ../hapi_input/chimp_sub.ped;