from gwf import Workflow

# prepare_input.py --vcf ../example/chimp_chr9_50.vcf --prefix ../example/tmp

# shapeit   --force                                                 \
#           --input-vcf ./example/tmp.vcf                           \
#           --input-map ./example/tmp_map.txt                       \
#           --output-max ./example/tmp.haps ./example/tmp.sample

## I will need this
## https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html#bed

# shapeit -B gwas-nomendel \
#         -M genetic_map.txt \
#         --duohmm \
#         --output-max gwas-duohmm \
#         --output-graph gwas-duohmm.graph

# ./duohmm -H duohmm-example \
#          -M genetic_map_chr10_combined_b37.txt \
#          -O duohmm-example-corrected
