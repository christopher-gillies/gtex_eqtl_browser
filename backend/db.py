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

if __name__ == "__main__":
    gene_names = gene_names()
    gene_info = gene_info('INF2')

    print(gene_info)