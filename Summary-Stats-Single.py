"""
This routine will create a textfile containing the summary statistics for a single CAM
"""
# ----------------------------------- IMPORTS --------------------------------------#
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from network_calc import *
from AdditionalFunctions import *
import networkx as nx
# ----------------------------------------------------------------------------------#
home_dir = '/home/carterrhea/Documents/CAM-proj/Clean'
output_dir = '/home/carterrhea/Documents/CAM-proj/Output/'
# ----------------------------------------------------------------------------------#



CAMS_block = {}  # User ID : blocks
CAMS_link = {}  # User ID: links
os.chdir(home_dir)
names = []
cam_names = []
for filename in os.listdir(os.getcwd()):  # Step through files
    if filename.endswith('.csv'):
        #fileout = open(output_dir+filename.split("_")[0]+'_'+filename.split("_")[1].strip('csv')+'_summary.csv', 'a+')
        if filename.endswith('_blocks.csv'):
            #fileout.write('Number of Blocks, Neutral, Positive, Negative, Ambivalent\n')
            name = filename.split("_")[0]
            cam_name = filename.split("_")[0]+'_'+filename.split("_")[1]
            df = pd.read_csv(filename)  # Read in data
            num_blocks = len(df.index)  # Get number of blocks
            num_neutral = sum(df["shape"].str.contains('neutral'))
            num_positive = sum(df["shape"].str.contains('positive'))
            num_negative = sum(df["shape"].str.contains('negative'))
            num_ambivalent = sum(df["shape"].str.contains('ambivalent'))
            val1, val2 = valenceCalc(df)
            CAMS_block[name] = [name,num_blocks, num_neutral, num_positive, num_negative, num_ambivalent, val1, val2]  # Save number of blocks
            names.append(name)  # Add to list of names
            cam_names.append(cam_name)
            #fileout.write('%i,%i,%i,%i,%i\n'%(num_blocks, num_neutral, num_positive, num_negative, num_ambivalent))
        if filename.endswith('_links.csv'):
            name = filename.split("_")[0]#+'_'+filename.split("_")[1]
            #fileout.write('Number of Links, Solid, Dashed\n')
            df = pd.read_csv(filename)  # Read in data
            num_links = len(df.index)  # Get number of links
            num_solid = sum(df["line_style"].str.contains('Solid'))
            num_dashed = sum(df["line_style"].str.contains('Dashed'))
            CAMS_link[name] = [num_links, num_solid, num_dashed]  # Save number of links
            #fileout.write('%i,%i,%i\n' % (num_links, num_solid, num_dashed))
        #fileout.close()

df_block = pd.DataFrame.from_dict(CAMS_block, orient='index',
                            columns=['User', 'Num Blocks', 'Num Neutral', 'Num Pos', 'Num Neg', 'Num Amb', 'Avg Valence 1', 'Avg Valence 2'])
df_link = pd.DataFrame.from_dict(CAMS_link, orient='index',
                                  columns=['Num Links', 'Num Solid', 'Num Dashed'])
df = pd.concat([df_block, df_link], axis=1, sort=False)


# Graph calculations for each CAM
network_dict = {}  # CAM name: [network data]
for name,cam_name in zip(names,cam_names):
    df_blocks = pd.read_csv(os.getcwd()+'/'+cam_name+'_blocks.csv')
    df_links = pd.read_csv(os.getcwd()+'/'+cam_name+'_links.csv')
    density, diameter, triadic_closure, central_node, central_node_title, central_node_val,central_node_val_eig, central_node_val_bet = calc_density(df_blocks, df_links)
    network_dict[name] = [density, diameter, triadic_closure, central_node, central_node_title, central_node_val]

df_network = pd.DataFrame.from_dict(network_dict, orient='index',
                                  columns=['Density', 'Diameter', 'Triadic Closure', 'Central Node', 'Central Node Title', 'Central Node Value'])
print(df_network)
df = pd.concat([df, df_network], axis=1)

df = df.sort_index()
df.to_csv(output_dir+'CAMS.csv')



df['Num Blocks'].plot.hist(bins=10)
plt.ylabel('Number of CAMs')
plt.xlabel('Number of Blocks')
plt.savefig(output_dir+'Blocks.png')
plt.clf()

df['Num Links'].plot.hist(bins=10)
plt.ylabel('Number of CAMs')
plt.xlabel('Number of Links')
plt.savefig(output_dir+'Links.png')
plt.clf()


fileout = open(output_dir+'summary.csv', 'w+')
fileout.write('Mean concepts, STD concepts, Mean links, STD links\n')
fileout.write('%i,%i,%i,%i\n' % (df['Num Blocks'].mean(), df['Num Blocks'].std() ,df['Num Links'].mean(), df['Num Links'].std()))