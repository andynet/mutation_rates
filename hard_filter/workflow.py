from gwf import Workflow
import yaml
import os


def hard_filter(in_vcf, ref, out_vcf):

    _filter = 'QD < 2.0 || FS > 30.0 || MQ < 40.0 || MQRankSum < -12.5 ' \
              '|| ReadPosRankSum < -3.0 || ReadPosRankSum > 3 || DP < 250 || DP > 900'

    inputs = [f'{in_vcf}', f'{ref}']
    outputs = [f'{out_vcf}']
    options = {}
    spec = f'''
        source /com/extra/GATK/LATEST/load.sh
        
        gatk \
            --java-options "-Xmx32G"        \
            -T VariantFiltration            \
            -R {ref}                        \
            -V {in_vcf}                     \
            --filterExpression {_filter}    \
            --filterName "hard_filter"      \
            -o {out_vcf}
    '''

    return inputs, outputs, options, spec


def main():

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    gwf = Workflow()
    project_dir = config['project_dir']
    input_vcf = config['input_vcf']
    base = os.path.basename(input_vcf)
    reference = config['reference']

    out_dir = f'{project_dir}/data_hard_filter'
    os.makedirs(out_dir, mode=0o775, exist_ok=True)
    output_vcf = f'{out_dir}/{base}'

    name = f'hard_filter_{base}'
    template = hard_filter(input_vcf, reference, output_vcf)
    gwf.target_from_template(name, template)


if __name__ == '__main__':
    main()
