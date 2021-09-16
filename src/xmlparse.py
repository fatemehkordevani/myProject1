# This file is created to parse uniprot xml data file to get mut locations and other useful info (sep 14th)
import xml.etree.ElementTree as ET
import config as cfg
import pandas as pd
import dateutil

NS = {'uniprot': 'http://uniprot.org/uniprot'}
# tree = ET.parse(cfg.data['xml'] + '/uniprot_example.xml')
tree = ET.parse(cfg.data['xml'] + '/uniprot-reflst-20001to40000.xml')
root = tree.getroot()
# sequence_length = int(root.find("uniprot:entry/uniprot:sequence", NS).attrib["length"])
entries = root.findall('uniprot:entry', NS)
# {acc: {var_id: {description: xxxx, evidence:xxxxx, position:x, orig_aa:x, var_aa:x}}}
acc_protinfo = []
for entry in entries:
    acc = (entry.find('uniprot:accession', NS)).text
    for feature in entry.findall('uniprot:feature', NS):
        if feature.attrib['type'] == 'sequence variant':
            for pos in feature.findall('uniprot:location/uniprot:position', NS):
                if 'description' in feature.attrib:
                    print('inside the if')
                    acc_protinfo.append([acc, feature.attrib['id'], feature.attrib['description'],
                                         feature.get('original'),
                                         feature.find('./variation'),
                                         pos.attrib['position']])
                else:
                    acc_protinfo.append([acc, feature.attrib['id'], None,
                                         feature.get('original'), feature.find('./variation'), pos.attrib['position']])

# with open(cfg.data['phens']+'/xml-parsed.txt', 'w') as f:
#     for item in acc_protinfo:
#         f.write("%s\n" % item)

df = pd.DataFrame(acc_protinfo, columns=['acc', 'id', 'description', 'aa', 'variation', 'pos'])
df.to_csv(cfg.data['phens'] + '/uniprot_variants.csv')

#
# print(acc_protinfo_dic)
# acc_pos_d = {}
# acc_lst = list(acc_protinfo_dic.keys())
# for acc in acc_lst:
#     vars_per_each_acc_lst = list(acc_protinfo_dic[acc].keys())
#     muts_pos_per_each_acc_lst = []
#     for id in vars_per_each_acc_lst:
#         mut_position = acc_protinfo_dic[acc][id]['position']
#         muts_pos_per_each_acc_lst.append(mut_position)
#     acc_pos_d[acc] = [list(set(muts_pos_per_each_acc_lst))]
#
# print(acc_pos_d)
# mutpos_df = pd.DataFrame(data=acc_pos_d)
# mutpos_df = mutpos_df.T
#
#
# # TODO: make dict of acc and corresponding diseases, for the ones not having that section, put None.
# #  then do the mut in IDR analysis again
# # in the end do it in terminal not pycharm
