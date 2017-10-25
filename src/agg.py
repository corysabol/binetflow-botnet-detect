import binet_features as bf # our feature extractors for CTU-13
import pandas as pd
import os
import sys # for argv
import datetime as dt

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

def get_files(path):
    # here it's okay if the file is not found
    # we would want the program to except on this
    # case, as without the files there is nothing to do.
    directory = os.fsencode(path)
    return os.listdir(directory)

def agg_time(interval='1S'):
    # iterate the files in the dataset directory
    pickle_dir = os.path.join('..','Datasets','ctu13pickles/')
    path = os.path.join('..','CTU-13-Dataset/')

    for f in get_files(path):
        print(f.decode('utf-8'))
        df = pd.read_csv(os.path.join(path, f.decode('utf-8')))
        # chop off the ms from the start time and reindex the df to use
        # start time as a datetime object index.
        df['StartTime'] = df['StartTime'].apply(lambda x: x[:19])
        df['StartTime'] = pd.to_datetime(df['StartTime'])
        df = df.set_index('StartTime')

        # replace NaN with a negative port number
        df['Dport'] = df['Dport'].fillna('-1')
        df['Dport'] = df['Dport'].apply(lambda x: int(x,0))
        df['Sport'] = df['Sport'].fillna('-1')
        df['Sport'] = df['Sport'].apply(lambda x: int(x,0))

        r = df.resample(interval)
        # apply extractors
        df = r.agg(extractors)
        df.columns = df.columns.droplevel(0)

        # pickle each df for later
        df.to_pickle(os.path.join(pickle_dir, f.decode('utf-8')))

agg_time('1S')
