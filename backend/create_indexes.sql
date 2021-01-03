CREATE INDEX IF NOT EXISTS gene_name_idx 
ON gene_info(gene_name);

/* eGene */

CREATE INDEX IF NOT EXISTS gene_name_eGene_idx
ON eGene(gene_name);

CREATE INDEX IF NOT EXISTS gene_id_eGene_idx
ON eGene(gene_id);

CREATE INDEX IF NOT EXISTS tissue_eGene_idx
ON eGene(tissue);

/* eSNP */

CREATE INDEX IF NOT EXISTS gene_id_eSNP_idx
ON eSNP(gene_id);

CREATE INDEX IF NOT EXISTS gene_id_eSNP_idx
ON eSNP(variant_id);

CREATE INDEX IF NOT EXISTS tissue_eSNP_idx
ON eSNP(tissue);