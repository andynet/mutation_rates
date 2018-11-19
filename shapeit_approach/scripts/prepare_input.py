import argparse


def get_lines(line):
    chr_, pos, id_, ref, alt, qlt, filter_, info, format_ = line.split()[0:9]
    individuals = line.split()[9:]

    qlt, filter_, info, format_ = '.', 'PASS', '.', 'GT'

    for i, individual in enumerate(individuals):
        individuals[i] = individual.split(':')[0]

    ind_str = '\t'.join(individuals)
    vcf_line = f'{chr_}\t{pos}\t{id_}\t{ref}\t{alt}\t{qlt}\t{filter_}\t{info}\t{format_}\t{ind_str}\n'
    map_line = f'{pos} {1.0} {int(pos)/1000000}\n'

    return vcf_line, map_line


def main():
    parser = argparse.ArgumentParser(description='Prepare input for shapeit')
    parser.add_argument('--vcf', required=True)
    parser.add_argument('--prefix', required=True)
    args = parser.parse_args()

    with open(args.vcf) as f:
        lines = f.readlines()

    vcf_out = ['##fileformat=VCFv4.1\n']
    map_out = ['position COMBINED_rate(cM/Mb) Genetic_Map(cM)\n']

    for line in lines:
        if line.startswith('#CHROM'):
            vcf_out.append(line)
        if not line.startswith('#'):
            vcf_line, map_line = get_lines(line)
            vcf_out.append(vcf_line)
            map_out.append(map_line)

    with open(f'{args.prefix}.vcf', 'w') as f:
        f.writelines(vcf_out)

    with open(f'{args.prefix}_map.txt', 'w') as f:
        f.writelines(map_out)


if __name__ == '__main__':
    main()
