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

    names = description.split()[9:]
    variants = []

    for i in range(len(names)):
        variants.append([])

    for record in records:
        record = record.split()

        chromosome = record[0]
        position = record[1]

        for i in range(len(names)):
            genotype = get_genotype(record[9+i])
            variants[i].append(genotype)

    for i in range(len(names)):
        print(names[i], variants[i])


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
    create_ped(description, records)


if __name__ == '__main__':
    main()
