# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 10:48:52 2018

@author: moss
"""

import random
import pandas as pd
from bokeh.io import  curdoc
from bokeh.models import ColumnDataSource, Panel, HoverTool
from bokeh.plotting import figure
from bokeh.layouts import row, WidgetBox
from bokeh.models.widgets import CheckboxGroup, Tabs



#testData = []
#x=[]
#cat=[]
#for _ in range(100):
#    testData.append(random.randint(0,100))
#    x.append(_)
#    cat.append(random.randint(1,4))
#    
#data = pd.DataFrame(data={'x':x,'y':testData,'cat':cat})
#dataCats = list(str(data['cat'].unique()))

data = pd.read_table('tcga.umap.15.tsv',header=0)
dataCats = list(str(data['tissue'].unique()))
source=ColumnDataSource(data=data)

def updateSelection(attr, old, new):
    newSelection = [selection.labels[i] for i in selection.active]
    new_source = old[newSelection]
    source.data.update(new_source)
    
def makePlot(source):
    tools=["box_select","hover","reset"]
    p = figure(plot_width = 600, plot_height = 600,tools=tools)
    p.circle(x='comp 0',y='comp 1', size = 5, hover_color ="black",source=source)
    hover=HoverTool(tooltips=[('Tissue','@tissue')])
    p.add_tools(hover)
    
    return(p)

callback=CustomJS(args=dict(source=source), code="""
			var data=source.data;
			var tissue=data['tissue'];

			var pc1=data['comp 0'];
			var pc2=data['comp 1'];

			var data1=source.data;
			var f=cb_obj.value;

			var x=[]
			var y=[];

			for(var i=0;i<pc1.length; i++){
				if(tissue[i]==f){
					x.push(pc1[i]);
					y.push(pc2[i]);
				}
			}
			data1['x']=x;
			data1['y']=y;

			source.change.emit();
""")

p = makePlot(source)
selection = CheckboxGroup(labels=dataCats, active = [1,0])
selection.on_change('active',callback)
controls=WidgetBox(selection)
layout = row(controls, p)
tab = Panel(child=layout, title='test')
tabs=Tabs(tabs=[tab])

curdoc().add_root(tabs)
#show(tabs)






#cancer_selection = CheckboxGroup(labels=list(___), active = [0,1])
#
#show(p)
#show(widgetbox(cancer_selection))
#
#
#def makePlot(data):
#    p = figure(plot_width = 600, plot_height = 600)
#    p.circle(data, size = 1)
#    
#    hover = HoverTool(tooltips=[('Cancer','@___'),
#                                (')])
#    
#
#def updatePlot(attr, old, new):
#    cancers_to_plot = [cancer_selection.labels[i] 
#        for i in cancer_selection.active]
#    new_src = data[cancers_to_plot]
#    src.data.update(new_src.data)
#    
#cancer_selection.on_change('active',updatePlot)

