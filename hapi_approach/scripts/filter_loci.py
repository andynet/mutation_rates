import argparse
import math


def save_lines(file, lines):
    with open(file, 'w') as f:
        f.writelines(lines)


def is_homozygotic(site):
    if len(set(site)) == 1 and site[0].split('/')[0] == site[0].split('/')[1]:
        return True
    else:
        return False


def is_polyallelic(site):
    alleles = set('/'.join(site).split('/'))

    if '0' in alleles:
        # print('Site has unknown variant.')
        alleles.remove('0')

    if len(alleles) > 2:
        return True
    else:
        return False


def filter_loci(result, loci):

    for i in range(len(result)):
        result[i] += '\t'

    variants = []
    for i in range(len(loci)):
        loci[i] = loci[i].split()
        variants.append([])

    polyallelic = 0
    homozygotic = 0
    loci_count = len(loci[0])
    markers = []

    for i in range(loci_count):

        tmp = []
        for j in range(len(loci)):
            tmp.append(loci[j][i])

        if i % math.floor(math.sqrt(loci_count)) == 0:
            print(f'Filtered {polyallelic + homozygotic} ({polyallelic}/{homozygotic}) out of {i} columns.')

        if is_polyallelic(tmp[1:]):
            polyallelic += 1
            continue

        if is_homozygotic(tmp[1:]):
            homozygotic += 1
            continue

        markers.append(tmp[0])
        for k in range(len(loci)):
            variants[k].append(tmp[k])

    print(f'Filtered {polyallelic + homozygotic} ({polyallelic}/{homozygotic}) out of {loci_count} columns.')

    for i in range(len(result)):
        result[i] = result[i] + ' '.join(variants[i]) + '\n'

    return result, markers


def filter_ped(ped):

    result = []
    loci = []

    with open(ped) as f:
        lines = f.readlines()

    for line in lines:
        result.append('\t'.join(line.split('\t')[0:-1]))
        loci.append(line.split('\t')[-1])

    result, markers = filter_loci(result, loci)

    return result, markers


def filter_lines(file, markers):

    new_lines = []

    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        marker = line.strip().split()[1]
        if marker in markers:
            new_lines.append(line)

    return new_lines


def main():

    parser = argparse.ArgumentParser(description='Convert vcf file to ped')
    parser.add_argument('--dat', required=True)
    parser.add_argument('--map', required=True)
    parser.add_argument('--ped', required=True)
    parser.add_argument('--prefix', required=True)
    args = parser.parse_args()

    new_ped_lines, markers = filter_ped(args.ped)
    save_lines(f'{args.prefix}.ped', new_ped_lines)

    markers = set(markers)

    new_dat_lines = filter_lines(args.dat, markers)
    save_lines(f'{args.prefix}.dat', new_dat_lines)

    new_map_lines = filter_lines(args.map, markers)
    save_lines(f'{args.prefix}.map', new_map_lines)


if __name__ == '__main__':
    main()