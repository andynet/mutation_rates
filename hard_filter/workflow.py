from gwf import Workflow
import yaml
import os


def hard_filter(in_vcf, ref, out_vcf):

    _filter = 'QD < 2.0 || FS > 30.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -3.0 || ReadPosRankSum > 3 || DP < 250 || DP > 900'

    inputs = [f'{in_vcf}', f'{ref}']
    outputs = [f'{out_vcf}']
    options = {}
    spec = f'''
        source /com/extra/GATK/LATEST/load.sh
        
        java \
            -Xmx32G \
            -jar /com/extra/GATK/LATEST/jar-bin/GenomeAnalysisTK.jar \
                -T VariantFiltration            \
                -R {ref}                        \
                -V {in_vcf}                     \
                --filterExpression "{_filter}"  \
                --filterName "hard_filter"      \
                -o {out_vcf}
    '''

    return inputs, outputs, options, spec


def select_passed(_in, out):
    tmp = out.replace('.gz', '')

    inputs = [f'{_in}']
    outputs = [f'{out}']
    options = {}
    spec = f'''
        less {_in} \
            | awk -F '\t' '{{if($0 ~ /\#/) print; else if($7 == "PASS") print}}' \
            > {tmp}

        bgzip -c {tmp} > {out}
    '''

    return inputs, outputs, options, spec


def vcf_tabix(vcf):
    inputs = [f'{vcf}']
    outputs = [f'{vcf}.tbi']
    options = {}
    spec = f"""
        tabix -p vcf {vcf}
    """
    return inputs, outputs, options, spec


def extract_chromosome(_in, out, chromosome):
    inputs = [f'{_in}', f'{_in}.tbi']
    outputs = [f'{out}']
    options = {}
    spec = f'''
        bcftools view   \
        -O z            \
        -r ^{chromosome}$      \
        {_in} > {out}
    '''

    return inputs, outputs, options, spec


def main(workflow):
    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    project_dir = config['project_dir']
    input_vcf = config['input_vcf']
    base = os.path.basename(input_vcf)
    reference = config['reference']

    out_dir = f'{project_dir}/data_hard_filter'
    os.makedirs(out_dir, mode=0o775, exist_ok=True)
    output_vcf = f'{out_dir}/{base}'

    name = f'hard_filter_{base}'
    template = hard_filter(input_vcf, reference, output_vcf)
    workflow.target_from_template(name, template)

    _in = output_vcf
    out = output_vcf.replace('.vcf.gz', '.PASS.vcf.gz')

    name = f'select_passed_{base}'
    template = select_passed(_in, out)
    workflow.target_from_template(name, template)

    name = f'tabix_{base}'
    template = vcf_tabix(out)
    workflow.target_from_template(name, template)

    _in = out
    split_dir = os.path.dirname(_in) + '/split'
    os.makedirs(split_dir, mode=0o755, exist_ok=True)
    chromosomes = 'chr1,chr2A,chr2B,chr3,chr4,chr5,chr6,chr7,chr8,chr9,chr10,chr11,' \
                  'chr12,chr13,chr14,chr15,chr16,chr17,chr18,chr19,chr20,chr21,chr22'

    for chromosome in chromosomes.split(','):

        out_file = os.path.basename(_in).replace('.PASS.vcf.gz', f'.{chromosome}.vcf.gz')
        out = '/'.join([split_dir, out_file])

        name = f'extract_chromosome_{out_file}'
        template = extract_chromosome(_in, out, chromosome)
        workflow.target_from_template(name, template)

        name = f'tabix_{out_file}'
        template = vcf_tabix(out)
        workflow.target_from_template(name, template)


gwf = Workflow()
main(gwf)
