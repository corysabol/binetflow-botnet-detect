import pandas as pd
import numpy as np
import os
import sys
import datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import binet_features as bf

from functools import reduce
import ipaddress

heatmaps     = (True if 'heatmaps' in sys.argv else False)
scatter_mats = (True if 'scatter_mats' in sys.argv else False)

dataset_path = os.path.join('..','CTU-13-Dataset/')
directory = os.fsencode(dataset_path)

files = os.listdir(directory)

# The datastructure to hold our feature extraction functions, which will
# get applied to each aggregation of the datasets.
extractors = {
    'Label'   : [bf.label_atk_v_norm,
                 bf.n_attack,
                 bf.background_flow_count,
                 bf.normal_flow_count,
                 bf.n_conn,
                ],
    'Dport'   : [bf.n_dports_gt1024,
                 bf.n_dports_lt1024
                ],
    'Sport'   : [bf.n_sports_gt1024,
                 bf.n_sports_lt1024,
                ],
    'Dur'     : [bf.avg_duration,
                ],
    'SrcAddr' : [bf.n_s_a_p_address,
                 bf.n_s_b_p_address,
                 bf.n_s_c_p_address,
                 bf.n_s_na_p_address,
                 bf.n_s_ipv6,
                ],
    'DstAddr' : [bf.n_d_a_p_address,
                 bf.n_d_b_p_address,
                 bf.n_d_c_p_address,
                 bf.n_d_na_p_address,
                 bf.n_d_ipv6,
                ],
    'Proto'   : [bf.n_tcp,
                 bf.n_icmp,
                 bf.n_udp,
                ],
}

if heatmaps or scatter_mats:
    print('Reading dataset...')
    i = 0
    for f in files:
        df = pd.read_csv(os.path.join(directory,f).decode('utf8'), low_memory=False)

        df['StartTime'] = df['StartTime'].apply(lambda x: x[:19])
        df['StartTime'] = pd.to_datetime(df['StartTime'])
        df = df.set_index('StartTime')

        # replace NaN with a negative port number
        df['Dport'] = df['Dport'].fillna('-1')
        df['Dport'] = df['Dport'].apply(lambda x: int(x,0))
        df['Sport'] = df['Sport'].fillna('-1')
        df['Sport'] = df['Sport'].apply(lambda x: int(x,0))

        r = df.resample('1S')
        print('applying extractors to file {}/13\r'.format(i+1))
        df = r.agg(extractors)
        df.columns = df.columns.droplevel(0) # get rid of the heirarchical columns

        if heatmaps:
            print('Generating heatmaps...')
            corr = df.corr()
            fig, ax = plt.subplots(figsize=(15,10))
            p = sns.heatmap(corr,
                    cmap = sns.diverging_palette(220, 10, as_cmap=True),
                    xticklabels=corr.columns.values,
                    yticklabels=corr.columns.values,
                    ax=ax,
                    label='CTU-13-Binet {} Heatmap'.format(i))
            plt.savefig(os.path.join('..','plots','hm{}'.format(i+1)))
        if scatter_mats:
            print('Generating scatter matricies')
            # generate scatter matrices
            sns.set(style='ticks')
            v = df.columns.tolist()[1:]
            v.remove('n_d_ipv6')
            v.remove('n_s_ipv6')
            print(v)
            sns.pairplot(df, vars=v, hue='label')
            plt.savefig(os.path.join('..','plots','pp{}'.format(i+1)))
            break
        i += 1
else:
    print('Specify heatmaps and or scatter_mats')

