def install_gatk(install_dir):
    inputs = [f'{install_dir}']
    outputs = [f'{install_dir}/gatk_success']
    options = {}
    spec = f'''
    wget https://github.com/broadinstitute/gatk/releases/download/4.0.11.0/gatk-4.0.11.0.zip
    unzip gatk-4.0.11.0.zip
    rm gatk-4.0.11.0.zip
    mv gatk-4.0.11.0 {install_dir}/gatk
    {install_dir}/gatk/gatk -h > {install_dir}/gatk_success
    '''

    return inputs, outputs, options, spec


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


def vcf_tabix(vcf):
    inputs = [f'{vcf}']
    outputs = [f'{vcf}.tbi']
    options = {}
    spec = f"""
        tabix -p vcf {vcf}
    """
    return inputs, outputs, options, spec


def run_variant_recalibrator(callset, resourceset, reference, gatk_path, out_prefix):
    inputs = [f'{callset}', f'{resourceset}']
    outputs = [f'{out_prefix}.recal']
    options = {'memory': '36G', 'walltime': '18000'}
    spec = f"""
        {gatk_path}                                                                         \
            --java-options "-Xmx36G"                                                        \
            -T VariantRecalibrator                                                          \
            -R {reference}                                                                  \
            -input {callset}                                                                \
            -resource:chimp,known=true,training=true,truth=true,prior=15.0 {resourceset}    \
            -an DP -an QD -an FS -an SOR -an MQ -an MQRankSum -an ReadPosRankSum            \
            -mode SNP                                                                       \
            -tranche 100.0 -tranche 99.9 -tranche 99.0 -tranche 90.0                        \
            -recalFile {out_prefix}.recal                                                   \
            -tranchesFile {out_prefix}.tranches                                             \
            -rscriptFile {out_prefix}_plots.R                                               \
            -nt 36
    """
    return inputs, outputs, options, spec


def apply_recalibration(gatk_path, callset, reference, recal, tranches, out_vcf):
    inputs = []
    outputs = []
    options = {}
    spec = f"""
        {gatk_path}                     \
            --java-options "-Xmx36G"    \
            -T ApplyRecalibration       \
            -R {reference}              \
            -input {callset}            \
            -mode SNP                   \
            --ts_filter_level 99.0      \
            -recalFile {recal}          \
            -tranchesFile {tranches}    \
            -o {out_vcf}                \
            -nt 36
    """
    return inputs, outputs, options, spec
