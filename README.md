# Mutation Rates

## Soft filtering
- filter variants using gatk VQSR

## Hard filtering
- filter variants using gatk VariantFiltration

## Hapi approach 
- searching recombination using hapi

## Shapeit approach
- searching recombination using shapeit

# envs
-bcftools
-tabix
-gwf

# to install
-gatk

```
wget https://github.com/broadinstitute/gatk/releases/download/4.0.11.0/gatk-4.0.11.0.zip
unzip gatk-4.0.11.0.zip
rm gatk-4.0.11.0.zip
mv gatk-4.0.11.0 {install_dir}/gatk
{install_dir}/gatk/gatk -h > {install_dir}/gatk_success
```

## Hapi
[hapi](http://hapi.csail.mit.edu/)

```
wget http://hapi.csail.mit.edu/hapi-1.03-x86_64.tgz
tar -xvzf hapi-1.03-x86_64.tgz
mv hapi-1.03-x86_64/ hapi
rm hapi-1.03-x86_64.tgz
```
