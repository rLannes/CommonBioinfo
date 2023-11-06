attr.get(biot_field, "NA")import matplotlib.pyplot as plt
import pickle
import argparse

def get_attr(string):
    dico = {}
    spt = string.split(";")
    
    for x in spt:
        if x:
            dico[x.split()[0]] =  x.split()[1].replace('"', "")
    return dico


def gtf_as_dict(gtf_file, biot_field, trans_s_field, gene_s_field, out=None):

    dico = {}
    with open(gtf_file) as f_in:

        for line in f_in:
            if line.startswith("#"):
                continue
            spt = line.strip().split("\t")

            chr_ = spt[0]
            start = int(spt[3])
            end = int(spt[4])
            strand =  spt[6]
            attr = get_attr(spt[-1])
            gene_id = attr["gene_id"]
            gene_symbol = attr[gene_s_field]
            biotype =  attr.get(biot_field, "NA")
            type_ = spt[2]

            if type_ == "gene":

                dico[gene_id] = {
                    "chr": chr_,
                    "start": start, 
                    "end" : end,
                    "strand" : strand,
                    "symbol" :  gene_symbol,
                    "biotype" : biotype,
                "transcript": {}}

            else:

                transcript_id  = attr["transcript_id"]
                transcript_symbol = attr[trans_s_field]

                if transcript_id not in dico[gene_id]["transcript"]:
                    dico[gene_id]["transcript"][transcript_id] = {
                    "transcript_symbol" : transcript_symbol,
                    "transcript_id" : transcript_id
                    }

                if type_ not in dico[gene_id]["transcript"][transcript_id]: 
                    dico[gene_id]["transcript"][transcript_id][type_] = []

                dico[gene_id]["transcript"][transcript_id][type_].append({
                    "chr": chr_,
                    "start": start, 
                    "end" : end,
                    "strand" : strand,
                })
            
            if out:
                with open(out, "wb") as f_o:
                    pickle.dump(dico, f_o)
    return dico

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--gtf', "-gtf")   
    parser.add_argument('--out', '-out')
    parser.add_argument('-biotype', default="gene_biotype")
    parser.add_argument('-trans_symbol', default="transcript_name")
    parser.add_argument('-gene_symbol', default="gene_name")
    # parser.add_argument('-biotype', default="gene_biotype")
    # parser.add_argument('-biotype', default="gene_biotype")
    args = parser.parse_args()
    out = None
    if args.out:
        out = args.out
    
    gtf_as_dict(gtf=args.gtf, out=out, biot_field=args.biotype, trans_s_field=args.trans_symbol, gene_s_field=args.gene_symbol)
  
