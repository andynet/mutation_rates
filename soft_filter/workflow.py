from gwf import Workflow
import yaml
import os


def extract_chromosome(_in, out, chromosome):
    inputs = [f'{_in}', f'{_in}.tbi']
    outputs = [f'{out}', f'{out}.tbi']
    options = {}
    spec = f'''
            bcftools view   \
            -O z            \
            -r {chromosome} \
            {_in} > {out}

            tabix -p vcf {out}
        '''

    return inputs, outputs, options, spec


def run_variant_recalibrator(ref, call, res, out, gatk_exe):

    inputs = [f'{ref}', f'{call}', f'{res}']
    outputs = [f'{out}.recal', f'{out}.tranches', f'{out}_plots.R']
    options = {'memory': '16G', 'walltime': '18000'}
    spec = f'''

        export LD_LIBRARY_PATH="/com/extra/slurm/LATEST/lib64:/com/extra/slurm/LATEST/lib:"

        source /com/extra/java/8/load.sh
        source /com/extra/GATK/3.8/load.sh

        java                                                                            \
            -Xmx16g                                                                     \
            -jar /com/extra/GATK/LATEST/jar-bin/GenomeAnalysisTK.jar                    \
                -T VariantRecalibrator                                                  \
                -R {ref}                                                                \
                -input {call}                                                           \
                -resource:chimp,known=false,training=true,truth=true,prior=15.0 {res}   \
                -an DP -an QD -an FS -an SOR -an MQ -an MQRankSum -an ReadPosRankSum    \
                -mode SNP                                                               \
                -tranche 100.0 -tranche 99.9 -tranche 99.0 -tranche 90.0                \
                -recalFile {out}.recal                                                  \
                -tranchesFile {out}.tranches                                            \
                -rscriptFile {out}_plots.R                                              \
                -nt 16
    '''

    return inputs, outputs, options, spec


def apply_recalibration(ref, call, recal, tranch, out, gatk_exe):

    inputs = [f'{ref}', f'{call}', f'{recal}', f'{tranch}']
    outputs = [f'{out}.recalibrated.vcf']
    options = {'memory': '16G', 'walltime': '18000'}
    spec = f'''
        
        export LD_LIBRARY_PATH="/com/extra/slurm/LATEST/lib64:/com/extra/slurm/LATEST/lib:"

        source /com/extra/java/8/load.sh
        source /com/extra/GATK/3.8/load.sh

        java                                                                            \
            -Xmx16g                                                                     \
            -jar /com/extra/GATK/LATEST/jar-bin/GenomeAnalysisTK.jar                    \
            -T ApplyRecalibration       \
            -R {ref}                    \
            -input {call}               \
            -mode SNP                   \
            --ts_filter_level 99.0      \
            -recalFile {recal}          \
            -tranchesFile {tranch}      \
            -o {out}.recalibrated.vcf   \
            -nt 16
    '''

    return inputs, outputs, options, spec


def select_passed(_in, out):

    tmp = out.replace('.gz', '.tmp')

    inputs = [f'{_in}']
    outputs = [f'{out}']
    options = {}
    spec = f'''
        awk -F "\t" '{{if($0 ~ /\#/) print; else if($7 == "PASS") print}}'  \
            {_in} > {tmp}
            
        bgzip -c {tmp} > {out}
    '''

    return inputs, outputs, options, spec


def main(workflow):

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    project_dir = config['project_dir']
    call_set = config['call_set']
    resource_set = config['resource_set']
    reference = config['reference']
    chromosomes = config['chromosomes'].split(',')
    gatk_exe = None     # config['gatk_exe']

    out_dir = f'{project_dir}/data_soft_filter'
    os.makedirs(out_dir, mode=0o775, exist_ok=True)

    base = os.path.basename(call_set)

    for chromosome in chromosomes:

        chr_dir = f'{out_dir}/{chromosome}'
        os.makedirs(chr_dir, mode=0o755, exist_ok=True)

        out = f'{chr_dir}/{base}'
        name = f'extract_chromosome_{chromosome}'
        template = extract_chromosome(call_set, out, chromosome)
        workflow.target_from_template(name, template)

        chr_vcf, chr_tbi = template[1]
        out_base = out.replace('.vcf.gz', '')

        name = f'run_variant_recalibrator_{chromosome}'
        template = run_variant_recalibrator(reference, chr_vcf, resource_set, out_base, gatk_exe)
        gwf.target_from_template(name, template)

        recal, tranch, plot = template[1]

        name = f'apply_recalibration_{chromosome}'
        template = apply_recalibration(reference, chr_vcf, recal, tranch, out_base, gatk_exe)
        gwf.target_from_template(name, template)

        _in, = template[1]
        out = out.replace('.vcf.gz', '.recalibrated.vcf.gz')

        name = f'select_passed_{chromosome}'
        template = select_passed(_in, out)
        gwf.target_from_template(name, template)


gwf = Workflow(defaults = {'account': 'MutationRates'})
main(gwf)
