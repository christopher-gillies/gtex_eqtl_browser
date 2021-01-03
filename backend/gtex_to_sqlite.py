import os
import re
import pandas as pd
import sqlite3

sqlite_db = '/data/eqtl_database.db'
data_files = '/data/GTEx_Analysis_v8_eQTL/'
eqtl_files = os.listdir(data_files)

#print(eqtl_files)

tissues = set()
files = []

class GTExDataFile:

    def __init__(self,file_name):
        tissue, version, file_type, ext1, ext2 = file_name.split('.')
        self.tissue = tissue
        self.version = version
        self.file_type = file_type
        self.ext1 = ext1
        self.ext2 = ext2
        self.file_name = data_files + file_name

        if file_type == 'egenes':
            self.type = 'eGene'
        elif file_type == 'signif_variant_gene_pairs':
            self.type = 'eSNP'
        else:
            self.type = 'ERROR'
    
    def __repr__(self):
        return self.file_name

    def __str__(self):
        return self.__repr__()

for file_name in eqtl_files:
    gtex_data_file = GTExDataFile(file_name)
    files.append(gtex_data_file)
    tissues.add(gtex_data_file.tissue)


#print(sorted(tissues))


gtex_tissue_dict = dict()
for tissue in tissues:
    gtex_tissue_dict[tissue] = []

for gtex_data_file in files:
    gtex_tissue_dict[gtex_data_file.tissue].append(gtex_data_file)


#print(gtex_tissue_dict['Liver'])

# type in [ 'eGene', 'eSNP' ]


tissues_to_use = ['Kidney_Cortex','Liver','Whole_Blood']

"""
Read the tissues of interest and insert into an sqlite3 database
"""

conn = sqlite3.connect(sqlite_db) 

print('Drop Tables')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS eGene;")
cursor.execute("DROP TABLE IF EXISTS eSNP;")

for tissue in tissues_to_use:
    files_per_tissue = gtex_tissue_dict[tissue]
    for gtex_data_file in files_per_tissue:
        print(tissue)
        if gtex_data_file.type == 'eGene':
            print('Reading...')
            print(gtex_data_file.file_name)
            egene_df = pd.read_csv(gtex_data_file.file_name,sep='\t')
            egene_df['Tissue'] = tissue
            print('Writing to db...')
            egene_df.to_sql('eGene', conn, if_exists='append', index=False) 
        else:
            print('Reading...')
            print(gtex_data_file.file_name)
            eSNP_df = pd.read_csv(gtex_data_file.file_name,sep='\t')
            eSNP_df['Tissue'] = tissue
            print('Writing to db...')
            eSNP_df.to_sql('eSNP', conn, if_exists='append', index=False) 


print('Create Indexes')

# eGene

cursor.execute("CREATE INDEX IF NOT EXISTS gene_name_eGene_idx ON eGene(gene_name);")

cursor.execute("CREATE INDEX IF NOT EXISTS gene_id_eGene_idx ON eGene(gene_id);")

cursor.execute("CREATE INDEX IF NOT EXISTS tissue_eGene_idx ON eGene(tissue);")

# eSNP

cursor.execute("CREATE INDEX IF NOT EXISTS gene_id_eSNP_idx ON eSNP(gene_id);")

cursor.execute("CREATE INDEX IF NOT EXISTS gene_id_eSNP_idx ON eSNP(variant_id);")

cursor.execute("CREATE INDEX IF NOT EXISTS tissue_eSNP_idx ON eSNP(tissue);")

conn.close()