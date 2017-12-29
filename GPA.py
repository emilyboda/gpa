from datetime import datetime
from tabulate import tabulate
import math
import csv

import plotly
plotly.tools.set_credentials_file(username='eboda1', api_key='SsuyI9TXxZHxSo01u3Mz')
import plotly.plotly as py
import plotly.graph_objs as go


# input term gpa
termQP = [42.67, 31.68, 48.51, 29.01, 47.32, 70.01, 33, None]
termCR = [16, 20, 14, 20, 17, 21, 14, 18]
x_labels = ["Term 1", "Term 2", "Term 3", "Term 4", "Term 5", "Term 6", "Term 7", "Term 8"]
terms = [1,2,3,4,5,6,7,8]

linewidth = [0]*12
for i in range(0,len(x_labels)):
    if i == len(x_labels):
        linewidth[i] = None
    else:
        x_labels[i] = x_labels[i]+ "<br>"+str(termCR[i])+" credits"
        linewidth[i] = (termCR[i]-8)*1.5
#print linewidth
# calculte term gpa
termGPA = [0]*len(x_labels)
for i in range(0,len(termQP)):
    if i == len(termQP)-1:
        termGPA = None
    else:
        termGPA[i] = round(termQP[i]/termCR[i]-0.005,2)
#print termGPA

# calculate overGPA, overCR, overQP
overGPA = [0]*len(x_labels)
overCR = [0]*len(x_labels)
overQP = [0]*len(x_labels)
overCR_val = 0
overQP_val = 0
for i in range(0,len(termQP)):
    if i == len(termQP)-1:
        overCR_val = overCR_val + termCR[i]
        overCR[i] = overCR_val
        overGPA[i] = None
    else:
        overCR_val = overCR_val + termCR[i]
        overQP_val = overQP_val + termQP[i]
        overCR[i] = overCR_val
        overQP[i] = overQP_val
        overGPA[i] = round(overQP_val/overCR_val-0.005,2)
#print overGPA

# calculate "If I got X this term, what would I get for my overall GPA"
ifigot = [[0]*len(x_labels) for i in range(0,5)]
GPA = 0
for i in range(0,len(ifigot)):
    for j in range(0,len(ifigot[0])):
        if j == 0:
            ifigot[i][j] = GPA
            GPA = GPA + 1
        else:
            ifigot[i][j] = round((overQP[j-1] + termCR[j]*ifigot[i][0])/overCR[j]-0.005,2)

#print ifigot
ifigot.append(overGPA)


# plot
#### what to plot?

x_data = [x_labels]*(len(ifigot))
y_data = ifigot
#print len(ifigot)
#print len(y_data)
x_headers = terms
y_headers = ["Fail all classes", "1.0 (D avg)", "2.0 (C avg)", "3.0 (B avg)", "4.0 (A avg)", "Actual GPA"]
yaxislabels = ["Fail", "1.0", "2.0", "3.0", "4.0", "Actual GPA"]

#colors
greenc = 'rgba(53,188,4,1)'
yellowc = 'rgba(247,225,23,1)'
orangec = 'rgba(255,178,102,1)'
redc = 'rgba(156,34,10,1)'
darkredc = 'rgba(48,11,3,1)'
bluec = 'rgba(0,128,255,1)'

#### plot
title = 'Plot'
labels = y_headers
colors = [darkredc,redc,orangec,yellowc,greenc,bluec]
mode_size = [12]*len(y_data)
line_size = [2]*len(y_data)

traces = []

for i in range(0, len(x_data)):
    if i == 5:
        traces.append(go.Scatter(
            x=x_data[i],
            y=y_data[i],
            fill= None,
            mode='lines+markers',
            line=dict(color=colors[i], width=line_size[i],shape='linear'),
            marker=dict(size=linewidth),
            text=None,
            connectgaps=True,
            name = yaxislabels[i],
            hoverinfo = ""
        ))
    elif i == 0:
        traces.append(go.Scatter(
            x=x_data[i],
            y=y_data[i],
            fill=None,
            mode='lines',
            line=dict(color=colors[i], width=line_size[i], dash='dot', shape='linear'),
            connectgaps=True,
            name = "If I receive an X.0 for the term, this will be my overall GPA",
            showlegend=True,
            hoverinfo = 'none',
        ))
    else:
        traces.append(go.Scatter(
            x=x_data[i],
            y=y_data[i],
            fill=None,
            mode='lines',
            line=dict(color=colors[i], width=line_size[i], dash='dot', shape='linear'),
            connectgaps=True,
            name = yaxislabels[i],
            showlegend=False,
            hoverinfo = 'none',
        ))

    # traces.append(go.Scatter(
    #     x=[x_data[i][0], x_data[i][len(x_data[0])-1]],
    #     y=[y_data[i][0], y_data[i][len(x_data[0])-1]],
    #     mode='markers',
    #     marker=dict(color=colors[i], size=mode_size[i])
    # ))

layout = go.Layout(
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=False
)

annotations = []

# Adding labels
for y_trace, labels, colors in zip(y_data, labels, colors):
    # labeling the left_side of the plot

    # labeling the right_side of the plot
    if labels != "Actual GPA":
        annotations.append(dict(xref='paper', x=0.97, y=y_trace[len(x_data[0])-1],
                                      xanchor='left', yanchor='middle',
                                      text=labels,
                                      ay = 0,
                                      font=dict(family='Arial',
                                                size=16,
                                                color=colors,),
                                      showarrow=True))


# Source
annotations.append(dict(xref='paper', yref='paper', x=1, y=-0.1,
                              xanchor='right', yanchor='top',
                              text='Made by <i>ebodes',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))

layout = go.Layout(
    title = "<em>Overall GPA</em><br>How overall GPA is effected by grades as the terms go by",
    xaxis =dict(
        fixedrange=True,
        showline=False,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        autotick=False,
        ticks='outside',
        tickcolor='rgb(204, 204, 204)',
        tickwidth=2,
        ticklen=5,
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        range=[0.0,4.0],
        fixedrange=True,
        dtick = 0.5
    ),
    annotations=annotations,
    legend=dict(orientation="h",x = 0.24,y=1.0),
    hovermode='closest',
)

fig = go.Figure(data=traces, layout=layout)
py.plot(fig, filename='new-plot')
