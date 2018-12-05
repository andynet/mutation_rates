from gwf import Workflow
import yaml
import os


def main(workflow):

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    project_dir = config['project_dir']
    reference = config['reference']
    chromosomes = config['chromosomes'].split(',')
    vcfs = config['vcfs']

    out_dir = f'{project_dir}/data_preprocessing'
    os.makedirs(out_dir, mode=0o775, exist_ok=True)


    # less ../data_raw/chimp.ref.fa | seqkit grep -r -p ${CHR_REG} > chimp.pp.ref.fa
    #
    # bcftools view   \
    #     -O z                                                            `# output vcf.gz`               \
    #     -r ${CHR}                                                       `# regions`                     \
    #     -v snps                                                         `# select SNP`                  \
    #     -m 2                                                            `# min alleles 2`               \
    #     -M 2                                                            `# max alleles 2`               \
    #     -g ^miss                                                        `# exclude missing genotypes`   \
    #     ../data_raw/chimp.known.vcf.gz > chimp.known.filtered.vcf.gz
    #
    # tabix -p vcf chimp.known.filtered.vcf.gz
    #
    # less chimp.raw.filtered.vcf.gz | grep -P '##fileformat|##FILTER|##FORMAT|##INFO|#CHROM|^chr' > chimp.raw.pure.vcf
    #
    # less chimp.raw.filtered.vcf.gz | grep -v "^#" | cut -f1 | uniq -c > chimp.raw.filtered.chrom
    #
    # source /com/extra/picard/LATEST/load.sh
    #
    # picard CreateSequenceDictionary R=chimp.pp.ref.fa O=chimp.pp.ref.dict
    #
    # source /com/extra/samtools/LATEST/load.sh
    #
    # samtools faidx chimp.pp.ref.fa

gwf = Workflow()
main(gwf)