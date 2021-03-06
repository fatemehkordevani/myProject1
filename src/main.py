# Start date = April 14th
import itertools

import matplotlib.pyplot
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import categorizer as pm
import testmutation2 as mt

mobidb_features_lst = []
mobidb_predictors_cont_fra_dict = {}
cont_fra_temp_lst = []

ndd_cont_fra_temp_lst = []
ndd_predictors_cont_fra_dict = {}


def drawplot(plot_input_lst, yscale, bins, is_dense, x_label, y_label, png_file_name):
    plt.hist(plot_input_lst, bins=bins,
             density=is_dense)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    file_format = '.png'
    plt.yscale(yscale)
    plt.savefig(png_file_name + file_format)
    plt.show()
    return


def draw_barplot(figsize_a, figsize_b, xlabel, ylabel, data, xticklabel, yscale, save_rout):  # input is DF, not list
    plt.figure(figsize=(int(figsize_a), int(figsize_b)))  # bigger figsize to have xticklabels shown
    sns.set_style("ticks")
    g = sns.barplot(x=xlabel, y=ylabel, data=data)
    # sns.despine(trim=True, offset=2)
    g.set_xticklabels(xticklabel, rotation=45, va="center", position=(0, -0.02))
    sns.color_palette("pastel")
    plt.yscale(yscale)
    plt.tight_layout()
    plt.savefig(save_rout)
    plt.show()
    return


def compare_plot(first_lst, second_lst, yscale, bins, is_dense, first_label, second_label, x_label, y_label,
                 png_file_name):
    plt.hist([first_lst, second_lst], bins=bins, density=is_dense, label=[first_label, second_label])
    plt.legend(loc='upper right')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    file_format = '.png'
    plt.yscale(yscale)
    plt.savefig(png_file_name + '_compare' + file_format)
    plt.show()
    return


def matrix_maker_nan(input_df, max_value, thrd_dim_cells, math_oper, get_values_in_range):
    # gets input_df and gives 2d, 3d arrays, filters based on max_value, the 3rd dim is based on the range of values,
    # e.g: 0-10 (thrd_dim_cells) math_oper and get_values_in_range are dependant, they should be calculated in order
    # to give distribute values 0-max based on number of 3d_cells example, for length, max_v = 1000 and we have 11
    # cell ranges [0:11], so we should divide all by 100 => 1000/100 = 10)
    matrix_2d = (input_df.to_numpy() <= max_value) * input_df.to_numpy()
    matrix_3d = np.full((matrix_2d.shape[0], matrix_2d.shape[1], thrd_dim_cells), np.nan)
    for i in range(matrix_2d.shape[0]):
        for j in range(matrix_2d.shape[1]):
            if matrix_2d[i, j] != 0:
                if math_oper == '*':
                    k = int(round(matrix_2d[i, j] * get_values_in_range))
                    matrix_3d[i, j, k] = 1
                elif math_oper == '/':
                    k = int(round(matrix_2d[i, j] / get_values_in_range))
                    matrix_3d[i, j, k] = 1

    #
    # Replace NaN with zeros for rows containing at least one value
    # for i in range(matrix_3d.shape[0]):
    #     for j in range(matrix_3d.shape[1]):
    #         if 1.0 in matrix_3d[i][j]:
    #             matrix_3d[i][j][np.isnan(matrix_3d[i][j])] = 0

    # sum of Pr.s with same content_fraction or length for each feature
    matrix_3d_sum = np.nansum(matrix_3d, axis=0, dtype=int)
    matrix_3d_sum_normalized = matrix_3d_sum / matrix_3d_sum.max(axis=1)[:, None]
    return matrix_2d, matrix_3d, matrix_3d_sum, matrix_3d_sum_normalized


def matrix_maker_zeros(input_df, num_3rd_dim, max_range):
    matrix_2d = (input_df.to_numpy() <= 1.) * input_df.to_numpy()
    matrix_3d = np.zeros((matrix_2d.shape[0], matrix_2d.shape[1], num_3rd_dim + 1))
    for i in range(matrix_2d.shape[0]):
        for j in range(matrix_2d.shape[1]):
            # if matrix_2d[i, j] != 0:
            k = int(round(matrix_2d[i, j] * num_3rd_dim))
            matrix_3d[i, j, k] = 1
    matrix_3d_sum = np.sum(matrix_3d, axis=0)
    # matrix_3d_sum_normalized = matrix_3d_sum / matrix_3d_sum.max(axis=1)[:, None]
    return matrix_2d, matrix_3d, matrix_3d_sum  # , matrix_3d_sum_normalized


def sum_df_generator(input_sum_matrix, columns):
    sum_df = pd.DataFrame(input_sum_matrix,
                          columns=columns,
                          index=mobidb_features_lst[1:])
    return sum_df


def draw_heatmaps(data, titles, saving_rout):  # www.stackabuse.com/ultimate-guide-to-heatmaps-in-seaborn-with-python/
    sns.set()
    fig, axes = plt.subplots(len(data), 1, figsize=(12 * len(data), 12))
    for i, (ax, d, t) in enumerate(zip(axes.reshape(-1), data, titles)):
        sb = sns.heatmap(d,
                         cmap="viridis",  # sequential colormap
                         annot=False,
                         annot_kws={'fontsize': 6},
                         fmt='',
                         square=True,
                         # vmax=1,
                         # vmin=0,
                         linewidth=0.01,
                         linecolor="#222",
                         ax=ax,
                         vmin=-1.0, vmax=1.0
                         )
        ax.set_title(t)
        # ax.set_ylabel(ylabel)
        if i < (len(data) - 1):
            sb.set(xticklabels=[])
            sb.set(xlabel=None)
    plt.tight_layout()
    plt.savefig(saving_rout, dpi=120)
    plt.show()
    return


def df_lst_maker_for_barplot(input_matrix):
    cols_sum_df = pd.DataFrame([input_matrix], columns=mobidb_features_lst[1:], index=['Protein count'])
    cols_sum_df = cols_sum_df.T.reset_index()
    cols_sum_df.columns = ['Features', 'Protein count']
    cols_sum_lst = cols_sum_df['Protein count']
    cols_sum_lst = [int(x) for x in cols_sum_lst]

    return cols_sum_df, cols_sum_lst


def expand_regions(region_ranges_lst):
    transformed_regions = []
    for reg in region_ranges_lst:
        start = int(reg.split('..')[0])
        end = int(reg.split('..')[1])
        while start <= end:
            transformed_regions.append(start)
            start += 1
    return set(transformed_regions)


if __name__ == '__main__':


    # # martina stuff:
    # # first py file
    # pm.generate_mutation_file()
    # # second py file
    # mt.generateggg()
    # pm.generate_mutation_file2()

    # -------


    # This is the main!
    ## Gene4denovo(exonic mutations)
    exonic_g4dn_df = pd.read_csv('../data/gene4denovo/exonic-df.csv')  # (70879, 156)
    ## mut position df import
    # rseq_mutinfo_df = pd.read_csv('data/gene4denovo/subdf-mut-beforeACC.csv')  # (201372, 11)
    # # merge with gene4dn exonic, now original exonic g4dn file + mutInfo e.g position
    # g4dn_exonic_mutinfo_df = pd.merge(rseq_mutinfo_df, exonic_g4dn_df, on='idx')  # (201372, 166)
    # g4dn_exonic_mutinfo_df.to_csv(r'data/gene4denovo/exonic-mutinfo.csv')
    # ## g4dn mutInfo + uniprot ACCs file
    # g4dn_exonic_mutinfo_df = pd.read_csv('data/gene4denovo/exonic-mutinfo.csv')  # (201372, 166)
    # refseq_acc_df1 = pd.read_csv('data/refseq/refseq-acc.tab', sep='\t')  # from Uniprot
    # # * merge g4dn exonic mutInfo with Uniprot ACC
    mut_acc_mrg_df = pd.read_csv('../data/mut-acc-mrg-df.csv')  # (236699, 169)

    ## mobidb
    mobidb_original_df = pd.read_csv('../data/mobidb_result.tsv', sep='\t')  # (1212280,6)
    final_mut_check_df = pd.read_csv('../data/mutations-position-mobidb-all.csv')  # (4258689, 10)

    # filtered with mutations inside IDRs
    filtered_mut_pos_df = final_mut_check_df[final_mut_check_df['is_in_startend'] == 1]  # (1003250, 10)
    filtered_mut_pos_df.to_csv(r'data/gene4denovo/mobidb-mut-pos-true.csv')
    mobidb_mutpos_true_df = pd.read_csv('../data/gene4denovo/mobidb-mut-pos-true.csv')

    ## mobidb pivot table, content count
    mobidb_muttrue_cc_pivot_df = mobidb_mutpos_true_df.pivot_table(
            index=['acc'], columns=['feature'], values='content_count').fillna(0)
    ## mobidb pivot table, content fraction
    # mobidbp_muttrue_cf_df = mobidb_mutpos_true_df.pivot_table(
    #     index=['acc'], columns=['feature'], values='content_fraction').fillna(0)
    #TODO: from here
    ## merged mobidb_muttrue(normal df) with (g4dn+acc)
    # # merged_filtered_mobidb_d4dn_df = pd.merge(filtered_mut_pos_df, mut_acc_mrg_df, on='index')
    # # merged_filtered_mobidb_d4dn_df.to_csv(r'data/gene4denovo/final-merged-mobi-g4dn-true.csv')

    ## merged mobidb_muttrue(pivot df) with (g4dn+acc)
    # merged_mobidbp_g4dn_df = pd.merge(mobidbp_muttrue_cf_df, mut_acc_mrg_df, on='acc')
    # merged_mobidbp_g4dn_df.to_csv(r'data/gene4denovo/final-merged-with-mobidb-pivot.csv')
    merged_mobidbp_g4dn_df = pd.read_csv('../data/gene4denovo/final-merged-with-mobidb-pivot.csv',
                                         low_memory=False)  # (180315, 245)
    phenotypes_lst = ['ASD', 'EE', 'ID', 'CMS', 'SCZ', 'NDDs']
    # (41081, 245)
    phens_mobip_g4dn_muttrue_df = merged_mobidbp_g4dn_df[merged_mobidbp_g4dn_df.Phenotype.isin(phenotypes_lst)]
    phens_mobip_g4dn_limited_df = phens_mobip_g4dn_muttrue_df.drop(
        columns=['Unnamed: 0', 'index', 'Unnamed: 0.1', 'mutNA', 'AAChange_refGene_x', 'Rare_or_Common',
                 'Func.refGene', 'Gene.refGene', 'GeneDetail.refGene', 'AAChange_refGene_y', 'GeneFullName.refGene',
                 'GeneFullName.ensGene', 'GeneFunction.ensGene', 'GeneExpressionTissue.ensGene',
                 'GeneDisease.ensGene', 'OMIM.ensGene', 'MGI.ensGene', 'RVIS.ensGene', 'LoFtool.ensGene', 'GDI.ensGene',
                 'Episcore.ensGene', 'Aggarwala.ensGene', 'pLi_EXAC.ensGene', 'HIPred.ensGene'])  # (41081, 221)
    phen_asd = ['ASD']
    ASD_mobip_g4dn_limited_df = phens_mobip_g4dn_limited_df[
        phens_mobip_g4dn_limited_df.Phenotype.isin(phen_asd)]  # (28486, 221)
    print(ASD_mobip_g4dn_limited_df['ExonicFunc.refGene'].value_counts(dropna=False))

    # filtered with mutations out of IDRs
    # mobidb_mut_check_df = pd.read_csv('data/mutations-position-mobidb-all.csv')
    # filtered_mut_pos_false_df = mobidb_mut_check_df[mobidb_mut_check_df['is_in_startend'] == 0]
    # filtered_mut_pos_false_df.to_csv(r'data/gene4denovo/mobidb-mut-pos-false.csv')  # (3255439, 10)
    filt_mut_pos_false_df = pd.read_csv('../data/gene4denovo/mobidb-mut-pos-false.csv')
    mobidb_mutfalse_cf_pivot_df = filt_mut_pos_false_df.pivot_table(index=['acc'], columns=['feature'],
                                                                    values='content_fraction').fillna(0)
    mobidb_mutfalse_cc_pivot_df = filt_mut_pos_false_df.pivot_table(index=['acc'], columns=['feature'],
                                                                    values='content_count').fillna(0)
    # TODO: also the content count for muttrue df

    ## merged mobidb_muttrue(pivot df) with (g4dn+acc)
    # mobidbp_g4dn_cf_mutfalse_df = pd.merge(mobidb_mutfalse_cf_pivot_df, mut_acc_mrg_df, on='acc')
    # mobidbp_g4dn_cf_mutfalse_df.to_csv(r'data/gene4denovo/merged-with-mobidb-pivot-mutfalse.csv')
    merged_mobidbp_g4dn_mutfalse_df = pd.read_csv('../data/gene4denovo/merged-with-mobidb-pivot-mutfalse.csv',
                                                  low_memory=False)
    phenotypes_lst = ['ASD', 'EE', 'ID', 'CMS', 'SCZ', 'NDDs']
    phens_mobip_g4dn_mutfalse_df = merged_mobidbp_g4dn_mutfalse_df[
        merged_mobidbp_g4dn_mutfalse_df.Phenotype.isin(phenotypes_lst)]
    phens_mobip_g4dn_mutfalse_df = phens_mobip_g4dn_mutfalse_df.drop(
        columns=['Unnamed: 0', 'index', 'Unnamed: 0.1', 'mutNA', 'AAChange_refGene_x', 'Rare_or_Common',
                 'Func.refGene', 'Gene.refGene', 'GeneDetail.refGene', 'AAChange_refGene_y', 'GeneFullName.refGene',
                 'GeneFullName.ensGene', 'GeneFunction.ensGene', 'GeneExpressionTissue.ensGene',
                 'GeneDisease.ensGene', 'OMIM.ensGene', 'MGI.ensGene', 'RVIS.ensGene', 'LoFtool.ensGene', 'GDI.ensGene',
                 'Episcore.ensGene', 'Aggarwala.ensGene', 'pLi_EXAC.ensGene', 'HIPred.ensGene'])  # (41081, 221)

    sys.exit()

    ### Files import and modify
    ## for content fraction
    mobidb_original_df = pd.read_csv('../data/mobidb_result.tsv', sep='\t')
    mobidb_pivot_contf_df = mobidb_original_df.pivot_table(
        index=['acc'], columns=['feature'], values='content_fraction').fillna(0)
    mobidb_pivot_contf_df = mobidb_pivot_contf_df.reset_index()  # added idx nums manually,ACCs recognized separate
    # column
    mobidb_pivot_contf_df.to_csv(r'data/mobidb_pivot_contf_df.csv', index=True)
    mobidb_features_lst = mobidb_pivot_contf_df.columns.str.split(',').tolist()  # this also contains the 'acc' column
    mobidb_features_lst = list(itertools.chain(*mobidb_features_lst))  # flat list

    ndd_acc_df = pd.read_csv('../data/allUniqueEntry.tab', sep='\t')
    ndd_acc_lst = ndd_acc_df['Entry'].to_list()
    ndd_contf_df = mobidb_pivot_contf_df[mobidb_pivot_contf_df['acc'].isin(ndd_acc_lst)]
    ndd_contf_df.to_csv(r'data/ndd-contf-dataframe.csv')
    # get proteins of phase separation feature
    ndd_llps_subdf = ndd_contf_df.loc[ndd_contf_df['curated-phase_separation-merge'] != 0.0, ('acc', 'curated'
                                                                                                     '-phase_separation-merge')]
    ndd_llps_subdf.to_csv(r'data/ndd-llps-merge-Pr-list.csv')
    ## for Length
    mobidb_length_df = mobidb_original_df[['acc', 'length']].drop_duplicates(subset=['acc'])
    mobidb_pivot_length_df = mobidb_original_df.pivot_table(
        index=['acc'], columns=['feature'], values='length').fillna(0)
    mobidb_pivot_length_df = mobidb_pivot_length_df.reset_index()  # reset idx to get acc as dif col to search in it
    mobidb_pivot_length_df.to_csv(r'data/mobidb-pivot-length-df.csv')
    ndd_length_df = mobidb_pivot_length_df[mobidb_pivot_length_df['acc'].isin(ndd_acc_lst)]  # len(df) = 1089
    ndd_length_df.to_csv(r'data/ndd-length-df.csv')

    ## Matrix
    # content fraction with nan
    _, mobi_contf_mat, mobi_contf_sum_mat, mobi_contf_sum_norm_mat = matrix_maker_nan(
        input_df=mobidb_pivot_contf_df.iloc[:, 1:], max_value=1., thrd_dim_cells=11, math_oper='*',
        get_values_in_range=10)
    _, ndd_contf_mat, ndd_contf_sum_mat, ndd_contf_sum_norm_mat = matrix_maker_nan(
        input_df=ndd_contf_df.iloc[:, 1:], max_value=1., thrd_dim_cells=11, math_oper='*', get_values_in_range=10)

    # Length (Use vstack or hstack ?)
    mobi_len_2d_mat, mobi_len_3d_mat, mobi_len_sum_mat, mobi_len_sum_norm_mat = matrix_maker_nan(
        input_df=mobidb_pivot_length_df.iloc[:, 1:], max_value=1000, thrd_dim_cells=11, math_oper='/',
        get_values_in_range=100)
    ndd_len_2d_mat, ndd_len_3d_mat, ndd_len_sum_mat, ndd_len_sum_norm_mat = matrix_maker_nan(
        input_df=ndd_length_df.iloc[:, 1:], max_value=1000, thrd_dim_cells=11, math_oper='/', get_values_in_range=100)
    # ax.hist(dataset_len, bins=np.arange(0, 1000, 10))

    ## sum dataframes
    mobi_contf_sum_norm_df = sum_df_generator(mobi_contf_sum_norm_mat,
                                              ['0', ' ', '20', ' ', '40', ' ', '60', ' ', '80', ' ', '100'])
    ndd_cont_fract_sum_norm_df = sum_df_generator(ndd_contf_sum_norm_mat,
                                                  ['0', ' ', '20', ' ', '40', ' ', '60', ' ', '80', ' ', '100'])
    mobi_len_sum_norm_df = sum_df_generator(mobi_len_sum_norm_mat,
                                            [' ', '100', ' ', '300', ' ', '500', ' ', '700', ' ', '900', ''])
    ndd_len_sum_norm_df = sum_df_generator(ndd_len_sum_norm_mat,
                                           [' ', '100', ' ', '300', ' ', '500', ' ', '700', ' ', '900', ''])

    ## Difference of the sum arrays(with nan)
    difference_contf_sum_norm_mat = mobi_contf_sum_norm_mat - ndd_contf_sum_norm_mat
    difference_len_sum_norm_mat = mobi_len_sum_norm_mat - ndd_len_sum_norm_mat
    difference_contf_sum_norm_df = sum_df_generator(difference_contf_sum_norm_mat,
                                                    ['0', ' ', '20', ' ', '40', ' ', '60', ' ', '80', ' ', '100'])
    difference_len_sum_norm_df = sum_df_generator(difference_len_sum_norm_mat,
                                                  [' ', '100', ' ', '300', ' ', '500', ' ', '700', ' ', '900', ''])

    ## heatmaps
    draw_heatmaps([mobi_contf_sum_norm_df.T, ndd_cont_fract_sum_norm_df.T, difference_contf_sum_norm_df.T],
                  ['Homo sapiens', 'NDDs', 'Difference (Homo sapiens - NDDs)'],
                  saving_rout='plots/heatmaps/Heatmaps0.png')
    draw_heatmaps([mobi_len_sum_norm_df.T, ndd_len_sum_norm_df.T, difference_len_sum_norm_df.T],
                  ['Homo sapiens', 'NDDs', 'Difference (Homo sapiens - NDDs)'],
                  saving_rout='plots/heatmaps/Heatmaps-Length.png')

    ## columns sum sum_matrix to get protein numbers (for bar plot based on distribution of heatmap)
    # content fraction
    mobi_contf_cols_sum_df, mobi_contf_cols_sum_lst = df_lst_maker_for_barplot(mobi_contf_sum_mat.T.sum(axis=0))
    ndd_contf_cols_sum_df, ndd_contf_cols_sum_lst = df_lst_maker_for_barplot(ndd_contf_sum_mat.T.sum(axis=0))
    mobi_contf_cols_sum_df.to_csv(r'data/mobidb-contf-distribution.csv')
    ndd_contf_cols_sum_df.to_csv(r'data/ndd-contf-distribution.csv')
    # length
    mobi_len_cols_sum_df, mobi_len_cols_sum_lst = df_lst_maker_for_barplot(mobi_len_sum_mat.T.sum(axis=0))
    ndd_len_cols_sum_df, ndd_len_cols_sum_lst = df_lst_maker_for_barplot(ndd_len_sum_mat.T.sum(axis=0))
    mobi_len_cols_sum_df.to_csv(r'data/mobidb-len-distribution.csv')
    ndd_len_cols_sum_df.to_csv(r'data/ndd-len-distibution.csv')

    ## Hmap distribution barplots (Protein count)
    # content fraction
    draw_barplot(figsize_a='18', figsize_b='9', xlabel='Features', ylabel='Protein count', data=mobi_contf_cols_sum_df,
                 xticklabel=mobi_contf_cols_sum_lst, yscale='log',
                 save_rout='plots/log/hist-hmaps-distribution/mobidb-contf-NEW.png')
    draw_barplot(figsize_a='18', figsize_b='9', xlabel='Features', ylabel='Protein count', data=ndd_contf_cols_sum_df,
                 xticklabel=ndd_contf_cols_sum_lst, yscale='log',
                 save_rout='plots/log/hist-hmaps-distribution/ndd-contf-NEW.png')
    # Length
    draw_barplot(figsize_a='18', figsize_b='9', xlabel='Features', ylabel='Protein count', data=mobi_len_cols_sum_df,
                 xticklabel=mobi_len_cols_sum_lst, yscale='log',
                 save_rout='plots/log/hist-hmaps-distribution/mobi-len-NEW.png')
    draw_barplot(figsize_a='18', figsize_b='9', xlabel='Features', ylabel='Protein count', data=ndd_len_cols_sum_df,
                 xticklabel=ndd_len_cols_sum_lst, yscale='log',
                 save_rout='plots/log/hist-hmaps-distribution/ndd-len-NEW.png')

    ## Dictionary Homo sapiens
    for each_feature in mobidb_features_lst:
        cont_fra_temp_lst = mobidb_pivot_contf_df[each_feature].tolist()
        mobidb_predictors_cont_fra_dict[each_feature] = cont_fra_temp_lst

    ## Plot for homosapiens
    for each_feature in mobidb_features_lst[
                        1:]:
        drawplot(mobidb_predictors_cont_fra_dict[each_feature], 'log', 30, True, each_feature + '_homosapiens',
                 "Protein Count(relative)",
                 'plots/log/hist-all-homo sapiens/' + each_feature)

    ## Dictionary Disease
    for each_feature in mobidb_features_lst:
        ndd_cont_fra_temp_lst = ndd_contf_df[each_feature].tolist()
        ndd_predictors_cont_fra_dict[each_feature] = ndd_cont_fra_temp_lst

    ## plot for ndds
    for each_feature in mobidb_features_lst[1:]:
        drawplot(ndd_predictors_cont_fra_dict[each_feature], 'log', 30, False, each_feature + '_NDD', 'Protein count',
                 'plots/log/hist-all-NDD/SCZ/' + each_feature + '_SCZ')

    # comparative histogram (homosapiens Vs. ndd)
    for each_feature in mobidb_features_lst[1:]:
        compare_plot(first_lst=mobidb_predictors_cont_fra_dict[each_feature],
                     second_lst=ndd_predictors_cont_fra_dict[each_feature], yscale='log', bins=30, is_dense=False,
                     x_label=each_feature + '_comparison', y_label='proteins count',
                     first_label='Homo sapiens Pr.s', second_label='NDD Pr.s',
                     png_file_name='plots/log/hist-comparison' '-homoS-NDD/' + each_feature)
