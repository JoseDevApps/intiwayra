import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt
from scipy.stats import weibull_min
# filename = '../data/WS80/MONTHLY_80m.shp'
# fn = gpd.read_file(filename)

class Viento:
    def __init__(self,lista, path_spd='../data/WS80/') -> None:
        self.lista,self.path_spd= lista, path_spd,  
    
    def find_nearest(self, lat, lon, gdf):
        target_point = Point(lon, lat)  # Convert to (lon, lat) for Shapely
        gdf["distance"] = gdf.geometry.distance(target_point)  # Compute distances
        nearest_feature = gdf.loc[gdf["distance"].idxmin()]  # Get closest row
        return nearest_feature  # Return the closest feature
    def wind(self,):
        #######################
        # Wind 80 m
        #######################
        shapefile_path =self.path_spd+ "data/WS80/MONTHLY_80m.shp"
        gdf = gpd.read_file(shapefile_path)
        points_df = pd.DataFrame(self.lista, columns=["Latitude", "Longitude"])
        nearest_features = points_df.apply(lambda row: self.find_nearest(row["Latitude"], row["Longitude"], gdf), axis=1)
        result_dfM80 = points_df.join(nearest_features.reset_index(drop=True))
        result_dfM80.to_csv('MONTHLY_80m.csv')
        self.M80 = result_dfM80
        print(result_dfM80)
        #######################
        # Distribution 80 m
        #######################
        shapefile_path =self.path_spd+ "data/WS80/DISTRIBUTION_80m.shp"
        gdf = gpd.read_file(shapefile_path)
        points_df = pd.DataFrame(self.lista, columns=["Latitude", "Longitude"])
        nearest_features = points_df.apply(lambda row: self.find_nearest(row["Latitude"], row["Longitude"], gdf), axis=1)
        result_dfD80 = points_df.join(nearest_features.reset_index(drop=True))
        self.D80 = result_dfD80
        result_dfD80.to_csv('DISTRIBUTION_80m.csv')
        print(result_dfD80)
        #######################
        # Rose 80 m
        #######################
        shapefile_path =self.path_spd+ "data/WS80/ROSE_80m.shp"
        gdf = gpd.read_file(shapefile_path)
        points_df = pd.DataFrame(self.lista, columns=["Latitude", "Longitude"])
        nearest_features = points_df.apply(lambda row: self.find_nearest(row["Latitude"], row["Longitude"], gdf), axis=1)
        result_dfR80 = points_df.join(nearest_features.reset_index(drop=True))
        self.R80 = result_dfR80
        result_dfR80.to_csv('ROSE_80m.csv')
        print(result_dfR80)
        #######################
        # Wind 140 m
        #######################
        shapefile_path =self.path_spd+ "data/WS80/MONTHLY_140m.shp"
        gdf = gpd.read_file(shapefile_path)
        points_df = pd.DataFrame(self.lista, columns=["Latitude", "Longitude"])
        nearest_features = points_df.apply(lambda row: self.find_nearest(row["Latitude"], row["Longitude"], gdf), axis=1)
        result_dfM140 = points_df.join(nearest_features.reset_index(drop=True))
        self.M140 = result_dfM140
        result_dfM140.to_csv('MONTHLY_140m.csv')        
        print(result_dfM140)
        #######################
        # Distribution 140 m
        #######################
        shapefile_path =self.path_spd+ "data/WS80/DISTRIBUTION_140m.shp"
        gdf = gpd.read_file(shapefile_path)
        points_df = pd.DataFrame(self.lista, columns=["Latitude", "Longitude"])
        nearest_features = points_df.apply(lambda row: self.find_nearest(row["Latitude"], row["Longitude"], gdf), axis=1)
        result_dfD140 = points_df.join(nearest_features.reset_index(drop=True))
        self.D140 = result_dfD140
        result_dfD140.to_csv('DISTRIBUTION_140m.csv')   
        print(result_dfD140)
        #######################
        # Rose 140 m
        #######################
        shapefile_path =self.path_spd+ "data/WS80/ROSE_140m.shp"
        gdf = gpd.read_file(shapefile_path)
        points_df = pd.DataFrame(self.lista, columns=["Latitude", "Longitude"])
        nearest_features = points_df.apply(lambda row: self.find_nearest(row["Latitude"], row["Longitude"], gdf), axis=1)
        result_dfR140 = points_df.join(nearest_features.reset_index(drop=True))
        self.R140 = result_dfR140
        result_dfR140.to_csv('ROSE_140m.csv')   
        print(result_dfR140)

    def weib(self,x,n,a):
        return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)
    def weibull(self,valores,n,a):
        # 80 M

        forma = np.float32(a)
        escala = np.float32(n)
        # sacar los parametros de weibull y su distribucion
        x = range(0,21)
        FuncWei = self.weib(x,escala,forma)*100
        # his, binEdges = np.histogram(df[CabeceraVar1], bins=binData, density=True)
        pass

        


# points = [[16.5, 68.5], [16.5, 69.3]]  # Latitude, Longitude
# ejemplo=Viento(points)
# ejemplo.wind()