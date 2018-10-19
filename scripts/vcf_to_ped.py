#!/usr/bin/python3

import argparse


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


if __name__ == '__main__':
    main()
