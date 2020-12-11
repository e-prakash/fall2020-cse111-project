import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors

from ..Common import DBTypes
from .import ValueCheck
from time import gmtime, strftime
import folium

Action = DBTypes.EnumReq.Action
Fields = DBTypes.EnumReq.Fields
ResFields = DBTypes.EnumRes

eq_template = """
<h5>{}</h5>
<h3>{}, {}, {} - {}</h3>
<h4>{} {}, {} {}:{}:{} UTC</h4>
<h5>(Lon: {}°, Lat: {}°), Depth: {} km</h5>
<h5>{}</h5>
<h5>Verified by: {}</h5>
"""

ne_template = """
<h5>{}</h5>
<h3>{}, {}, {} - {}</h3>
<h4>{} {}, {} {}:{}:{} UTC</h4>
<h5>(Lon: {}°, Lat: {}°), Depth: {} km</h5>
<h5>{}</h5>
<h5>Verified by: {}</h5>
<h5>Yield: {} kt, {}</h5>
"""

def getColor(mag):
        if mag >= 0 and mag < 2:
                return "#00ff00"
        elif mag>=2 and mag <5:
                return "#ffff00"
        elif mag>=5 and mag<7:
                return "#ffa500"
        else:
                return "#ff0000"

def getRadius(mag):
        return mag * 2.5

def showGraph(data, graphSelection):

        if "Aggregate" in graphSelection:
                x = data[ResFields.Graph.XValue]
                y = data[ResFields.Graph.YValue]
                x_pos = [i for i, _ in enumerate(x)]

                plt.bar(x_pos, y, color=['g', 'r', 'c', 'm', 'y', 'b'])
                plt.title(graphSelection)
                plt.xticks(x_pos, x)
                plt.xticks(rotation=90)
                plt.show()
        else:
                names = list(set(data[ResFields.Graph.XValue]))
                values = {}
                for name in names:
                        values[name] = [[],[]]
                for name, xval, yval in zip(data[ResFields.Graph.XValue], data[ResFields.Graph.Year], data[ResFields.Graph.YValue]):
                        values[name][0].append(xval)
                        values[name][1].append(yval)

                fig, ax = plt.subplots()
                for name in values:
                        values[name][0], values[name][1] = zip(*sorted(zip(values[name][0], values[name][1])))
                        ax.plot(values[name][0], values[name][1], label=name)
                if len(values) == 0:
                        ax.plot([0,1],[1,1],label = 'NO VALUES FOR CURRENT SELECTION')
                ax.legend()
                plt.title(graphSelection)
                plt.show()

def showMap(data, isNuclear):
        months = ['None', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
        m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)
        for i in range(len(data[ResFields.Earthquake.Key])):
                entry = {}
                for key in data:
                        entry[key] = data[key][i]
                dt = ValueCheck.julianToDatetime(entry[ResFields.Earthquake.Time])
                eqsrcs = ','.join(list(set(entry[ResFields.Report.EarthquakeSourceMappingSourceKeys].split(','))))
                if not isNuclear:
                        popup = eq_template.format(
                                entry[ResFields.Earthquake.Key],
                                entry[ResFields.City.Name],
                                entry[ResFields.State.Name],
                                entry[ResFields.Nation.Name],
                                entry[ResFields.Earthquake.Mag],
                                dt[2], months[dt[1]], dt[0], dt[3], dt[4], dt[5],
                                entry[ResFields.Earthquake.Longitude],
                                entry[ResFields.Earthquake.Latitude],
                                entry[ResFields.Earthquake.Depth],
                                entry[ResFields.Earthquake.Type],
                                eqsrcs
                        )
                else:
                        popup = ne_template.format(
                                entry[ResFields.Earthquake.Key],
                                entry[ResFields.City.Name],
                                entry[ResFields.State.Name],
                                entry[ResFields.Nation.Name],
                                entry[ResFields.Earthquake.Mag],
                                dt[2], months[dt[1]], dt[0], dt[3], dt[4], dt[5],
                                entry[ResFields.Earthquake.Longitude],
                                entry[ResFields.Earthquake.Latitude],
                                entry[ResFields.Earthquake.Depth],
                                entry[ResFields.Earthquake.Type],
                                eqsrcs,
                                entry[ResFields.Nuclear.Yield],
                                entry['ne_nationname']
                        )
                folium.CircleMarker(
                        location=[entry[ResFields.Earthquake.Latitude], entry[ResFields.Earthquake.Longitude]],
                        popup=popup,
                        radius=getRadius(entry[ResFields.Earthquake.Mag]),
                        color=getColor(entry[ResFields.Earthquake.Mag]),
                        fill=True,
                        fill_color=getColor(entry[ResFields.Earthquake.Mag]),
                        fill_opacity=0.4,
                        weight=1,
                        opacity=0
                ).add_to(m)
        
        fname = "output/view-" + strftime("%Y-%m-%d--%H-%M-%S", gmtime()) + ".html"
        m.save(fname)
        with open(fname, "r") as in_file:
                buf = in_file.readlines()

        with open(fname, "w") as out_file:
                for line in buf:
                        if "</head>" in line:
                                line = "<style>.leaflet-popup.leaflet-zoom-animated{width:350px}</style>" + line
                        out_file.write(line)
        return fname