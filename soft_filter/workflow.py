from gwf import Workflow
import yaml
import os


def run_variant_recalibrator(ref, call, res, out):

    inputs = [f'{ref}', f'{call}', f'{res}']
    outputs = [f'{out}.recal', f'{out}.tranches', f'{out}_plots.R']
    options = {'memory': '32G', 'walltime': '18000'}
    spec = f'''
        source /com/extra/GATK/LATEST/load.sh
        
        gatk \
            --java-options "-Xmx32G"                                                \
            -T VariantRecalibrator                                                  \
            -R {ref}                                                                \
            -input {call}                                                           \
            -resource:chimp,known=true,training=true,truth=true,prior=15.0 {res}    \
            -an DP -an QD -an FS -an SOR -an MQ -an MQRankSum -an ReadPosRankSum    \
            -mode SNP                                                               \
            -tranche 100.0 -tranche 99.9 -tranche 99.0 -tranche 90.0                \
            -recalFile {out}.recal                                                  \
            -tranchesFile {out}.tranches                                            \
            -rscriptFile {out}_plots.R                                              \
            -nt 64
    '''

    return inputs, outputs, options, spec


def apply_recalibration(ref, call, recal, tranch, out):

    inputs = [f'{ref}', f'{call}', f'{recal}', f'{tranch}']
    outputs = [f'{out}.vcf']
    options = {'memory': '32G', 'walltime': '18000'}
    spec = f'''
        source /com/extra/GATK/LATEST/load.sh
        
        gatk \
            --java-options "-Xmx32G"    \
            -T ApplyRecalibration       \
            -R {ref}                    \
            -input {call}               \
            -mode SNP                   \
            --ts_filter_level 99.0      \
            -recalFile {recal}          \
            -tranchesFile {tranch}      \
            -o {out}.vcf                \
            -nt 64
    '''

    return inputs, outputs, options, spec


def select_passed(_in, out):

    tmp = out.replace('.gz', '')

    inputs = [f'{_in}']
    outputs = [f'{out}']
    options = {}
    spec = f'''
        awk -F "\t" "{{if($0 ~ /\#/) print; else if($7 == "PASS") print}}"
            {_in} > {tmp}
            
        bgzip -c {tmp} > {out}
    '''

    return inputs, outputs, options, spec


def main():

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    gwf = Workflow()
    project_dir = config['project_dir']
    call_set = config['call_set']
    resource_set = config['resource_set']
    reference = config['reference']

    out_dir = f'{project_dir}/data_soft_filter'
    os.makedirs(out_dir, mode=0o775, exist_ok=True)
    out = f'{out_dir}/chimp'

    name = f'run_variant_recalibrator_{call_set}'
    template = run_variant_recalibrator(reference, call_set, resource_set, out)
    gwf.target_from_template(name, template)

    recal, tranch, plot = template[1]

    name = f'apply_recalibration_{call_set}'
    template = apply_recalibration(reference, call_set, recal, tranch, out)
    gwf.target_from_template(name, template)

    out, = template[1]

    name = f'select_passed_{out}'
    template = select_passed()
    gwf.target_from_template(name, template)

    # split to chromosomes?


if __name__ == '__main__':
    main()
