import geopandas as gpd
import numpy as np
from minio import Minio
import os
import rasterio
from shapely import geometry
import pandas as pd
from tqdm import tqdm
import warnings
import requests
warnings.filterwarnings("ignore")
import random
from joblib import Parallel, delayed

## read the global_input that contains all the files in all the tiles
df_total_tiles=gpd.read_file('one_degree_tiles_equi7/global_input.geojson')
## shuffle the geopandas table
df_total_tiles=df_total_tiles.sample(frac=1)
# Convert selected columns to the desired list format, create the argument
selected_columns = ['file_name','file_path','bbox','EQUI7_TILE','TILE']  # Specify the columns you want
args = list(zip(*(df_total_tiles[col] for col in selected_columns)))
server_name='apollo'
def worker(info):
#    print(info)
    root_dir=f'/mnt/{server_name}/equi_tiling'
    file_name,file_path,bbox,equi7_tile,tile = info[0],info[1],info[2],info[3],info[4]
    var = file_name.split('_')[0]

    url=f"http://192.168.49.30:8333/tmp-global-geomorpho/latlon/v6/{tile}_{equi7_tile.lower().replace('_','.').replace('extracont','aa')}/{var}_edtm_m_30m_s_20060101_20151231_go_epsg.4326.3855_v20250619.tif"
#    print(url)
    r = requests.head(url)
    if r.status_code == 200:
        print(f'{url} has been processed')
        return

    #bbox=' '.join([str(i) for i in bbox_arr])

    s3_config = {
    'access_key': 'iwum9G1fEQ920lYV4ol9',
    'secret_access_key': 'GMBME3Wsm8S7mBXw3U4CNWurkzWMqGZ0n2rXHggS0',
    'host': '192.168.49.30:8333',
    'bucket': 'tmp-global-geomorpho'}
    client = Minio(s3_config['host'], s3_config['access_key'], s3_config['secret_access_key'], secure=False) 

    #file_name = file_name.replace('_go_',f"_{equi7_tile.lower().replace('_','.')}_")
    if var == 'geomorphon':
        resample_method = 'mode'
    else :
        resample_method = 'cubicspline'
    
    gdal_cmd = f'gdalwarp -overwrite -t_srs "+proj=longlat +datum=WGS84 +no_defs +type=crs" -tr 0.00025 0.00025 \
    -r {resample_method} -te {bbox}  --config GDAL_CACHEMAX 9216 \
    -co BLOCKXSIZE=1024 -co BLOCKYSIZE=1024 -co BIGTIFF=YES -co COMPRESS=DEFLATE \
    -co PREDICTOR=2 -co NUM_THREADS=8 -co SPARSE_OK=TRUE'
    out_dir=f"{root_dir}/{tile}_{equi7_tile.lower().replace('_','.').replace('extracont','aa')}"


    os.makedirs(out_dir,exist_ok=True)
    cmd=f"{gdal_cmd} /vsicurl/{file_path} {out_dir}/{file_name}"
    os.system(cmd)


    s3_path = f"latlon/v6/{tile}_{equi7_tile.lower().replace('_','.').replace('extracont','aa')}/{file_name}"    
    client.fput_object(s3_config['bucket'], s3_path, f'{out_dir}/{file_name}')
    print(f'http://192.168.1.30:8333/tmp-global-geomorpho/{s3_path} on S3')
    os.remove(f'{out_dir}/{file_name}')
#for i in args:
#    worker(i)
    
Parallel(n_jobs=70)(delayed(worker)(i) for i in args)