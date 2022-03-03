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
    'vars': absolute + 'data/variants',
    'var-desc-cf': absolute + 'data/variants/desc-idrvars/cf',
    'var-desc-cc': absolute + 'data/variants/desc-idrvars/cc',
    'var-desc-len': absolute + 'data/variants/desc-idrvars/length',
    'all-var-desc-cf': absolute + 'data/variants/desc-allvariant/cf',
    'all-var-desc-cc': absolute + 'data/variants/desc-allvariant/cc',
    'all-var-desc-len': absolute + 'data/variants/desc-allvariant/length',
    'dis': absolute + 'data/Disprot',
    'jsn': absolute + 'data/json',
    'ptm': absolute + 'data/ptms',
    'ptm-u': absolute + 'data/ptms/uniprot-ptms',
    'fp': absolute + 'data/llps/phasepro',
    'fs': absolute + 'data/llps/phasep',
    'mlo-d':absolute + 'data/llps/mlo-dis',
    'mlo':absolute + 'data/llps/insight-into-llps',



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
    'vb-cf': absolute + 'plots/variants/inIDR/boxplot/cf',
    'vb-cc': absolute + 'plots/variants/inIDR/boxplot/cc',
    'vb-len': absolute + 'plots/variants/inIDR/boxplot/length',
    'vv-cf': absolute + 'plots/variants/inIDR/violinplot/cf',
    'vv-cc': absolute + 'plots/variants/inIDR/violinplot/cc',
    'vv-len': absolute + 'plots/variants/inIDR/violinplot/length',
    'var-bar': absolute + 'plots/variants/inIDR/barplot',
    'avb-cf': absolute + 'plots/variants/allVars/boxplot/cf',
    'avb-cc': absolute + 'plots/variants/allVars/boxplot/cc',
    'avb-len': absolute + 'plots/variants/allVars/boxplot/length',
    'avv-cf': absolute + 'plots/variants/allVars/violinplot/cf',
    'avv-cc': absolute + 'plots/variants/allVars/violinplot/cc',
    'avv-len': absolute + 'plots/variants/allVars/violinplot/length',
    'avar-bar': absolute + 'plots/variants/allVars/barplot',
    'var-hms': absolute + 'plots/variants/heatmaps',


}
