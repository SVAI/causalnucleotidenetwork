import sys
import pandas as pd
from collections import defaultdict

def preproc(glist):
    ens_list = set([])
    with open(glist) as f:
        for line in f:
            ens = line.split(",")[1].strip()
            ens_list.add(ens)
    return ens_list

def filter_by_gene(matrix, ens_genes):
    with open('filtered_by_gene.tsv', 'w') as filtered:
        with open(matrix) as matr:
            # copy header
            filtered.write(matr.readline())
            # read the rest of the lines and filter by gene
            for line in matr:
                spl = line.split()
                gene = spl[0]
                if "." in gene:
                    final_g = gene.split(".")[0]
                else:
                    final_g = gene
                print final_g
                if final_g in ens_genes:
                    filtered.write("KIRP" + line + "\n")

# load data
kidney = sys.argv[1]
matrix = sys.argv[2]

# kidney mutated genes set
ens_genes = preproc(kidney)
print len(ens_genes)

# filter by gene
filter_by_gene(matrix, ens_genes)

# filter by tumor
df = pd.read_csv('filtered_by_gene.tsv', delimiter='\t')
print df.head(2)
filter_col = [col for col in df if col.startswith('KIRP') or col.startswith('ENSGRowID')]
print filter_col
print len(filter_col)
filtered_vals = df[filter_col]
filtered_vals.to_csv('filtered_by_gene_and_tumor.tsv', sep='\t', index=False)

