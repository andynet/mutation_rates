import argparse


def main():

    parser = argparse.ArgumentParser(description='Insert relations to ped file')
    parser.add_argument('--ped', required=True)
    parser.add_argument('--pedigree', required=True)
    args = parser.parse_args()

    name2id = None
    id2family, id2father, id2mother, id2gender = None, None, None, None


if __name__ == '__main__':
    main()
