from flask import Flask,jsonify

import pandas as pd
import db

app = Flask(__name__)


@app.route('/')
def hello():
    return jsonify( "eqtl_browser" )

@app.route('/gene_names')
def gene_names():
    gene_names = db.gene_names()
    return jsonify(gene_names)

@app.route('/tissues')
def tissues():
    tissues_res = db.tissues()
    return jsonify(tissues_res)

@app.route('/gene_info/<gene_name>')
def gene_info(gene_name):
    gene_info_res = db.gene_info(gene_name)
    return jsonify(gene_info_res)

@app.route('/eGenes_by_tissue/<tissue>')
def eGenes_by_tissue(tissue):
    eGenes_by_tissue_res = db.eGenes_by_tissue(tissue)
    return jsonify(eGenes_by_tissue_res)

@app.route('/eSNPs_by_gene_name_tissue/<gene_name>/<tissue>')
def eSNPs_by_gene_name_tissue(gene_name,tissue):
    eSNPS_res = db.eSNPs_by_gene_name_tissue(gene_name,tissue)
    return jsonify(eSNPS_res)
    
if __name__ == '__main__':
    #app.run()
    app.run(host= '0.0.0.0')