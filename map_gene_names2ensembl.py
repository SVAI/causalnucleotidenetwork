import sys
from collections import defaultdict

def get_mapping(mapp):
    gmap = defaultdict(set)
    with open(mapp) as f:
        f.readline()
        for l in f:
            if len(l.split(",")) != 6:
                print(l)
                #sys.exit()
            # Gene stable ID,Transcript stable ID,HGNC symbol,Chromosome/scaffold name,Gene start (bp),Gene end (bp)
            gene_id, transcript, hgnc, chrom_name, gene_start, gene_end = l.split(",")
            if len(hgnc) > 0:
                if hgnc in gmap and gene_id not in gmap[hgnc]:
                    #print("Multiple hgnc: {}, {}, {}".format(gene_id, gmap[hgnc], hgnc))
                    pass
                gmap[hgnc].add(gene_id)
    return gmap

def map_cancer_genes(cancer_file, gmap):
    cancer_gmap = {}
    with open(cancer_file) as f:
        f.readline()
        for l in f:
            if len(l.split()) != 4:
                print(l)
                #sys.exit()
            hgnc, mut, num, freq = l.split() 
            if hgnc in gmap:
                cancer_gmap[hgnc] = gmap[hgnc] 
            else:
                #print hgnc
                pass
    return cancer_gmap

def get_list(c_map, file_name):
    with open(file_name, 'w') as f:
        for i in c_map.keys():
            for j in c_map[i]:
                f.write("{},{}\n".format(i, j))

# load data
# mapp = sys.argv[1]
# kidney = sys.argv[2]
# breast = sys.argv[3]

mapp = 'ENSEMBL_91_MAPPING.txt'
kidney = 'kidney.mutated.genes.txt'
breast = 'breast.mutated.genes.txt'

# get one maps for each of the two cancers: {hgnc_name: gene_id}
gmap = get_mapping(mapp)
kmap = map_cancer_genes(kidney, gmap)
bmap = map_cancer_genes(breast, gmap)

get_list(kmap, 'kidney_ensambl_list.txt')
get_list(bmap, 'breast_ensambl_list.txt')
