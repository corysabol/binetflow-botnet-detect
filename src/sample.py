import os.path
import sys
import pandas as pd

# create a sample of the data we will be working with, using pandas.
basepath = os.path.dirname(__file__)
dataset_path = os.path.abspath(os.path.join(basepath,"..","CTU-13-Dataset"))

# generate a summary of the dataset
# There are 13 files in the directory, for a total size of about 2.5GB
# dictionary to hold information about the dataset.
dataset_info = {}
directory = os.fsencode(dataset_path)

def binet_summary_to_md(summaries):
    '''
    Expects a dict of summaries of binet flow files.
    it will spit out a markdown formatted table of the summaries.
    '''
    template_header = \
    '|Scen.|Total Flows|Botnet Flows|Normal Flows|C&C Flows|Background Flows|\n' + \
    '|---|---|---|---|---|---|\n'
    
    # This is hacky...
    template_row = \
    '|{}|{}|{}({:.2f}%)|{}({:.2f}%)|{}({:.2f}%)|{}({:.2f}%)|\n'

    output = template_header
    i = 1
    for s in summaries:
        output = output + template_row.format(\
            i,\
            str(s['total_flows']),\
            str(s['botnet_flows']), (s['botnet_flows'] / s['total_flows'] * 100),\
            str(s['normal_flows']), (s['normal_flows'] / s['total_flows'] * 100),\
            str(s['cc_flows']), (s['cc_flows'] / s['total_flows'] * 100),\
            str(s['bg_flows']), (s['bg_flows'] / s['total_flows'] * 100)\
        )
        i = i + 1
    return output

def summarize_binet_file(f):
    '''
    @arg f - pandas dataframe representing a parsed CTU-13 binetflow file.

    Each file has the following information associated with it;
    Total Flows, Botnet Flows, Normal Flows, C&C Flows, Background Flows
    '''
    file_summary = {
        'total_flows': 0,
        'botnet_flows': 0,
        'normal_flows': 0,
        'cc_flows': 0,
        'bg_flows':0
    }

    file_summary['total_flows']  = f.size
    file_summary['botnet_flows'] = f[f['Label'].str.contains('Botnet')].size
    file_summary['normal_flows'] = f[f['Label'].str.contains('Normal')].size
    file_summary['cc_flows']     = f[(f['Label'].str.contains('Botnet')) 
                                    & (f['Label'].str.contains('CC'))].size
    file_summary['bg_flows']     = f[f['Label'].str.contains('Background')].size
    
    return file_summary

print('Processing data set...')
progress = ''
i = 0
summaries = []
for f in os.listdir(directory):
    f_name = os.fsdecode(f)
    if f_name.endswith(".binetflow"):
        i = i + 1
        # in here we should us pandas to read the files and do some processing on them
        # just check really fast how we can read the Labels
        p = os.path.join(dataset_path, f_name)
        scene = pd.read_csv(p, usecols=['Label'])
        summaries.append(summarize_binet_file(scene))
        # progress bar
        progress = progress + '=' * 6
        sys.stdout.write('%d/13 Files %s\r' % (i,progress))
        sys.stdout.flush()
sys.stdout.write('\n')
sys.stdout.flush()

# Print the dataset summary table.
sys.stdout.write(binet_summary_to_md(summaries))
