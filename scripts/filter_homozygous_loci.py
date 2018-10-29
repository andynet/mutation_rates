import argparse
import math


def save_lines(file, lines):
    with open(file, 'w') as f:
        f.writelines(lines)


def filter_loci(result, loci):

    for i in range(len(result)):
        result[i] += '\t'

    for i in range(len(loci)):
        loci[i] = loci[i].split()

    filtered_count = 0
    for i in range(len(loci[0])):
        tmp = []
        for j in range(len(loci)):
            tmp.append(loci[j][i])

        if len(set(tmp[1:])) == 1 and tmp[1].split('/')[0] == tmp[1].split('/')[1]:
            filtered_count += 1
        else:
            for k in range(len(loci)):
                result[k] = f'{result[k]}{tmp[k]} '

        if i % math.floor(math.sqrt(len(loci[0]))) == 0:
            print(f'Filtered {filtered_count} out of {i} columns.')

    print(f'Filtered {filtered_count} out of {i} columns.')
    
    for i in range(len(result)):
        result[i] += '\n'

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