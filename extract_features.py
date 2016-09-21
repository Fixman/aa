# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import numpy
import pandas
import sys

# Extrae cierto conjunto de features aplicado individualmente a ciertas columnas.
class ExtractedFeature(object):
    """
    name -- Nombre del feature. La columna final queda como col_name.
    trans -- Función que se le aplica a ciertas columnas para conseguir el feature.
    filt -- Nombre de columna, lista de columnas, o función (columna -> booleano)
        que decide a qué columnas se le aplica.
    filna -- Con qué rellenar NaNs.
    """
    def __init__(self, name, trans, filt = lambda x: True, fillna = numpy.nan):
        self.name = name
        self.trans = trans
        self.fillna = fillna

        if type(filt) == str:
            self.filt = lambda x: x.name == filt
        elif type(filt) == list:
            self.filt = lambda x: x.name.name in filt
        else:
            self.filt = filt
    
    # Usa el extractor para extraer datos de un DataFrame.
    def extractFrom(self, table):
        cols = table.columns.difference(table._get_numeric_data().columns)
        cols = pandas.Index(x for x in cols if table[x].notnull().any() and self.filt(table[x].dropna()))
        
        return (
            table[cols].apply(lambda x: self.trans(x.dropna()))
            .rename(columns = lambda x: x + '_' + self.name)
            .fillna(self.fillna)
        )

def avg(x):
    return sum(x) / len(x)

# Extrae muchos datos de una tabla.
def extractAll(table):
    sep = ','
    features = [
        ExtractedFeature('length', lambda x: x.str.len()),
        ExtractedFeature('fields', lambda x: x.str.count(sep) + 1, lambda x: x.str.contains(sep).any()),
        ExtractedFeature('avgFieldLength', lambda x: x.str.split(sep).apply(lambda x: avg(map(len, x))), lambda x: x.str.contains(sep).any()),
        ExtractedFeature('words', lambda x: x.str.strip().str.count(' ') + 1, lambda x: x.str.strip().str.contains(' ').any()),
        ExtractedFeature('avgWordLength', lambda x: x.str.strip().str.split(' ').apply(lambda x: avg(map(len, x))), lambda x: x.str.strip().str.contains(' ').any()),
        ExtractedFeature('exists', lambda x: x.notnull(), fillna = False),
    ]

    return pandas.concat(map(lambda x: x.extractFrom(table), features), axis = 1)

def main():
    train = pandas.read_csv(
        sys.stdin,
        index_col = 'num',
        encoding = 'utf-8',
        chunksize = 10000,
        dtype = object
    )

    first = True
    for e, chunk in enumerate(train):
        try:
            # Ugly hack: if b : Bool, b * 1 : Int
            features = extractAll(chunk.drop('spam', axis = 1)) * 1
            features['spam'] = chunk['spam']
            features.to_csv(sys.stdout, index = True, header = first)
            first = False
        except Exception as t:
            print('Exception "{}" on chunk {}'.format(t, e), file = sys.stderr) 

if __name__ == '__main__':
    main()
