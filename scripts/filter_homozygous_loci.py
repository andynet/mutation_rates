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

        for k in range(len(loci)):
            variants[k].append(tmp[k])

    print(f'Filtered {polyallelic + homozygotic} ({polyallelic}/{homozygotic}) out of {loci_count} columns.')

    for i in range(len(result)):
        result[i] = result[i] + ' '.join(variants[i]) + '\n'

    return result


def filter_file(ped):

    result = []
    loci = []

    with open(ped) as f:
        lines = f.readlines()

    for line in lines:
        result.append('\t'.join(line.split('\t')[0:-1]))
        loci.append(line.split('\t')[-1])

    result = filter_loci(result, loci)

    return result


def main():

    parser = argparse.ArgumentParser(description='Convert vcf file to ped')
    parser.add_argument('--ped', required=True)
    args = parser.parse_args()

    new_ped_lines = filter_file(args.ped)
    save_lines('tmp_new.ped', new_ped_lines)


if __name__ == '__main__':
    main()