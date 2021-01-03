import pandas as pd;
import sqlite3
# %run /app/backend/db.py

def get_conn():
    sqlite_db = '/data/eqtl_database.db'
    conn = sqlite3.connect(sqlite_db) 
    return conn

def gene_names():
    conn = get_conn()
    genes = pd.read_sql('select distinct gene_name from gene_info ORDER BY gene_name', conn)
    conn.close()
    return  list( genes.gene_name.values )

def gene_info(gene_name):
    """get_gene_info(gene_name)
    gene_name = gene symbol (string)
    This method will use pandas to query the database and get the corresponding gene_information from the database
    It will return the data as a dictionary of records
    Ex:

    [
    {
        'chrom': 'chr14',
        'type': 'exon',
        'start': 104718795,
        'stop': 104722535,
        'strand': '+',
        'gend_id': 'ENSG00000203485.12',
        'gene_name': 'INF2',
        'gene_type': 'protein_coding',
        'transcript_id': 'ENSG00000203485.12',
        'transcript_name': 'INF2',
        'transcript_type': 'protein_coding',
        'level': 1
    }
    ]
    """
    conn = get_conn()
    gene_info = pd.read_sql('select * from gene_info where gene_name = ?', con=conn, params=[gene_name])
    conn.close()
    return gene_info.to_dict(orient='record')

def tissues():
    conn = get_conn()
    tissues_res = pd.read_sql('select distinct tissue from eGene', con=conn)
    conn.close()
    return list(tissues_res.Tissue.values)

def eGenes_by_tissue(tissue):
    conn = get_conn()
    egenes = pd.read_sql('select * from eGene where tissue = ?', con=conn, params=[tissue])
    conn.close()
    return egenes.to_dict(orient='record')

def eSNPs_by_gene_name_tissue(gene_name,tissue):
    conn = get_conn()
    gene_info_for_gene_name = gene_info(gene_name)
    gene_id = gene_info_for_gene_name[0]['gene_id']
    esnps_for_gene_and_tissue = pd.read_sql('select * from eSNP where gene_id = ? and tissue = ?', con=conn, params=[gene_id, tissue])
    conn.close()
    return esnps_for_gene_and_tissue.to_dict(orient='record')

if __name__ == "__main__":
    gene_names = gene_names()
    erap2_info = gene_info('ERAP2')
    egenes_liver = eGenes_by_tissue('Liver')
    
    #print(egenes_liver[0])

    eSNP_res = eSNPs_by_gene_name_tissue('ERAP2','Liver')
    print(eSNP_res)

    print(erap2_info[0]['gene_id'])

    tissues_res = tissues()

    print(tissues_res)