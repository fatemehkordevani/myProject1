# created at sep 8th to extract variant id from uniprot txt API, store and insert in expasy API to
# get the mutation position fromn there
import urllib.request
import re
import pandas as pd
import config as cfg

my_proteins_acc_df = pd.read_csv(cfg.data['phens-fdr'] + '/acc-phen-5percentFDR.csv', usecols=['acc'])
my_proteins_acc_lst = set(my_proteins_acc_df['acc'].tolist())  # 1308
my_proteins_acc_lst = list(dict.fromkeys(my_proteins_acc_lst))
my_proteins_acc_lst = my_proteins_acc_lst[:3]
proteins_dict = {}
par_list = []

for acc in my_proteins_acc_lst:
    url = 'https://www.uniprot.org/uniprot/' + acc + '.txt'
    # proteins_dict[acc] = []
    disease_par_lst = []
    file_test = urllib.request.urlopen(url)
    for l in file_test:
        line = l.decode("utf-8")
        if re.search(r'^CC\s+-!-', line):
            if re.search(r'^CC\s+-!- DISEASE:', line):
                # Crerate new paragraph
                disease_par_lst.append(line)
            # Otherwise, break only if all DISEASE line have been terminated
            elif len(disease_par_lst) > 0:
                break
        elif len(disease_par_lst) > 0:
            # print(line)
            disease_par_lst[-1] += line

    for par in disease_par_lst:
        # Extract subsequence
        par = re.sub(r'[\n\r]+', ' ', par)
        print(par)
        par = re.split(r'^CC\s+-!- DISEASE: ', par, 1)
        print(par)
        par = re.split(r'\[MIM:\d{6}\]', par[0], 1)[0]
        print('org: '+par)
        # par = par[0]
        #print(par)
        # Retrieve list
        par_list = proteins_dict.setdefault(acc, [])
        # Store paragraph
        par_list.append(par)


print(proteins_dict)
print(par_list)
