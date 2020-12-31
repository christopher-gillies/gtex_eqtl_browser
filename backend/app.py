from flask import Flask,jsonify

import pandas as pd
import db

app = Flask(__name__)


@app.route('/')
def hello():
    return jsonify( "eqtl_browser" )

@app.route('/gene_names')
def gene_names():
    gene_names = db.get_gene_names()
    return jsonify(gene_names)

@app.route('/gene_info/<gene_name>')
def gene_info(gene_name):
    gene_info_res = db.gene_info(gene_name)
    return jsonify(gene_info_res)

if __name__ == '__main__':
    #app.run()
    app.run(host= '0.0.0.0')