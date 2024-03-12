import numpy as np
import astropy.units as u
import astropy.constants as const
from astroquery.simbad import Simbad
from astroquery.vizier import Vizier
from astropy.table import QTable, Table, Column, vstack
import yaml
import re
import os
import time

homedir = os.path.expanduser('~')
savedir = homedir + '/uasal/roman-psf-vetting/data/catalog_tables/'

from astropy.utils.data import clear_download_cache

clear_download_cache()

#Simbad.cache_location

savepath = savedir + 'simbad.fits'

Simbad.add_votable_fields(
    'fluxdata(U)',
    'fluxdata(B)',
    'fluxdata(V)',
    'fluxdata(R)',
    'fluxdata(I)',
    'parallax',
    'sptype',
    'morphtype',
    'measurements',
)

if not os.path.isdir(savedir):
    os.makedirs(savedir)
print("Saving to:\n{}".format(savedir))

with open("hd_id_list.yaml", 'r') as f:
    current_list = yaml.safe_load(f)

#print(current_list)

with open("all_v3_stars.yaml", 'r') as f:
    all_v3_stars = yaml.safe_load(f)
    
#print(all_v3_stars)

simbad_results = []
min_time = 1

for idx, star in enumerate(all_v3_stars):
    print("Processing ({}) {}          ".format(idx + 1, star), end = '\r')
    t0 = time.time()
    simbad_results.append(Simbad.query_object_async(star, cache = False))
    t1 = time.time()
    t_elapsed = t1 - t0
    if t_elapsed < min_time:
        time.sleep(min_time - t_elapsed)
        
simbad_table = vstack(simbad_results)

simbad_table.write(savedir + "simbad_table.fits", format = 'fits')