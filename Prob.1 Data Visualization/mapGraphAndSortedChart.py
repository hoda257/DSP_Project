#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import cv2
import numpy as np
import glob
#--------------------------------------------------------------------------------------------------------------------

data_frame = pd.read_csv('covid_19_data.csv')
video_path = 'Exported Video/'
#--------------------------------------------------------------------------------------------------------------------

countries_to_plot = []
for country in data_frame['Country/Region']:
    if country not in countries_to_plot:
        countries_to_plot.append(country)
#--------------------------------------------------------------------------------------------------------------------
        
days = []
for day in data_frame['ObservationDate']:
    if day not in days:
        days.append(day)
#--------------------------------------------------------------------------------------------------------------------

all_days = data_frame['ObservationDate']
countries = data_frame['Country/Region']
deaths = data_frame['Deaths'] 
confirmed_cases = data_frame['Confirmed']
recovered = data_frame['Recovered']


# In[14]:


# Problem 1.B.

fig_1 = 0
#--------------------------------------------------------------------------------------------------------------------

def map_plot(y, rang):
    global fig_1 
    fig_1 = px.choropleth(data_frame, locationmode= 'country names', locations= countries, color= y, 
                          animation_frame= all_days, projection= 'natural earth', range_color=(0, rang),
                          color_continuous_scale= 'sunset', labels= {'color': str(y)})
    fig_1.show()
#-------------------------------------------------------------------------------------------------------------------- 

def export(fig, video_name):
    for i in range(len(fig.frames)):
        frame = go.Figure(fig.frames[i].data, fig.layout)
        frame.write_image(video_path +'image'+ str(i) +'.png')
        
    img_array = []
    for filename in glob.glob(video_path +'*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    
    if len(img_array) != 0:
        out = cv2.VideoWriter(video_path + video_name + '.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

        for i in range(len(img_array)):
            out.write(img_array[i])

        out.release()
#--------------------------------------------------------------------------------------------------------------------
    
map_plot(confirmed_cases, 30000)
export(fig_1, 'Map graph video of cases')
map_plot(deaths, 4000)
export(fig_1, 'Map graph video of deaths')


# In[8]:


# Problem 1.C.

fig_2 = 0
#--------------------------------------------------------------------------------------------------------------------

def bar_chart_plot(y_axis):
    global fig_2
    fig_2 = px.bar(data_frame, x= countries, y= y_axis,
                   color= countries, animation_frame= all_days)
    fig_2.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})

    fig_2.show() 
#--------------------------------------------------------------------------------------------------------------------

bar_chart_plot(confirmed_cases)
export(fig_2, 'Sorted chart video of cases')
bar_chart_plot(deaths)
export(fig_2, 'Sorted chart video of deaths')


# In[10]:


# Problem 1.D.

#--------------------------------------------------------------------------------------------------------------------

fig_3 = px.scatter(data_frame, x= deaths, y= recovered, range_x= (-2500, 40000), range_y= (-2500, 80000),
                   size= confirmed_cases, color= countries, animation_frame= all_days,
                   hover_name='Country/Region', size_max= 100)
fig_3.show()
#--------------------------------------------------------------------------------------------------------------------

export(fig_3, '1.D. video')

