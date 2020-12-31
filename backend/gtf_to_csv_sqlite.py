import csv
import gzip

import sqlite3 
import pandas as pd

"""
Purpose: Convert GTF file to a csv file for importing into a sqlite databases
"""
#  %run /app/backend/gtf_to_csv_sqlite.py

class GTFRow:
    def __init__(self,rows):
        """
        Example:
        ['chr1', 'HAVANA', 'gene', '11869', '14403', '.', '+', '.', 'gene_id "ENSG00000223972.5"; transcript_id "ENSG00000223972.5"; gene_type "transcribed_unprocessed_pseudogene"; gene_name "DDX11L1"; transcript_type "transcribed_unprocessed_pseudogene"; transcript_name "DDX11L1"; level 2; havana_gene "OTTHUMG00000000961.2";']
        """

        chrom, source, type_of, start, stop, u1, strand, u2, info = rows

        self.chrom = chrom
        self.type = type_of
        self.start = start
        self.stop = stop
        self.strand = strand
        self.info = dict()

        info_elements = info.split(';')
        for info_element in info_elements:
            info_element = info_element.strip()
            if len(info_element) > 0:
                #print(info_element)
                field, value = info_element.split(' ')
                value = value.replace('"','')
                self.info[field] = value
        
        self.gene_id = self.info['gene_id'] if 'gene_id' in self.info else  ""
        self.transcript_id = self.info['transcript_id'] if 'transcript_id' in self.info else  ""
        self.gene_type = self.info['gene_type'] if 'gene_type' in self.info else  ""
        self.gene_name = self.info['gene_name'] if 'gene_name' in self.info else  ""
        self.transcript_type = self.info['transcript_type'] if 'transcript_type' in self.info else  ""
        self.transcript_name = self.info['transcript_name'] if 'transcript_name' in self.info else  ""
        self.level = self.info['level'] if 'level' in self.info else  ""

    @staticmethod
    def header():
        return ','.join(['chrom','type','start','stop','strand','gend_id','gene_name','gene_type','transcript_id','transcript_name','transcript_type','level'])

    def __repr__(self):
        return ','.join( [self.chrom, self.type, self.start, self.stop, self.strand, self.gene_id, self.gene_name, self.gene_type, self.transcript_id, self.transcript_name, self.transcript_type, self.level] )

    def __str__(self):
        return self.__repr__()

gtf_file = '/data/gencode.v26.GRCh38.genes.gtf.gz'
gtf_csv_file = '/data/gencode.v26.GRCh38.genes.csv.gz'
sqlite_db = '/data/eqtl_database.db'

conn = sqlite3.connect(sqlite_db) 

with gzip.open(gtf_csv_file,'wt') as out:
    with gzip.open(gtf_file, 'rt') as csv_file:
        reader = csv.reader(csv_file, delimiter='\t')
        out.write( GTFRow.header() )
        out.write('\n')

        for row in reader:
            #skip the header rows
            if row[0].startswith('#'):
                continue
            row_gtf = GTFRow(row)
            out.write(row_gtf.__repr__())
            out.write('\n')


gtf_rows = pd.read_csv(gtf_csv_file) 

print( gtf_rows.head(10) )

gtf_rows.to_sql('gene_info', conn, if_exists='replace', index=False) 

# create index

create_index = """CREATE INDEX IF NOT EXISTS gene_name_idx 
ON gene_info(gene_name);"""

cursor = conn.cursor()
cursor.execute(create_index)

conn.close()

