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


def run_hapi(hapi_exe, dat, _map, ped):

    inputs = [f'{dat}', f'{_map}', f'{ped}']
    outputs = [f'{ped}.finished']
    options = {}
    spec = f'''
        {hapi_exe} -i {dat} {_map} {ped}
        touch {ped}.finished
    '''

    return inputs, outputs, options, spec


def main(workflow):

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    project_dir = config['project_dir']
    input_vcf = config['input_vcf']
    base = os.path.basename(input_vcf)
    hapi_exe = config['hapi_dir']
    hapi_dir = f'{project_dir}/data_hapi_approach'
    os.makedirs(hapi_dir, mode=0o775, exist_ok=True)

    tmp = base.replace('.vcf', '')
    prefix = f'{hapi_dir}/{tmp}'

    name = f'convert_vcf_{base}'
    template = convert_vcf(input_vcf, prefix)
    workflow.target_from_template(name, template)

    dat, _map, ped = template[1]

    name = f'run_hapi_{base}'
    template = run_hapi(hapi_exe, dat, _map, ped)
    workflow.target_from_template(name, template)


gwf = Workflow()
main(gwf)


# hapi approach
    # python vcf_to_ped.py --vcf chimp_chr9.PASS.vcf --prefix ./chimp_chr9
    # ./hapi-mr -i ../hapi_input/chimp_sub.dat ../hapi_input/chimp_sub.map ../hapi_input/chimp_sub.ped;