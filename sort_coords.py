import json
from shapely.geometry import shape, Point
import pandas as pd
import numpy as np

def add_manually(name):
    if name == "ΝΑΟΥΣΑΣ":
        return ["ΗΡΩΙΚΗΣ ΠΟΛΕΩΣ ΝΑΟΥΣΑΣ",2]
    elif name == "ΣΕΡΒΙΩΝ-ΒΕΛΒΕΝΤΟΥ":
        return ["ΣΕΡΒΙΩΝ",3]
    elif name == "ΟΡΕΣΤΙΔΟΣ":
        return ["ΟΡΕΣΤΙΑΔΑΣ",2]
    elif name == "ΛΑΡΙΣΑΙΩΝ":
        return ["ΛΑΡΙΣΑΣ",1]
    elif name == "ΚΑΛΑΜΠΑΚΑΣ":
        return ["ΜΕΤΕΩΡΩΝ",3] 
    elif name == "ΦΑΡΚΑΔΟΝΑΣ":
        return ["ΦΑΡΚΑΔΟΝΟΣ",3]  
    elif name == "ΜΩΛΟΥ-ΑΓΙΟΥ ΚΩΝΣΤΑΝΤΙΝΟΥ":
        return ["ΚΑΜΕΝΩΝ ΒΟΥΡΛΩΝ",3]     
    elif name == "ΣΤΥΛΙΔΟΣ":
        return ["ΣΤΥΛΙΔΑΣ",3]   
    elif name == "ΚΕΡΚΥΡΑΣ":
        return ["ΚΕΝΤΡΙΚΗΣ ΚΕΡΚΥΡΑΣ ΚΑΙ ΔΙΑΠΟΝΤΙΩΝ ΝΗΣΩΝ",2]     
    elif name == "ΚΕΦΑΛΟΝΙΑΣ":
        return ["ΑΡΓΟΣΤΟΛΙΟΥ",2]  
    elif name == "ΙΕΡΑΣ ΠΟΛΗΣ ΜΕΣΟΛΟΓΓΙΟΥ":
        return ["ΙΕΡΑΣ ΠΟΛΕΩΣ ΜΕΣΟΛΟΓΓΙΟΥ",2]
    elif name == "ΉΛΙΔΑΣ":
        return ["ΗΛΙΔΑΣ",2]
    elif name == "ΗΛΙΟΥΠΟΛΕΩΣ":
        return ["ΗΛΙΟΥΠΟΛΗΣ",1]
    elif name == "ΦΙΛΑΔΕΛΦΕΙΑΣ-ΧΑΛΚΗΔΟΝΟΣ":
        return ["ΝΕΑΣ ΦΙΛΑΔΕΛΦΕΙΑΣ-ΝΕΑΣ ΧΑΛΚΗΔΟΝΑΣ",1]
    elif name == "ΗΡΑΚΛΕΙΟΥ":
        return ["ΗΡΑΚΛΕΙΟΥ ΚΡΗΤΗΣ",1]     
    elif name == "ΠΕΤΡΟΥΠΟΛΕΩΣ":
        return ["ΠΕΤΡΟΥΠΟΛΗΣ",1]
    elif name == "ΠΕΙΡΑΙΩΣ":
        return ["ΠΕΙΡΑΙΑ",1]
    elif name == "ΣΑΛΑΜΙΝΟΣ":
        return ["ΣΑΛΑΜΙΝΑΣ",2]
    elif name == "ΎΔΡΑΣ":
        return ["ΥΔΡΑΣ",3]    
        # THIS DOES NOT EXIST 
    elif name == "ΑΓΚΙΣΤΡΙΟΥ":
        return ["ΑΓΚΙΣΤΡΙΟΥ",3]  
    elif name == "ΛΕΣΒΟΥ":
        return ["ΔΥΤΙΚΗΣ ΛΕΣΒΟΥ",3]   
    elif name == "ΣΑΜΟΥ":
        return ["ΔΥΤΙΚΗΣ ΣΑΜΟΥ",3]    
    elif name == "ΨΑΡΩΝ":
        return ["ΗΡΩΙΚΗΣ ΝΗΣΟΥ ΨΑΡΩΝ",3]   
        # THIS DOES NOT EXIST 
    elif name == "ΑΓΑΘΟΝΗΣΙΟΥ":
        return ["ΑΓΑΘΟΝΗΣΙΟΥ",3]  
    elif name == "ΚΑΣΟΥ":
        return ["ΗΡΩΙΚΗΣ ΝΗΣΟΥ ΚΑΣΟΥ",3]   
        # THIS DOES NOT EXIST                              
    elif name == "ΓΑΥΔΟΥ":
        return ["ΓΑΥΔΟΥ",3]   
        # THIS DOES NOT EXIST 
    elif name == "ΑΓΙΟ ΟΡΟΣ (Αυτοδιοίκητο)":
        return ["ΑΓΙΟ ΟΡΟΣ (Αυτοδιοίκητο)",3]   
    else:
        return [0,0]                                              

def add_category(lat,long):
    # load GeoJSON file containing sectors
    with open('dhmoi.geojson', encoding = 'utf-8') as f:
        js = json.load(f)

    organized_dhmoi = data = pd.read_csv('organized_dhmoi.csv')    

    # construct point based on lon/lat returned by geocoder
    # point = Point(23.818465,38.672728)
    point = Point(long,lat)

    # check each polygon to see if it contains the point
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        # print(polygon.distance(point))
        if polygon.contains(point):
            # print('Found containing polygon:', feature['properties']["LEKTIKO"])
            name = feature['properties']["LEKTIKO"]
            # ΔΗΜΟΣ
            name = name.replace("ΔΗΜΟΣ ","")
            # spaces
            name = name.replace(" - ","-")
            # ' -> A
            name = name.replace("’","Α")
            tmp = 0
            for i in range(0,organized_dhmoi.shape[0]):
                dhmos = organized_dhmoi[data.columns[1]][i]
                if dhmos==name:
                    # return organized_dhmoi[data.columns[3]][i]
                    return dhmos
                    tmp = 1
            if tmp==0:
                res = add_manually(name)
                if res[0]!=0:
                    return res[0]
                else:
                    return 0
    return 0                

stations = pd.read_csv('stations',sep=";")
# cols: name, sum, coords
data = {}
for i in range(0,stations.shape[0]):
    dhmos = add_category(stations['lat'][i],stations['long'][i])
    if dhmos!=0:
        if dhmos in data:
            data[dhmos]['sum']+=1 
            data[dhmos]['coords'].append([stations['lat'][i],stations['long'][i]])
        else:
            data[dhmos] = {'sum':1, 'coords':[[stations['lat'][i],stations['long'][i]]]}
    print(i)        

dataa = pd.DataFrame.from_dict(data, orient="index")
dataa.to_csv("stations_sum.csv",sep=';')
print(dataa)        



