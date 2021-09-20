import os

absolute = os.path.abspath(os.getcwd())
absolute = absolute + '/../'
data = {
    'gene4': absolute + 'data/gene4denovo',
    'rseq': absolute + 'data/refseq',
    '': absolute + 'data',
    'brain': absolute + 'data/brain',
    'csv': absolute + 'data/to-csv',
    'dndb': absolute + 'data/denovodb',
    'phens': absolute + 'data/mobibool-phens',
    'phens-fdr': absolute + 'data/mobibool-phens/acc-phens-FDR',
    'xml': absolute + 'data/xml',
    'xml-p': absolute + 'data/xml/parsed',
    'vars' : absolute + 'data/variants',

}
plots = {
    '': absolute + 'plots',
    'bar': absolute + 'plots/g4dn/barplot',
    'box': absolute + 'plots/g4dn/boxplot',
    'box-cf': absolute + 'plots/g4dn/boxplot/cf',
    'box-cc': absolute + 'plots/g4dn/boxplot/cc',
    'box-len': absolute + 'plots/g4dn/boxplot/length',
    'violin': absolute + 'plots/g4dn/violinplot',
    'vio-cf': absolute + 'plots/g4dn/violinplot/cf',
    'vio-cc': absolute + 'plots/g4dn/violinplot/cc',
    'vio-len': absolute + 'plots/g4dn/violinplot/length',
    'vars': absolute + 'plots/variants',
    'var-cf': absolute + 'plots/variants/cf',
    'var-cc': absolute + 'plots/variants/cc',
    'var-len': absolute + 'plots/variants/length',


}
