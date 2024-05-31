import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
# Import lightkurve
import lightkurve as lk
import astropy.units as u
import astropy.constants as const
# Import astropy's tables
from astropy.table import QTable
# Import yaml
import yaml
# Import os 
import os
from pprint import pprint
import time

import warnings
warnings.filterwarnings("ignore")

starttime = time.time()
nerrors = 0

## Setting up the directories for saving
#
# Git directory name
gitdir = "roman-vetting"
# Get the present working directory
pwdir = os.getcwd()
# Determine the path to the base of the git repository
basedir = pwdir.split(gitdir)[0] + gitdir + "/"
# Set the path to the data directory
datadir = basedir + "data/"
# Set the path to the candidate reports directory
canddir = datadir + "candidate_reports/"
# Create this directory if it doesn't exist
if not os.path.isdir(canddir):
    os.mkdir(canddir)
# Set this as the save directory
savedir = canddir

print("Saving to {}".format(savedir))

# Load the current candidate list
with open(canddir + "current_list.yaml", 'r') as f:
    candlist = yaml.load(f, Loader=yaml.FullLoader)

for c in candlist:
    # Create a separate directory for each candidate
    candidate_dir = (savedir + c + "/")
    # If the directory doesn't exist, create it
    if not os.path.isdir(candidate_dir):
        os.mkdir(candidate_dir)

for c in candlist:
    # Search the lightkurve catalogs
    print("Searching for light curve data for {}... ".format(c.upper()), end = "")
    sr = lk.search_lightcurve(c)
    # Convert the search results to a table
    srtable = sr.table
    print("Found {} results".format(len(srtable)))
    if len(srtable) == 0:
        print("Did not find any light curve results for {}, continuing to next candidate...".format(c))
        print("============================================", end = "\n\n")
        nerrors += 1
        continue

    # If not present, create a direcotry for the light curve data to be downloaded into
    canddir = (savedir + c + "/")
    lc_data_dir = (canddir + "lc_data/")
    if not os.path.isdir(lc_data_dir):
        os.mkdir(lc_data_dir)

    # If not present, create a directory for the light curve figures to be saved into
    lc_fig_dir = (canddir + "lc_figs/")
    if not os.path.isdir(lc_fig_dir):
        os.mkdir(lc_fig_dir)

    # Additionally, create a directory for the light curve figure metadata to be saved into
    lc_meta_dir = (lc_fig_dir + "lc_meta/")
    if not os.path.isdir(lc_meta_dir):
        os.mkdir(lc_meta_dir)
    
    print("Light curves will be downloaded into {} and figures will be saved into {}.".format(lc_data_dir, lc_fig_dir))

    # For each result in the search results, download the light curve, save the data, and plot the output
    for i in range(len(srtable)):

        # Get the row of data from srtable, convert it to a dictionary, and extract some metadata for file names
        try:
            row = srtable[i]
            metadict = dict(zip(row.colnames, row.values()))
            project = str(metadict['project'])
            author = str(metadict['author'])
            year = str(metadict['year'])
            obs_start = str(int(metadict['t_min']))
        except Exception as e:
            print("Problem encountered for {} result {}: {}".format(c, i, str(e)))
            nerrors += 1
            continue

        # First, verify that the dataproduct is a timeseries. If not, put an error in the metadata, save it, and move on.
        if not srtable['dataproduct_type'][i] == 'timeseries':
            metadict['ERROR'] = "Skipping this result because it is not a timeseries.".format(c, i)
            savemetadict = {k: str(v) for k, v in metadict.items()}
            yamlpath = (lc_meta_dir + project + "_" + author + "_" + year + "_" + obs_start +".yaml")
            with open(yamlpath, 'w') as outfile:
                yaml.dump(savemetadict, outfile, default_flow_style = False)
            print(metadict['ERROR'])
            #print("============================================", end = "\n\n")
            nerrors += 1
            continue
        
        try:
            # Download the light curve
            print("Downloading data for search result {}... ".format(i), end = "")
            lc_raw = sr[i].download(download_dir = lc_data_dir)
            print("Download complete.")
            # Get the normalization factor for the LC
            norm_factor = np.median(lc_raw.flux)
            lc = lc_raw.normalize()
            # Get the lomb-scargle periodogram
            pgram = lc.to_periodogram(
                method = 'lombscargle',
            #    normalization = 'psd',
            )
            # Get the period at maximum power
            pmaxpower = pgram.period_at_max_power
            metadict['norm_factor'] = norm_factor
            metadict['pmaxpower'] = pmaxpower
            # Get the 'project', 'author', and 'year' fields from the table as strings

            # Remove that principal signal from the light curve (roughly)
            lc_model = pgram.model(time = lc.time, frequency = pgram.frequency_at_max_power)
            newlc = lc.copy()
            newlc.flux = newlc.flux / lc_model.flux
            
            # Establish the plot filename
            plotpath = (lc_fig_dir + project + "_" + author + "_" + year + "_" + obs_start + ".png")

        except Exception as e:
            metadict['ERROR'] = "An error occurred in downloading the data for {} result {}: {}".format(c, i, str(e))
            savemetadict = {k: str(v) for k, v in metadict.items()}
            yamlpath = (lc_meta_dir + project + "_" + author + "_" + year + "_" + obs_start +".yaml")
            with open(yamlpath, 'w') as outfile:
                yaml.dump(savemetadict, outfile, default_flow_style = False)
            print(metadict['ERROR'])
            #print("============================================", end = "\n\n")
            nerrors += 1
            continue


        try:
            nrows = 3
            ncols = 3

            fig = plt.figure(
                figsize = (16, 12),
                dpi = 200,
                tight_layout = True,
            )

            gs = GridSpec(
                nrows,
                ncols,
                figure = fig,
                width_ratios = [2, 1, 1],
            )

            # Plot the light curve
            ax = fig.add_subplot(gs[0, :])
            lc.scatter(
                ax = ax,
                marker = '.',
                s = 0.5,
                color = 'black',
                label = "Normalization = " + f"{norm_factor.value:0.2e} [{norm_factor.unit:latex}]",
            )
            ax.set_title(c.upper() + " " + project + " " + author + " (" + year + ") - Light Curve")
            ax.legend(
                loc = 'best',
                fontsize = 8,
            )
            #ax.set_ylabel("Normalized Flux (norm. = " + f"{norm_factor.value:0.2e} [{norm_factor.unit:latex}]" + ")")

            # Plot a periodogram of the above light curve
            ax = fig.add_subplot(gs[1, 0])
            pgram.plot(
                ax = ax,
                color = 'black',
                label = None,
            )
            ax.axvline(
                1/pmaxpower.to(u.day).value,
                color = 'red',
                alpha = 1,
                linestyle = '-',
                linewidth = 1,
                ymin = 0.0,
                ymax = 0.2,
                label = "p (max power): {:.2f} days".format(pmaxpower.to(u.day).value),
                zorder = 10,
            )
            ax.axvline(
                1/pmaxpower.to(u.day).value,
                color = 'red',
                alpha = 0.5,
                linestyle = ':',
                linewidth = 1,
                ymin = 0.2,
                ymax = 1.0,
                #label = "P (max power): {:.2f} days".format(pmaxpower.to(u.day).value),
                zorder = 10,
            )
            ax.set_yscale('log')
            ax.set_title("Periodogram (Lomb-Scargle)")
            ax.legend()

            # Plot a phase-folded light curve based on the period of maximum power
            ax = fig.add_subplot(gs[1, 1])
            lc.fold(
                period = pmaxpower.to(u.day).value,
            ).scatter(
                ax = ax,
                marker = '.',
                s = 0.5,
                color = 'black',
                label = None,
            )
            ax.set_title("Folded LC (p = {:0.2f} d)".format(pmaxpower.to(u.day).value))

            # Plot a river plot based on the period of maximum power
            ax = fig.add_subplot(gs[1, 2])
            lc.plot_river(
                ax = ax,
                period = pmaxpower.to(u.day).value,
            #    aspect = 'auto',
            )
            ax.set_aspect('auto')
            ax.set_title("River Plot (p = {:0.2f} d)".format(pmaxpower.to(u.day).value))

            # Plot the light curve with the principal signal removed
            ax = fig.add_subplot(gs[2, :])
            newlc.scatter(
                ax = ax,
                marker = '.',
                s = 0.5,
                color = 'black',
                label = None,
            )
            ax.set_title("Light Curve - Highest power frequency removed")
            newlc.bin(pmaxpower.value).plot(
                ax = ax,
                color = 'red',
                linewidth = 2.5,
                label = "Binned (size = {:.2f} d)".format(pmaxpower.to(u.day).value),
            )
            ax.legend(
                loc = 'best',
                fontsize = 8,
            )


            # Turn each piece of the metadata into strings for saving with a dictionary comprehension
            savemetadict = {k: str(v) for k, v in metadict.items()}

            # Save the figure
            fig.savefig(
                plotpath,
                metadata = savemetadict,
            )

            # Save the metadata as a yaml file
            yamlpath = (lc_meta_dir + project + "_" + author + "_" + year + "_" + obs_start +".yaml")
            with open(yamlpath, 'w') as outfile:
                yaml.dump(savemetadict, outfile, default_flow_style = False)

            #plt.show()
            plt.close()
        
        except Exception as e:
            metadict['ERROR'] = "An error occurred in creating the plot for {} result {}: {}".format(c, i, str(e))
            savemetadict = {k: str(v) for k, v in metadict.items()}
            yamlpath = (lc_meta_dir + project + "_" + author + "_" + year + "_" + obs_start +".yaml")
            with open(yamlpath, 'w') as outfile:
                yaml.dump(savemetadict, outfile, default_flow_style = False)
            print(metadict['ERROR'])
            print("============================================", end = "\n\n")
            plt.close()
            nerrors += 1
            continue
            
        
    
    print("============================================", end = "\n\n")

endtime = time.time()
print("Light curve generation completed in: {:.1f} minutes and encountered {} issues.".format((endtime - starttime)/60, nerrors))