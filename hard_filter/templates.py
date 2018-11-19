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