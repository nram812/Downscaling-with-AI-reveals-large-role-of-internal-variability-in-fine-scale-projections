"""
Created on Tue Nov  8 17:31:00 2022

@author: lewisho
"""

import time

def Scrape_WGET(file,wget_variable,ssp,startdate=1950,enddate=2100,variables=['hus','va','ua','wap','ta','zg','psl'],ssps=['historical','ssp126','ssp245','ssp370','ssp585']):


    f = open(file, "r")
    lines = (f.readlines())
    
    for i,line in enumerate(lines):
        if 'download_files="$(cat <<EOF--dataset.file.url.chksum_type.chksum' in line:
            start = i
            print(line)
        if 'EOF--dataset.file.url.chksum_type.chksum' in line:
            end = i
            print(line)
    
    
    desired_lines = lines[start+1:end]
    links = []
    for line in desired_lines:
        links.append(line.split(' ')[1])
    
    desired_links = []
    for link in links:
        if int(link.split('_')[-1].strip(".nc'")[0:4]) >= startdate and int(link.split('_')[-1].strip(".nc'")[9:13]) <= enddate:
            desired_links.append(link)
            #print(link)
            
    all_variables = {}
    for j in range(len(ssps)):
        all_variables[ssps[j]] = {}
        for i in range(len(variables)): 
            all_variables[ssps[j]][variables[i]] = []
            for link in desired_links:
                print(link.replace(wget_variable, variables[i]).replace(ssp, ssps[j]))
                all_variables[ssps[j]][variables[i]].append(link.replace(wget_variable, variables[i]).replace(ssp, ssps[j]))
# =============================================================================
#     all_variables = []
#     for j in range(len(ssps)):
#         for i in range(len(variables)): 
#             for link in desired_links:
#                 print(link.replace(wget_variable, variables[i]).replace(ssp, ssps[j]))
# 
#                 all_variables.append(link.replace(wget_variable, variables[i]).replace(ssp, ssps[j]))
# =============================================================================

    return all_variables

path = 'C:\\Users\\lewisho\\Downloads\\'
name = "wget-20221108035008.SH"
wget_variable = 'hus'
ssp = 'historical'
links = Scrape_WGET(path+name,wget_variable,ssp)
df.loc["hus"].ssp370[0].strip("'")
df = pd.DataFrame(links)