def check(lon, lat):
    from shapely.geometry import Point, Polygon, shape
    import shapely
    import shapefile
    import numpy as np
    import matplotlib.pyplot as plt
    import xarray as xr
    from shapely.geometry import Point, Polygon, shape
    import shapely
    import math
    from numpy import genfromtxt
    import time
    import netCDF4 as nc
    point = Point(lon, lat)
    return polygon.contains(point)


def durschn(array,Gewichtungsmatrix):   #Berechnet den Durchschnitt fuer die Regionen aus den Koordinatendaten, achtet dabei auf Fehlwerte
    import numpy as np
    bfakt=sum(sum(Gewichtungsmatrix))/(len(array)**2-np.count_nonzero(Gewichtungsmatrix == 0))
    Schnitt=sum(sum(array))/((len(array)**2-np.count_nonzero(array == 0))*bfakt)
    if Schnitt > 0:
        al=1                #Platzhalter, bringt nix au\'dfer dass ich else schreiben kann
    else:
        array1=np.nan_to_num(array)
        bfakt=sum(sum(Gewichtungsmatrix))/(len(array1)**2-np.count_nonzero(Gewichtungsmatrix == 0))
        Schnitt=sum(sum(array1))/((len(array1)**2-np.count_nonzero(array1 == 0))*bfakt)
    return Schnitt

#Funktion zur Berechnung der Prozentwerte der Ensembles, welche ueber einem gewissen Grenzwert liegen
#Fuer Grenz dann gdmer1.Prec33 z.B. einsetzen, fuer unterober entweder ein 'u' oder 'o', je nachdem, ob unter oder ueber dem
#Grenzwert der Perzentilwert gebildet werden soll (unter eig nur bei Prec33, Prec20 und Prec10 und den entspr. Variablen)
#Vor 2018 fuer Ens 25 einsetzen, danach 51
def Proz(Grenz,unterober,Ens,var,mo):
    ary=[]
    import numpy as np
    arry=[]
    for lead in range (0,7):
        for k in range (0,37):
            j=0                      #Für var lages, leges, liges, loges oder luges einsetzen (siehe unten)
            qu=Grenz[lead][mo][k]
            if unterober == 'u':
                for i in range (0,Ens):
                    if len(var[0,0]) > 38 or len(var[0,0]) < 38:
                        if var[lead][k][i] <= qu:
                            j=j+1
                    else:
                        if var[lead][i][k] <= qu:
                            j=j+1
            else:
                for i in range (0,Ens):
                    if len(var[0,0]) > 38 or len(var[0,0]) < 38:
                        if var[lead][k][i] >= qu:
                            j=j+1
                    else:
                        if var[lead][i][k] >= qu:
                            j=j+1
            ary.append((j/Ens*100))
        ary.append((j/Ens*100))
        arry.append(ary)
        ary=[]
    arry=np.asarray(arry)
    return arry

#Funktion zur Berechnung der Prozentwerte der Ensembles, welche zwischen zwei gewissen Grenzwerten liegen
#Fuer Grenz dann gdmer2.Prec20 z.B. einsetzen, fuer Grenz2 die Oberkante, also gdmer2.Prec40
#Vor 2018 fuer Ens 25 einsetzen, danach 51
#Fuer var gdf.tp einsetzen
def Proz2(Grenz,Grenz2,Ens,var,mo):    
    ary=[]
    arry=[]
    import numpy as np 
    for lead in range (0,7):
        for k in range (0,37):
            j=0
            qu=Grenz[lead][mo][k]
            que=Grenz2[lead][mo][k]
            for i in range (0,Ens):
                if len(var[0,0]) > 38 or len(var[0,0]) < 38:
                    if var[lead][k][i] <= que and var[lead][k][i] >= qu:
                        j=j+1
                else:
                    if var[lead][i][k] <= que and var[lead][i][k] >= qu:
                        j=j+1
            ary.append((j/Ens*100))
        ary.append((j/Ens*100))
        arry.append(ary)
        ary=[]
    arry=np.asarray(arry)
    return arry

def hooch(low,high,normal,region):       #Wertet aus, welches von (above normal, normal, below normal) am st\'e4rksten vertreten ist\
    liste=[low[region],high[region],normal[region]]
    maxvalue=max(low[region],high[region],normal[region])
    maxpos=liste.index(maxvalue)
    return maxpos

def hoochex(low,high,region):
    liste=[low[region],high[region]]
    maxvalue=max(low[region],high[region])
    maxpos=liste.index(maxvalue)
    return maxpos  #Wertet aus, welches von (high extreme, low extreme) am st\'e4rksten vertreten ist

def hooch5(verylow,low,normal,high,veryhigh,region):
    liste=[verylow[region],low[region],normal[region],high[region],veryhigh[region]]
    maxvalue=max(verylow[region],low[region],normal[region],high[region],veryhigh[region])
    maxpos=liste.index(maxvalue)
    return maxpos  #Wertet aus, welches von (far above normal, above normal, normal, below normal, far below normal) am st\'e4rksten vertreten ist

def gleich(low,high,normal,region): #checkt ab, ob der maximale Wert in mehr als einer Kategorien vorhanden ist
    def hooch(low,high,normal,region):       #Wertet aus, welches von (above normal, normal, below normal) am st\'e4rksten vertreten ist\
    	liste=[low[region],high[region],normal[region]]
    	maxvalue=max(low[region],high[region],normal[region])
    	maxpos=liste.index(maxvalue)
    	return maxpos
    if low[region] < 34 and high[region] < 34 and normal[region] < 34:
        return -0.5
    elif low[region] - high[region] < 1 and low[region] - high[region] > -1:
        if hooch(low,high,normal,region) == 0 or hooch(low,high,normal,region) == 1:
            return -0.5
        else:
            return hooch(low,high,normal,region)
    elif low[region] - normal[region] < 1 and low[region] - normal[region] > -1:
        if hooch(low,high,normal,region) == 0 or hooch(low,high,normal,region) == 2:
            return -0.5
        else:
            return hooch(low,high,normal,region)
    elif high[region] - normal[region] < 1 and high[region] - normal[region] > -1:
        if hooch(low,high,normal,region) == 1 or hooch(low,high,normal,region) == 2:
            return -0.5
        else:
            return hooch(low,high,normal,region)
    else:
        return hooch(low,high,normal,region)
    
def gleich5(verylow,low,normal,high,veryhigh,region):  #Das gleiche f\'fcr die Quintiles
    def hooch5(verylow,low,normal,high,veryhigh,region):
    	liste=[verylow[region],low[region],normal[region],high[region],veryhigh[region]]
    	maxvalue=max(verylow[region],low[region],normal[region],high[region],veryhigh[region])
    	maxpos=liste.index(maxvalue)
    	return maxpos
    if verylow[region] < 21 and low[region] < 21 and normal[region] < 21 and high[region] < 21 and veryhigh[region] < 21:
        return -0.5
    elif low[region] - high[region] < 1 and low[region] - high[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 3:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif low[region] - normal[region] < 1 and low[region] - normal[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 2:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif low[region] - verylow[region] < 1 and low[region] - verylow[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 0:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif low[region] - veryhigh[region] < 1 and low[region] - veryhigh[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif high[region] - normal[region] < 1 and high[region] - normal[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 3 or hooch5(verylow,low,normal,high,veryhigh,region) == 2:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif high[region] - verylow[region] < 1 and high[region] - verylow[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 3 or hooch5(verylow,low,normal,high,veryhigh,region) == 0:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif high[region] - veryhigh[region] < 1 and high[region] - veryhigh[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 3 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif normal[region] - veryhigh[region] < 1 and normal[region] - veryhigh[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif normal[region] - verylow[region] < 1 and normal[region] - verylow[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 0:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif verylow[region] - veryhigh[region] < 1 and verylow[region] - veryhigh[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif verylow[region] - low[region] < 1 and verylow[region] - low[region] > -1 and verylow[region] - normal[region] < 1 and verylow[region] - normal[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 2:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif verylow[region] - low[region] < 1 and verylow[region] - low[region] > -1 and verylow[region] - high[region] < 1 and verylow[region] - high[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 3:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif verylow[region] - low[region] < 1 and verylow[region] - low[region] > -1 and verylow[region] - veryhigh[region] < 1 and verylow[region] - veryhigh[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif verylow[region] - normal[region] < 1 and verylow[region] - normal[region] > -1 and verylow[region] - high[region] < 1 and verylow[region] - high[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 3:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif verylow[region] - normal[region] < 1 and verylow[region] - normal[region] > -1 and verylow[region] - veryhigh[region] < 1 and verylow[region] - veryhigh[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif verylow[region] - high[region] < 1 and verylow[region] - high[region] > -1 and verylow[region] - veryhigh[region] < 1 and verylow[region] - veryhigh[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 3 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif low[region] - high[region] < 1 and low[region] - high[region] > -1 and low[region] - veryhigh[region] < 1 and low[region] - veryhigh[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 3 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif low[region] - normal[region] < 1 and low[region] - normal[region] > -1 and low[region] - veryhigh[region] < 1 and low[region] - veryhigh[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif low[region] - normal[region] < 1 and low[region] - normal[region] > -1 and low[region] - high[region] < 1 and low[region] - high[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 3:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif veryhigh[region] - normal[region] < 1 and veryhigh[region] - normal[region] > -1 and veryhigh[region] - high[region] < 1 and veryhigh[region] - high[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 4 or hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 3:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif veryhigh[region] - normal[region] < 1 and veryhigh[region] - normal[region] > -1 and veryhigh[region] - high[region] < 1 and veryhigh[region] - high[region] > -1 and veryhigh[region] - low[region] < 1 and veryhigh[region] - low[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 3 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif veryhigh[region] - normal[region] < 1 and veryhigh[region] - normal[region] > -1 and veryhigh[region] - high[region] < 1 and veryhigh[region] - high[region] > -1 and veryhigh[region] - verylow[region] < 1 and veryhigh[region] - verylow[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 3 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif veryhigh[region] - low[region] < 1 and veryhigh[region] - low[region] > -1 and veryhigh[region] - high[region] < 1 and veryhigh[region] - high[region] > -1 and veryhigh[region] - verylow[region] < 1 and veryhigh[region] - verylow[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 3 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif veryhigh[region] - low[region] < 1 and veryhigh[region] - low[region] > -1 and veryhigh[region] - normal[region] < 1 and veryhigh[region] - normal[region] > -1 and veryhigh[region] - verylow[region] < 1 and veryhigh[region] - verylow[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 4:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif high[region] - low[region] < 1 and high[region] - low[region] > -1 and high[region] - normal[region] < 1 and high[region] - normal[region] > -1 and high[region] - verylow[region] < 1 and high[region] - verylow[region] > -1:
        if hooch5(verylow,low,normal,high,veryhigh,region) == 0 or hooch5(verylow,low,normal,high,veryhigh,region) == 1 or hooch5(verylow,low,normal,high,veryhigh,region) == 2 or hooch5(verylow,low,normal,high,veryhigh,region) == 3:
            return -0.5
        else:
            return hooch5(verylow,low,normal,high,veryhigh,region)
    elif high[region] - low[region] < 1 and high[region] - low[region] > -1 and high[region] - normal[region] < 1 and high[region] - normal[region] > -1 and high[region] - verylow[region] < 1 and high[region] - verylow[region] > -1 and high[region] - veryhigh[region] < 1 and high[region] - veryhigh[region] > -1:
        return -0.5
    else:
        return hooch5(verylow,low,normal,high,veryhigh,region)
    
def gleichex(low,high,region):   #Das Gleiche fuer die Extreme
    def hoochex(low,high,region):
    	liste=[low[region],high[region]]
    	maxvalue=max(low[region],high[region])
    	maxpos=liste.index(maxvalue)
    	return maxpos
    if low[region] - high[region] < 1 and low[region] - high[region] > -1:
        return -0.5
    else:
        return hoochex(low,high,region)

#Weil Bokeh mit Json-Strings arbeitet, müssen die Daten in ein Json-Format umgewandelt werden
def json_data(selectedLeadMonth,gdf):
    LM = selectedLeadMonth
    #Schreibt die Werte eines Lead Months heraus
    df_LM = gdf[gdf['Month'] == LM]
    #Merged die Shapedatei mit den Werten zu einem Dataframe
    merged = pd.merge(geometries, df_LM, on='NUTS_NAME', how='left')
    merged_json = json.loads(merged.to_json())          # Konvertiert zu json
    json_data = json.dumps(merged_json)
    return json_data


def make_plotis(field_name):    
    #Den einzelnen Kategorien weise ich jeweils eine andere Farbe zu
    #palette = ['#FFFFD9','#EDF8B1','#C7E9B4','#7FCDBB','#41B6C4','#1D91C0','#225EA8','#253494','#081D58']
    from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter, FuncTickFormatter

    # Set the format of the colorbar    
    min_range = -0.3
    max_range = 0.5
    field_format = format_df.loc[format_df['field'] == field_name, 'format'].iloc[0]
    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    
    color_mapper = LinearColorMapper(palette = palette, low = min_range, high = max_range)
    # Create color bar.
    #format_tick = NumeralTickFormatter(format=field_format)
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=10,border_line_color=None, location = (0, 0))
    # Create figure object.
    verbage = format_df.loc[format_df['field'] == field_name, 'verbage'].iloc[0]
    titl='d) Vorhersagbarkeit Juni'

    #hover tool sowie der Titel wird für jede Variable individualisiert
    #titl='d) Vorhersagbarkeit Juni'    
    p = figure(title=titl,plot_height = 700, plot_width = 550, toolbar_location = None)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False
    # Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource, fill_color = {'field' : field_name, 'transform' : color_mapper},
            line_color = 'black', line_width = 0.25, fill_alpha = 1)
    # Specify color bar layout.
    p.add_layout(color_bar, 'right')
    return p

def make_plot3(field_name):
    from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter, FuncTickFormatter
    #Hier werden die Farben der ColorBar gesettet. Da bei Temperatur hohe Werte mit Rot gekennzeichnet sind, bei Niederschlag abermit blau üblicherweise, werden
    #zwei verschiedene Paletten erstellt
    if field_name=='Prec':
          palette = ['#993404','#FE9929','#FFFFD4','#74C476','#EDF8E9','#08519C','#6BAED6','#EFF3FF','#F8F8F8']
    else:
          palette = ['#08519C','#6BAED6','#EFF3FF','#74C476','#EDF8E9','#67001F','#D6604D','#FDDBC7','#F8F8F8']

    min_range = 0   #Min-Max-Werte der Colorbar sind immer gleich, da es nur diese 10 Kategorien gibt
    max_range = 8
    field_format = '0.0'

    color_mapper = LinearColorMapper(palette = palette, low = min_range, high = max_range)

    Xlabel = {0: ' ', 1: 'below normal conditions              ', 2: ' ', 3: ' ', 4: 'normal conditions                         ', 5: ' ', 6: 'above normal conditions              ', 7: ' ', 8: 'no trend detected                        '}

    format_tick = FuncTickFormatter(code="""
              var labels = %s;
              return labels[tick] || tick;
              """ % Xlabel)    #Um statt 0-9 was Gescheites an der Colorbar stehen zu haben
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=49, formatter=format_tick, border_line_color=None, location = (0, 0))    #Color bar erstellen

    # Create figure object.
    verbage = format_df.loc[format_df['field'] == field_name, 'verbage'].iloc[0]

    #Der Titel wird flexibel gestaltet, dass es immer zu den Daten passt
    if field_name=='Prec':
        if slider.value == 0:
            titl='Probability of different conditions for Precipitation in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Precipitation in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Precipitation in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='SSRD':
        if slider.value == 0:
            titl='Probability of different conditions for Solar Surface Radiation in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Solar Surface Radiation in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Solar Surface Radiation in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='T2m':
        if slider.value == 0:
            titl='Probability of different conditions for Mean Temperature in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Mean Temperature in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Mean Temperature in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='Tmax':
        if slider.value == 0:
            titl='Probability of different conditions for Mean Maximum Temperature in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Mean Maximum Temperature in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Mean Maximum Temperature in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='Tmin':
        if slider.value == 0:
            titl='Probability of different conditions for Mean Minimum Temperature in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Mean Minimum Temperature in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Mean Minimum Temperature in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'

    p = figure(title = titl, plot_height = 700, plot_width = 800, toolbar_location = None)     #Erstellen des Plots
    
    #hover tool wird für jede Variable individualisiert
    if field_name=='Prec':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                               ('Probability of wet conditons','@Prec66'+' %'),
                               ('Probability of normal conditons','@Precno'+' %'),
                               ('Probability of dry conditons','@Prec33'+' %'),])
    elif field_name=='T2m':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                               ('Probability of warm conditons','@T2m66'+' %'),
                               ('Probability of normal conditons','@T2mno'+' %'),
                               ('Probability of cold conditons','@T2m33'+' %'),])
    elif field_name=='Tmax':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                               ('Probability of warm conditons','@T2max66'+' %'),
                               ('Probability of normal conditons','@Tmaxno'+' %'),
                               ('Probability of cold conditons','@T2max33'+' %'),])
    elif field_name=='Tmin':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                               ('Probability of warm conditons','@T2min66'+' %'),
                               ('Probability of normal conditons','@Tminno'+' %'),
                               ('Probability of cold conditons','@T2min33'+' %'),])
    elif field_name=='SSRD':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                               ('Probability of sunny conditons','@SSRD66'+' %'),
                               ('Probability of normal conditons','@SSRDno'+' %'),
                               ('Probability of cloudy conditons','@SSRD33'+' %'),])

    
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    # Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource, fill_color = {'field' : field_name, 'transform' : color_mapper},
            line_color = 'black', line_width = 0.25, fill_alpha = 1)

    p.add_layout(color_bar, 'right')    #Colorbar zum Plot dazufügen
    p.add_tools(hover)                  #Hover tool zum Plot dazufügen
    return p

def make_plot5(field_name):
    from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter, FuncTickFormatter
    #Hier werden die Farben der ColorBar gesettet. Da bei Temperatur hohe Werte mit Rot gekennzeichnet sind, bei Niederschlag abermit blau üblicherweise, werden
    #zwei verschiedene Paletten erstellt
    if field_name=='Prec5':
          palette = ['#A50F15','#FB6A4A','#FEE5D9','#993404','#FE9929','#FFFFD4','#006D2C','#74C476','#EDF8E9','#08519C','#6BAED6','#EFF3FF','#54278F','#9E9AC8','#F2F0F7','#F8F8F8']
    else:
          palette = ['#54278F','#9E9AC8','#F2F0F7','#08519C','#6BAED6','#EFF3FF','#006D2C','#74C476','#EDF8E9','#993404','#FE9929','#FFFFD4','#A50F15','#FB6A4A','#FEE5D9','#F8F8F8']

    min_range = 0   #Min-Max-Werte der Colorbar sind immer gleich, da es nur diese 10 Kategorien gibt
    max_range = 15
    field_format = '0.0'

    color_mapper = LinearColorMapper(palette = palette, low = min_range, high = max_range)

    if field_name=='Prec5':
        Xlabel = {0: 'strong dry conditions                   ', 1: ' ', 2: ' ', 3: ' ', 4: 'dry conditions                              ', 5: ' ', 6: ' ', 7: ' ', 8: 'normal conditions                       ',9: ' ',10: 'wet conditions                             ',11:' ',12: 'strong wet conditions                  ',13: ' ',14: 'no trend detected                        ', 15: 'no trend detected      '}
    elif field_name=='SSRD5':
        Xlabel = {0: 'strong cloudy conditions                ', 1: ' ', 2: ' ', 3: ' ', 4: 'cloudy conditions                           ', 5: ' ', 6: ' ', 7: ' ', 8: 'normal conditions                       ',9: ' ',10: 'sunny conditions                           ',11:' ',12: 'strong sunny conditions                ',13: ' ',14: 'no trend detected                        ', 15: 'no trend detected      '}
    else:
        Xlabel = {0: 'strong cold conditions                  ', 1: ' ', 2: ' ', 3: ' ', 4: 'cold conditions                             ', 5: ' ', 6: ' ', 7: ' ', 8: 'normal conditions                       ',9: ' ',10: 'warm conditions                            ',11:' ',12: 'strong warm conditions                 ',13: ' ',14: 'no trend detected                        ', 15: 'no trend detected      '}

    format_tick = FuncTickFormatter(code="""
              var labels = %s;
              return labels[tick] || tick;
              """ % Xlabel)    #Um statt 0-9 was Gescheites an der Colorbar stehen zu haben
    if field_name=='SSRD5':
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=51, formatter=format_tick, border_line_color=None, location = (0, 0))    #Color bar erstellen
    else:
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=49, formatter=format_tick, border_line_color=None, location = (0, 0))    #Color bar erstellen


    # Create figure object.
    verbage = format_df.loc[format_df['field'] == field_name, 'verbage'].iloc[0]

    #Der Titel wird flexibel gestaltet, dass es immer zu den Daten passt
    if field_name=='Prec5':
        if slider.value == 0:
            titl='Probability of different conditions for Precipitation in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Precipitation in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Precipitation in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='SSRD5':
        if slider.value == 0:
            titl='Probability of different conditions for Solar Surface Radiation in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Solar Surface Radiation in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Solar Surface Radiation in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='T2m5':
        if slider.value == 0:
            titl='Probability of different conditions for Mean Temperature in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Mean Temperature in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Mean Temperature in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='T2max5':
        if slider.value == 0:
            titl='Probability of different conditions for Mean Maximum Temperature in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Mean Maximum Temperature in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Mean Maximum Temperature in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='T2min5':
        if slider.value == 0:
            titl='Probability of different conditions for Mean Minimum Temperature in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Mean Minimum Temperature in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Mean Minimum Temperature in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'

    p = figure(title = titl, plot_height = 700, plot_width = 800, toolbar_location = None)     #Erstellen des Plots
    
    #hover tool wird für jede Variable individualisiert
    if field_name=='Prec5':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                            ('Probability of strong wet conditons','@Prec100'+' %'),
                            ('Probability of wet conditons','@Prec80'+' %'),
                            ('Probability of normal conditons','@Prec60'+' %'),
                            ('Probability of dry conditons','@Prec40'+' %'),
                            ('Probability of strong dry conditons','@Prec20'+' %'),])
    elif field_name=='T2m5':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                            ('Probability of strong warm conditons','@T2m100'+' %'),
                            ('Probability of warm conditons','@T2m80'+' %'),
                            ('Probability of normal conditons','@T2m60'+' %'),
                            ('Probability of cold conditons','@T2m40'+' %'),
                            ('Probability of strong cold conditons','@T2m20'+' %'),])
    elif field_name=='T2max5':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                            ('Probability of strong warm conditons','@T2max100'+' %'),
                            ('Probability of warm conditons','@T2max80'+' %'),
                            ('Probability of normal conditons','@T2max60'+' %'),
                            ('Probability of cold conditons','@T2max40'+' %'),
                            ('Probability of strong cold conditons','@T2max20'+' %'),])
    elif field_name=='T2min5':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                            ('Probability of strong warm conditons','@T2min100'+' %'),
                            ('Probability of warm conditons','@T2min80'+' %'),
                            ('Probability of normal conditons','@T2min60'+' %'),
                            ('Probability of cold conditons','@T2min40'+' %'),
                            ('Probability of strong cold conditons','@T2min20'+' %'),])
    elif field_name=='SSRD5':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                            ('Probability of strong sunny conditons','@SSRD100'+' %'),
                            ('Probability of sunny conditons','@SSRD80'+' %'),
                            ('Probability of normal conditons','@SSRD60'+' %'),
                            ('Probability of cloudy conditons','@SSRD40'+' %'),
                            ('Probability of strong cloudy conditons','@SSRD20'+' %'),])

    
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    # Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource, fill_color = {'field' : field_name, 'transform' : color_mapper},
            line_color = 'black', line_width = 0.25, fill_alpha = 1)

    p.add_layout(color_bar, 'right')    #Colorbar zum Plot dazufügen
    p.add_tools(hover)                  #Hover tool zum Plot dazufügen
    return p


def make_plotex(field_name):
    from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter, FuncTickFormatter
    #Hier werden die Farben der ColorBar gesettet. Da bei Temperatur hohe Werte mit Rot gekennzeichnet sind, bei Niederschlag abermit blau üblicherweise, werden
    #zwei verschiedene Paletten erstellt
    if field_name=='Precex':
          palette = ['#67001F','#D6604D','#FDDBC7','#053061','#4393C3','#D1E5F0','#F8F8F8']
    else:
          palette = ['#053061','#4393C3','#D1E5F0','#67001F','#D6604D','#FDDBC7','#F8F8F8']

    min_range = 0   #Min-Max-Werte der Colorbar sind immer gleich, da es nur diese 9 Kategorien gibt
    max_range = 6
    field_format = '0.0'

    color_mapper = LinearColorMapper(palette = palette, low = min_range, high = max_range)
    if field_name=='Precex':
        Xlabel = {0: ' ', 1: 'extreme dry conditions    ', 2: ' ', 3: ' ', 4: 'extreme wet conditions   ', 5: ' ', 6: 'relative normal conditions '}
    elif field_name=='SSRDex':
        Xlabel = {0: ' ', 1: 'extreme cloudy conditions    ', 2: ' ', 3: ' ', 4: 'extreme sunny conditions   ', 5: ' ', 6: 'relative normal conditions '}
    else:
        Xlabel = {0: ' ', 1: 'extreme cold conditions    ', 2: ' ', 3: ' ', 4: 'extreme warm conditions  ', 5: ' ', 6: 'relative normal conditions '}
    format_tick = FuncTickFormatter(code="""
              var labels = %s;
              return labels[tick] || tick;
              """ % Xlabel)    #Um statt 0-8 was Gescheites an der Colorbar stehen zu haben
    if field_name=='SSRDex':
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=42, formatter=format_tick, border_line_color=None, location = (0, 0))    # Create color bar
    else:
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=40, formatter=format_tick, border_line_color=None, location = (0, 0))
        
    # Create figure object.
    verbage = format_df.loc[format_df['field'] == field_name, 'verbage'].iloc[0]

    #Der Titel wird flexibel gestaltet, dass es immer zu den Daten passt
    if field_name=='Precex':
        if slider.value == 0:
            titl='Probability of different conditions for Precipitation in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Precipitation in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Precipitation in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='SSRDex':
        if slider.value == 0:
            titl='Probability of different conditions for Solar Surface Radiation in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Solar Surface Radiation in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Solar Surface Radiation in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='T2mex':
        if slider.value == 0:
            titl='Probability of different conditions for Mean Temperature in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Mean Temperature in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Mean Temperature in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='T2maxex':
        if slider.value == 0:
            titl='Probability of different conditions for Mean Maximum Temperature in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Mean Maximum Temperature in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Mean Maximum Temperature in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'
    elif field_name=='T2minex':
        if slider.value == 0:
            titl='Probability of different conditions for Mean Minimum Temperature in '+str(Monat)+'/'+str(Jahr)
        elif slider.value == 1:
            titl='Probability of different conditions for Mean Minimum Temperature in '+str(Monat)+'/'+str(Jahr)+' + 1 Lead Month'
        else:
            titl='Probability of different conditions for Mean Minimum Temperature in '+str(Monat)+'/'+str(Jahr)+' + ' +str(slider.value)+' Lead Months'

    p = figure(title = titl,                               #Erstellen des Plots
               plot_height = 750, plot_width = 750,
               toolbar_location = None)
    
    #hover tool wird für jede Variable individualisiert
    if field_name=='Precex':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                               ('Probability of extreme wet conditions','@Prec90'+' %'),
                               ('Probability of extreme dry conditons','@Prec10'+' %'),])
    elif field_name=='T2mex':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                               ('Probability of extreme warm conditons','@T2m90'+' %'),
                               ('Probability of extreme cold conditons','@T2m10'+' %'),])
    elif field_name=='T2maxex':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                               ('Probability of extreme warm conditons','@T2max90'+' %'),
                               ('Probability of extreme cold conditons','@T2max10'+' %'),])
    elif field_name=='T2minex':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                               ('Probability of extreme warm conditons','@T2min90'+' %'),
                               ('Probability of extreme cold conditons','@T2min10'+' %'),])
    elif field_name=='SSRDex':
          hover = HoverTool(tooltips = [('Region','@NUTS_NAME'),
                               ('Probability of extreme sunny conditons','@SSRD90'+' %'),
                               ('Probability of extreme cloudy conditons','@SSRD10'+' %'),])

    
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    # Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource, fill_color = {'field' : field_name, 'transform' : color_mapper},
            line_color = 'black', line_width = 0.25, fill_alpha = 1)

    p.add_layout(color_bar, 'right')    #Colorbar zum Plot dazufügen
    p.add_tools(hover)                  #Hover tool zum Plot dazufügen
    return p

def update_plot(attr, old, new):
    active = radio_button_group.active
    if active == 0:
            mnt = slider.value         #mnt ist somit der vom Slider eingestellte Monat
            new_data = json_data(mnt,gdf)

            cr = selectis.value          #cr ist das mit select ausgewählte Kriterium
            input_field = format_df.loc[format_df['verbage'] == cr, 'field'].iloc[0]

            p = make_plotis(input_field)    #Plot updaten

            layout = column(p,bokeh.models.Column(radio_button_group),bokeh.models.Column(selectis),bokeh.models.Column(slider))   #Neues Layout updaten
            curdoc().clear()                                               #Altes Dokument löschen
            curdoc().add_root(layout)                                      #Neues Document darstellen

            geosource.geojson = new_data    #Update the data
            
    if active == 1:
            mnt = slider.value         #mnt ist somit der vom Slider eingestellte Monat
            new_data = json_data(mnt,gdf)

            cr = select3.value          #cr ist das mit select ausgewählte Kriterium
            input_field = format_df.loc[format_df['verbage'] == cr, 'field'].iloc[0]

            p = make_plot3(input_field)    #Plot updaten

            layout = column(p,bokeh.models.Column(radio_button_group),bokeh.models.Column(select3),bokeh.models.Column(slider))   #Neues Layout updaten
            curdoc().clear()                                                              #Altes Dokument löschen
            curdoc().add_root(layout)                                                     #Neues Document darstellen

            geosource.geojson = new_data    #Update the data
            
    if active == 2:
            mnt = slider.value         #mnt ist somit der vom Slider eingestellte Monat
            new_data = json_data(mnt,gdf)

            cr = select5.value          #cr ist das mit select ausgewählte Kriterium
            input_field = format_df.loc[format_df['verbage'] == cr, 'field'].iloc[0]

            p = make_plot5(input_field)    #Plot updaten

            layout = column(p,bokeh.models.Column(radio_button_group),bokeh.models.Column(select5),bokeh.models.Column(slider))   #Neues Layout updaten
            curdoc().clear()                                                              #Altes Dokument löschen
            curdoc().add_root(layout)                                                     #Neues Document darstellen

            geosource.geojson = new_data    #Update the data
            
    if active == 3:
            mnt = slider.value         #mnt ist somit der vom Slider eingestellte Monat
            new_data = json_data(mnt,gdf)

            cr = selectex.value          #cr ist das mit select ausgewählte Kriterium
            input_field = format_df.loc[format_df['verbage'] == cr, 'field'].iloc[0]

            p = make_plotex(input_field)    #Plot updaten

            layout = column(p, bokeh.models.Column(radio_button_group),bokeh.models.Column(selectex),bokeh.models.Column(slider))   #Neues Layout updaten
            curdoc().clear()                                                              #Altes Dokument löschen
            curdoc().add_root(layout)                                                     #Neues Document darstellen

            geosource.geojson = new_data    #Update the data


def modify_doc(doc):
    doc.add_root(row(layout, width=800))
    doc.title = "Sliders"
    select3.on_change('value', update_plot)
    selectis.on_change('value', update_plot)
    select5.on_change('value', update_plot)
    selectex.on_change('value', update_plot)
    slider.on_change('value', update_plot)
    radio_button_group.on_change('active',update_plot)

