import hail
from hail.experimental import import_gtf
gtf_data = import_gtf('/data/gencode.v26.GRCh38.genes.gtf.gz',force=True)

