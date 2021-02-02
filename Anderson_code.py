col_list = list(cam_GLI_df.columns)
GLI_list = col_list[8:]
GLI_list

GLI_name = GLI_list[0]

P_H = 0
P_L = 0
N = 0 
N_max = 20 #number of iterations

alpha = .05 # desired level of significance


Obs_GLI = cam_GLI_df[GLI_name][0] #observed GLI



n = cam_GLI_df['node_count']  # number of nodes
m = cam_GLI_df['edge_count'] # number edges

while N <= N_max:

    # STEP 2: Make the random graph
    G_uni = nx.gnm_random_graph(n, m)


    #Get the necessary GLI measures
    # Calculate Density
    density = np.round(nx.density(G_uni), 3)

    # Calculate longest path
    try:
        components = nx.connected_components(G_uni)
        largest_component = max(components, key=len)
        subgraph = G_uni.subgraph(largest_component)
        diameter = nx.diameter(subgraph)
    except:
        diameter = 0
    # Calculate transitivity
    triadic_closure = np.round(nx.transitivity(G_uni), 3)

    # Calculate max degree
    try:
        degree_centrality = nx.degree_centrality(G_uni)
        max_centrality_ind = np.argmax(list(degree_centrality.values()))
        central_node_val = np.round(list(degree_centrality.values())[max_centrality_ind], 3)
    except:
        central_node_val = 0

    # Eigenvector Centrality
    try:
        eigenvector_centrality = nx.eigenvector_centrality(G_uni)
        max_centrality_ind = np.argmax(list(eigenvector_centrality.values()))
        central_node_val_eig = np.round(list(eigenvector_centrality.values())[max_centrality_ind], 3)
    except:
        central_node_val_eig = 0

    # Betweeness Centrality
    try:
        betweenness_centrality = nx.betweenness_centrality(G_uni)
        max_centrality_ind = np.argmax(list(betweenness_centrality.values()))
        central_node_val_bet = np.round(list(betweenness_centrality.values())[max_centrality_ind], 3)
    except:
        central_node_val_bet = 0

    # Make the dictionary
    G_uni_GLI_dict = {
        'central_node_val': central_node_val,
        'central_node_val_eig': central_node_val_eig,
        'central_node_val_bet': central_node_val_bet
    }

    #STEP 3 - #Maybe issue with have a two conditions with the 'equal to' option
    if G_uni_GLI_dict[GLI_name] >= Obs_GLI:
        P_H = P_H + 1

    elif G_uni_GLI_dict[GLI_name] <= Obs_GLI:
        P_L = P_L +1
    
    #increment N for each iteration till max is reached
    N = N + 1

#Step 5
condition_1 = (P_H/N_max) < (alpha/2)
condition_2 = (P_L/N_max) < (alpha/2)

if condition_1 | condition_2:
    print(f'Reject the Null Hypothesis')
    