import ROOT
import argparse
import os, sys
from colorama import Fore, Style
import logging

logging.basicConfig(filename='comparison_result.log', filemode='w', format='%(levelname)s:%(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description='Provide two TREx output folders for comparison.')
parser.add_argument('first', metavar='first_path', type=str, help='path to the first folder')
parser.add_argument('second', metavar='second_path', type=str, help='path to the second folder')

args = parser.parse_args()

input_path_1 = args.first
input_path_2 = args.second

if not (os.path.isdir(input_path_1) and os.path.isdir(input_path_2)):
    logging.error('Input folder(s) does not exist.')
    sys.exit()

# write summary file
outfile = open('comparison.log','w')


# Get list of root histograms
list_hist_1 = sorted(os.listdir(f'{input_path_1}/Histograms'))
list_hist_2 = sorted(os.listdir(f'{input_path_2}/Histograms'))

# Remove input_path from file names
list_hist_1_woName = [str.replace(input_path_1,'') for str in list_hist_1]
list_hist_2_woName = [str.replace(input_path_2,'') for str in list_hist_2]

# check 1. Check number of root files and their names in the Histogram folder
# print('Checking Histograms directory...')
logging.info('Histograms directory...')
if list_hist_1_woName == list_hist_2_woName:
    # print('   Number of root files and the names are identical in the Histograms folder!')
    logging.info('   Number of root files and the names are identical in the Histograms folder!')
else:
    # print(f'{Fore.RED}   Number of root files or name of root files are not identical in the Histogram folder...{Style.RESET_ALL}')
    # outfile.write(f'   Number of root files or name of root files are not identical in the Histogram folder\n')
    logging.warning(f'   Number of root files or name of root files are not identical in the Histogram folder')
    sys.exit()

# Loop over root files
for file1, file2 in zip(list_hist_1, list_hist_2):
    try:
        f1 = ROOT.TFile.Open(f'{input_path_1}/Histograms/{file1}')
        f2 = ROOT.TFile.Open(f'{input_path_2}/Histograms/{file2}')
    except:
        logging.warning('   Cannot open root file...')
        # print('   Cannot open root file...')

    # check 2. Check number of keys in the root file
    if len(f1.GetListOfKeys()) == len(f2.GetListOfKeys()):
        logging.info(f'   Same number of keys in the root file: {file1}!')
        # print(f'   Same number of keys in the root file: {file1}!')
    else:
        logging.warning(f'   Number of keys are not identical...')
        # print(f'{Fore.RED}   Number of keys are not identical...{Style.RESET_ALL}')
        # outfile.write(f'   Number of keys are not identical...\n')
        sys.exit()

    # check 3. Check all bins of all 1-D histograms
    for key1 in f1.GetListOfKeys():
        if 'TH1' in key1.GetClassName():
            histName = key1.GetName()
            # print(histName)
            h1 = f1.Get(histName)
            h2 = f2.Get(histName)
            for x in range(1, h1.GetNbinsX()+1):
                if h1.GetBinContent(x) and h2.GetBinContent(x): 
                    if abs(h1.GetBinContent(x) - h2.GetBinContent(x))/h1.GetBinContent(x) > 1e-10:
                        logging.warning(f'      histogram {histName} - Bin content {x} is not identical - first: {h1.GetBinContent(x)} and second: {h2.GetBinContent(x)} ...')
                        # print(f'{Fore.RED}      histogram {histName} - Bin content {x} is not identical - first: {h1.GetBinContent(x)} and second: {h2.GetBinContent(x)} ... {Style.RESET_ALL}')
                        # outfile.write(f'      histogram {histName} - Bin content {x} is not identical - first: {h1.GetBinContent(x)} and second: {h2.GetBinContent(x)} ... \n')
    f1.Close()
    f2.Close()

# Compare Systematics folder
# print('Checking Systematics directory...')
logging.info('\nSystematics:')
# outfile.write('Systematics:\n')
checkSystematics = True

# Get list of folders in the Systematics 
try:
    list_sys_1 = sorted(os.listdir(f'{input_path_1}/Systematics'))
    list_sys_2 = sorted(os.listdir(f'{input_path_2}/Systematics'))
except:
    # print(f'{Fore.RED}   Systematics folder does not exist...{Style.RESET_ALL}')
    # outfile.write('   Systematics folder does not exist...\n')
    logging.warning('   Systematics folder does not exist...')
    checkSystematics = False

if checkSystematics:
    # check 4. Check the existence of systematic folders
    if list_sys_1 == list_sys_2:
        # print('   Number of systematic folders and the names are identical!')
        logging.info('   Number of systematic folders and the names are identical!')
        
        # check 5. compare each systematic folder
        for folder1, folder2 in zip(list_sys_1, list_sys_2):
            list_file1 = sorted(os.listdir(f'{input_path_1}/Systematics/{folder1}'))
            list_file2 = sorted(os.listdir(f'{input_path_2}/Systematics/{folder2}'))
            
            # check 6. check number of files in each systematic folder
            if list_file1 == list_file2:
                logging.info(f'   Number of files in the folder {folder1} are identical!')
                # print(f'   Number of files in the folder {folder1} are identical!')
                
                # check 7. compare size of png files
                for file1, file2 in zip(list_file1, list_file2):
                    if 'png' in file1:
                        file1_size = os.path.getsize(f'{input_path_1}/Systematics/{folder1}/{file1}')
                        file2_size = os.path.getsize(f'{input_path_2}/Systematics/{folder2}/{file2}')
                        if file1_size != file2_size:
                            logging.warning(f'      Systematic - {input_path_1}/Systematics/{folder1}/{file1} is not identical...')
                            # print(f'{Fore.RED}      Systematic - {input_path_1}/Systematics/{folder1}/{file1} is not identical...{Style.RESET_ALL}')
                            # outfile.write(f'      Systematic - {input_path_1}/Systematics/{folder1}/{file1} is not identical...\n')
            else:
                logging.warning(f'   Systematic - Number of files in the folder {folder1} are not identical...')
                # print(f'{Fore.RED}   Systematic - Number of files in the folder {folder1} are not identical...{Style.RESET_ALL}')
                # outfile.write(f'   Systematic - Number of files in the folder {folder1} are not identical...\n')
    else:
        logging.warning('   Systematic - different folders...')
        # print(f'{Fore.RED}   Systematic - different folders...{Style.RESET_ALL}')
        # outfile.write('   Systematic - different folders...\n')

    
