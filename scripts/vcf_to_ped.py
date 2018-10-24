#!/usr/bin/python3

import argparse


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


def create_ped(description, records):

    result = []

    names = description.split()[9:]
    IDs = []
    variants = []

    for i in range(len(names)):
        variants.append([])

    for record in records:
        record = record.split()

        chromosome = record[0]
        position = record[1]

        ID = f'{chromosome}_{position}'
        IDs.append(ID)

        for i in range(len(names)):
            genotype = get_genotype(record[9+i])
            variants[i].append(genotype)

    IDs_str = '\t'.join(IDs)
    result.append(f'#Family\tChild\tFather\tMother\tChild_Gender\t{IDs_str}\n')
    for i in range(len(names)):
        variants_str = '\t'.join(variants[i])
        result.append(f'fam\t{names[i]}\t0\t0\t0\t{variants_str}\n')

    return result, IDs


def create_dat(ids):

    result = []
    for i in range(len(ids)):
        result.append(f'M\t{ids[i]}\n')

    return result


def create_map(ids):

    result = []
    for i in range(len(ids)):
        chromosome, distance = ids[i].split('_')[0:2]
        result.append(f'{chromosome[3:]}\t{ids[i]}\t{int(distance)/1000000}\n')

    return result


def read_vcf(file_name):

    description = None
    records = []

    with open(file_name) as f:
        for line in f:

            if line[0:2] != '##':
                if line[0] == '#':
                    description = line.strip()
                else:
                    records.append(line.strip())

    return description, records


def main():
    parser = argparse.ArgumentParser(description='Convert vcf file to ped')
    parser.add_argument('--vcf', required=True)
    args = parser.parse_args()

    description, records = read_vcf(args.vcf)
    ped_lines, marker_IDs = create_ped(description, records)
    dat_lines = create_dat(marker_IDs)
    map_lines = create_map(marker_IDs)

    with open('../tmp.ped', 'w') as f:
        f.writelines(ped_lines)

    with open('../tmp.dat', 'w') as f:
        f.writelines(dat_lines)

    with open('../tmp.map', 'w') as f:
        f.writelines(map_lines)


if __name__ == '__main__':
    main()
