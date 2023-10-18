import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas

sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize= (10,6))

shp_path = "/Dhmoi/dhmoi.shp"
another_path = '/Dhmoi/mgp.shp'
myshp = open("/Dhmoi/dhmoi.shp",'rb')
mydbf = open("/Dhmoi/dhmoi.dbf",'rb')
# sf = shp.Reader(shp_path)
sf = shp.Reader(shp=myshp, dbf=mydbf, encoding = 'iso8859_7')

def read_shapefile(sf):
    fields = [x[0] for x in sf.fields[1:]]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(data=records, columns=fields)
    df = df.assign(coords=shps)
    return df

df = read_shapefile(sf)

def plot_shape(id,s=None):
    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal')
    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon,y_lat) 
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    plt.show()
    return x0, y0

def plot_map(sf, x_lim = None, y_lim = None, figsize = (11,9)):
    plt.figure(figsize = figsize)
    id=0
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')
        
        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, id, fontsize=10)
        id = id+1
    
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    plt.show()



# myshpfile = geopandas.read_file(another_path, encoding = 'iso8859_7')
# myshpfile = myshpfile.to_crs(epsg=4326)

# myshpfile.to_file('mgp.geojson', driver='GeoJSON')

myshpfile = geopandas.read_file(shp_path, encoding = 'iso8859_7')
myshpfile = myshpfile.to_crs(epsg=4326)
myshpfile.to_file('dhmoi.geojson', driver='GeoJSON')

