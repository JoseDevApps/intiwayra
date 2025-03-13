import pandas as pd
from SolarTif import Solar
from Windspeed import Viento
import os


def process_inputs(lat, lon, option,mode,file=""):
    """ Process the inputs and return a result """
    # You can replace this logic with whatever action you need
    print(mode)
    print(option)
    csv_path =""
    df_inti = None
    print("dir df:",file)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
    parent_dir = os.path.dirname(script_dir)  # Go one folder back

    # Eolico
    if option=="Eolico":
        if mode=="excel":
            df = pd.read_excel(file,skiprows=1, )
            narray = df[['Longitude','Latitude']].to_numpy()
            larray = narray.tolist()
            ejemplo=Viento(lista=larray, path_spd=parent_dir+'/')
        else:
            ejemplo=Viento(lista=[[lon, lat]], path_spd=parent_dir+'/')
        ejemplo.wind()
        csv_path = os.path.abspath('MONTHLY_80m.csv')
    # Solar
    if option=="Irradiación Solar":
        if mode=="excel":
            df = pd.read_excel(file,skiprows=1, )
            narray = df[['Longitude','Latitude']].to_numpy()
            larray = narray.tolist()
            ejemplo=Solar(lista=larray, path_ghi=parent_dir+'/data/GHI/', path_dni=parent_dir+'/data/DNI',path_dif=parent_dir+'/data/DIF',path_tmp=parent_dir+'/data/TEMP')
        else:
            ejemplo=Solar(lista=[[lon, lat]], path_ghi=parent_dir+'/data/GHI/', path_dni=parent_dir+'/data/DNI',path_dif=parent_dir+'/data/DIF',path_tmp=parent_dir+'/data/TEMP')
        ejemplo.ghi()
        ejemplo.dhi()
        ejemplo.dif()
        ejemplo.tmp()
        df_inti = pd.DataFrame({
        'GHI_1': ejemplo.GHI_matriz[:,0],
        'GHI_2': ejemplo.GHI_matriz[:,1],
        'GHI_3': ejemplo.GHI_matriz[:,2],
        'GHI_4': ejemplo.GHI_matriz[:,3],
        'GHI_5': ejemplo.GHI_matriz[:,4],
        'GHI_6': ejemplo.GHI_matriz[:,5],
        'GHI_7': ejemplo.GHI_matriz[:,6],
        'GHI_8': ejemplo.GHI_matriz[:,7],
        'GHI_9': ejemplo.GHI_matriz[:,8],
        'GHI_10': ejemplo.GHI_matriz[:,9],
        'GHI_11': ejemplo.GHI_matriz[:,10],
        'GHI_12': ejemplo.GHI_matriz[:,11],

        'DNI_1': ejemplo.DNI_matriz[:,0],
        'DNI_2': ejemplo.DNI_matriz[:,1],
        'DNI_3': ejemplo.DNI_matriz[:,2],
        'DNI_4': ejemplo.DNI_matriz[:,3],
        'DNI_5': ejemplo.DNI_matriz[:,4],
        'DNI_6': ejemplo.DNI_matriz[:,5],
        'DNI_7': ejemplo.DNI_matriz[:,6],
        'DNI_8': ejemplo.DNI_matriz[:,7],
        'DNI_9': ejemplo.DNI_matriz[:,8],
        'DNI_10': ejemplo.DNI_matriz[:,9],
        'DNI_11': ejemplo.DNI_matriz[:,10],
        'DNI_12': ejemplo.DNI_matriz[:,11],
    

        'DIF_1': ejemplo.DIF_matriz[:,0],
        'DIF_2': ejemplo.DIF_matriz[:,1],
        'DIF_3': ejemplo.DIF_matriz[:,2],
        'DIF_4': ejemplo.DIF_matriz[:,3],
        'DIF_5': ejemplo.DIF_matriz[:,4],
        'DIF_6': ejemplo.DIF_matriz[:,5],
        'DIF_7': ejemplo.DIF_matriz[:,6],
        'DIF_8': ejemplo.DIF_matriz[:,7],
        'DIF_9': ejemplo.DIF_matriz[:,8],
        'DIF_10': ejemplo.DIF_matriz[:,9],
        'DIF_11': ejemplo.DIF_matriz[:,10],
        'DIF_12': ejemplo.DIF_matriz[:,11],

        'TMP_1': ejemplo.TMP_matriz[:,0],
        'TMP_2': ejemplo.TMP_matriz[:,1],
        'TMP_3': ejemplo.TMP_matriz[:,2],
        'TMP_4': ejemplo.TMP_matriz[:,3],
        'TMP_5': ejemplo.TMP_matriz[:,4],
        'TMP_6': ejemplo.TMP_matriz[:,5],
        'TMP_7': ejemplo.TMP_matriz[:,6],
        'TMP_8': ejemplo.TMP_matriz[:,7],
        'TMP_9': ejemplo.TMP_matriz[:,8],
        'TMP_10': ejemplo.TMP_matriz[:,9],
        'TMP_11': ejemplo.TMP_matriz[:,10],
        'TMP_12': ejemplo.TMP_matriz[:,11],

        })
        print(df_inti)
        df_inti.to_csv('SolarData.csv',index=False)
        csv_path = os.path.abspath('SolarData.csv')
        print("CSV file saved at:", csv_path)
    result = f"Processed data for coordinates ({lat}, {lon}) with option: {option} and saved in {csv_path}"
    # You can add logic to interact with datasets, run calculations, or perform other actions here
    return result, df_inti

