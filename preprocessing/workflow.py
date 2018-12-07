from gwf import Workflow
import yaml
import os


def prepare_fasta(_in, chr_regexp, out):

    fa_dict = out.replace('.fa', '.dict')

    inputs = [_in]
    outputs = [out, fa_dict, f'{out}.fai']
    options = {'memory': '16g', 'walltime': '1440'}
    spec = f'''
    
        less {_in} | seqkit grep -r -p '{chr_regexp}' > {out}
        # picard CreateSequenceDictionary -R {out} -O {fa_dict}
        # samtools faidx {out}

    '''

    return inputs, outputs, options, spec


def prepare_vcf(_in, chr_str, out):

    filtered = out.replace('pure', 'filtered')

    inputs = [_in]
    outputs = [out, f'{out}.tbi']
    options = {'memory': '16g', 'walltime': '1440'}
    spec = f'''
        bcftools view   \
            -O z                                                            `# output vcf.gz`               \
            -r {chr_str}                                                       `# regions`                     \
            -v snps                                                         `# select SNP`                  \
            -m 2                                                            `# min alleles 2`               \
            -M 2                                                            `# max alleles 2`               \
            -g ^miss                                                        `# exclude missing genotypes`   \
            {_in} > {filtered}

        less {filtered} | grep -P '##fileformat|##FILTER|##FORMAT|##INFO|#CHROM|^chr' | bgzip -c > {out}
        
        tabix -p vcf {out}
    '''

    return inputs, outputs, options, spec


def main(workflow):

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    project_dir = config['project_dir']
    reference = config['reference']
    chromosomes = config['chromosomes']
    vcfs = config['vcfs']

    out_dir = f'{project_dir}/data_preprocessing'
    os.makedirs(out_dir, mode=0o775, exist_ok=True)

    chr_regexp = '^{}$'.format('$|^'.join(chromosomes))
    out = f'{out_dir}/chimp.pp.ref.fa'

    name = 'prepare_fasta'
    template = prepare_fasta(reference, chr_regexp, out)
    workflow.target_from_template(name, template)

    for vcf in vcfs:

        base = os.path.basename(vcf)
        out = '{}/{}'.format(out_dir, base.replace('.vcf.gz', '.pure.vcf.gz'))
        chr_str = ','.join(chromosomes)

        name = f'prepare_vcf_{base}'
        template = prepare_vcf(vcf, chr_str, out)
        workflow.target_from_template(name, template)


gwf = Workflow()
main(gwf)
