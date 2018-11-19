from gwf import Workflow


def vcf_filter(vcf):
    chromosomes = 'chr1,chr2A,chr2B,chr3,chr4,chr5,chr6,chr7,chr8,chr9,chr10,' \
                  'chr11,chr12,chr13,chr14,chr15,chr16,chr17,chr18,chr19,chr20,chr21,chr22'
    filtered_vcf = vcf.replace('.vcf.gz', '') + '.filtered.vcf.gz'

    inputs = [f'{vcf}']
    outputs = [f'{filtered_vcf}']
    options = {}
    spec = f'''
        bcftools view   \
        -O z                `# output vcf.gz`   \
        -r {chromosomes}    `# regions`         \
        -v snps             `# select SNP`      \
        -m 2                `# min alleles 2`   \
        -M 2                `# max alleles 2`   \
        {vcf} > {filtered_vcf}
    '''

    return inputs, outputs, options, spec


def hard_filter(vcf, ref):
    out_vcf = vcf.replace('.vcf.gz', '.hf.vcf.gz')

    inputs = [f'{vcf}']
    outputs = [f'{out_vcf}']
    options = {}
    spec = f'''
        gatk \
            --java-options "-Xmx32G" \
            -T VariantFiltration                                                \
            -R {ref}    \
            -V {vcf}                                        \
            --filterExpression "QD < 2.0 || FS > 30.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -3.0 || ReadPosRankSum > 3 || DP < 250 || DP > 900" \ 
            --filterName "hard_filter" \ 
            -o {out_vcf}
            -nt 36
    '''

    return inputs, outputs, options, spec


input_data = '../../data_raw/chimp.raw.vcf.gz'
reference = '/project/MutationRates/NewVariantCalling/ref-genomes/panTro5.fa'

