import argparse
import sys
import os
import json


def save_lines(file, lines):
    with open(file, 'w') as f:
        f.writelines(lines)


def translate(genotype):
    first_allel, second_allel = genotype.split('/')

    try:
        first_allel = int(first_allel)+1
    except ValueError:
        first_allel = 0

    try:
        second_allel = int(second_allel)+1
    except ValueError:
        second_allel = 0

    return '{}/{}'.format(first_allel, second_allel)


def get_genotype(sample):

    sample = sample.split(':')
    genotype = translate(sample[0])

    return genotype


def create_files(cname2cnum, names, lines):

    ped = []
    map = []
    dat = []

    variants = []
    identifiers = []

    for i in range(len(names)):
        variants.append([])

    for line in lines:
        record = line.split()

        cname = record[0]
        cnum = cname2cnum[cname]
        position = record[1]
        identifiers.append(f'{cname}_{position}')

        map.append(f'{cnum} {identifiers[-1]}  {int(position)/1000000}\n')
        dat.append(f' M {identifiers[-1]}\n')

        for i in range(len(names)):
            genotype = get_genotype(record[9+i])
            variants[i].append(genotype)

    identifiers_str = '\t'.join(identifiers)
    ped.append(f'# Family\tChild\tFather\tMother\tChild_Gender  0\t{identifiers_str}\n')

    for i in range(len(names)):
        variant_str = ' '.join(variants[i])
        ped.append(f'1\t{names[i]}\t0\t0\t0  0\t{variant_str}\n')

    return ped, map, dat


def read_vcf(file_name):

    cname2cnum = dict()
    cnum = 1

    names = None
    lines = []

    with open(file_name) as f:
        for line in f:

            if line.startswith('##contig'):
                contig_name = line.split('<')[1].split(',')[0].split('=')[1]
                cname2cnum[contig_name] = cnum
                cnum += 1

            if line.startswith('#CHROM'):
                names = line.split()[9:]

            if not line.startswith('#'):
                lines.append(line.strip())

    return cname2cnum, names, lines


def main():

    parser = argparse.ArgumentParser(description='Convert vcf file to ped')
    parser.add_argument('--vcf', required=True)
    parser.add_argument('--prefix', required=True)
    args = parser.parse_args()

    # print(f'Running {os.environ["_"]} with parameters {sys.argv}')

    cname2cnum, names, lines = read_vcf(args.vcf)

    with open(f'{args.prefix}.cname2cnum.json', 'w') as f:
        json.dump(cname2cnum, f)

    ped_lines, map_lines, dat_lines = create_files(cname2cnum, names, lines)

    save_lines(f'{args.prefix}.ped', ped_lines)
    save_lines(f'{args.prefix}.map', map_lines)
    save_lines(f'{args.prefix}.dat', dat_lines)


if __name__ == '__main__':
    main()
