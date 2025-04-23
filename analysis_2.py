from typing import List

import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from data_loader import DataLoader
from model import Issue,Event
import config



class Analysis2:
    """
    Implements an example analysis of GitHub
    issues and outputs the result of that analysis.
    """
    
    def __init__(self):
        # load dataset based off config
        self.DATASET:str = config.get_parameter('dataset')
        if self.DATASET == None:
            self.DATASET = 0

        self.nxG = nx.Graph()
        
        
    def run(self):
        print("Started analysis 2")
        
         # load issues
        issues:List[Issue] = DataLoader(self.DATASET).get_issues()
        
        # create nodes and edges
        nodes = []
        edges = []
        for issue in issues:
            nodes.append(issue.creator)
            for event in issue.events:
                if event.author is None:
                    continue
                nodes.append(event.author)
                if issue.creator != event.author:
                    edges.append( (issue.creator, event.author) )
        print("Done creating nodes and edges.")
        
        # add nodes and edges 
        self.nxG.add_nodes_from(nodes)
        for user1, user2 in edges:
            u, v = sorted([user1, user2])
            if self.nxG.has_edge(u, v):
                self.nxG[u][v]['weight'] += 1
            else:
                self.nxG.add_edge(u, v, weight=1)
        print("Done adding nodes and edges to network graph")
        
        # compute the layout for plotly
        pos = nx.spring_layout(self.nxG)
        
        
        # plot the data
        # Create edge traces
        edge_x = []
        edge_y = []
        mid_x = []
        mid_y = []
        mid_text = []
        for u, v, data in self.nxG.edges(data=True):
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]
            mid_x.append((x0 + x1) / 2)
            mid_y.append((y0 + y1) / 2)
            mid_text.append(f"{u} and {v}: {data['weight']} interaction(s)")
            

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines',
        )
        
        edge_hover_trace = go.Scatter(
            x=mid_x,
            y=mid_y,
            mode='markers',
            marker=dict(size=0.1, color='rgba(0,0,0,0)'),  # invisible markers
            hoverinfo='text',
            text=mid_text,
            showlegend=False
        )

        # Create node traces
        node_x = []
        node_y = []
        node_text = []
        for node in self.nxG.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"{node} - {self.nxG.degree(node)} connection(s)")  # label to show on hover

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color='lightblue',
                size=10,
                line=dict(width=2)
            ),
            text=node_text
        )

        # Combine into figure
        fig = go.Figure(data=[edge_trace, node_trace, edge_hover_trace],
                        layout=go.Layout(
                            title='Interactive Network',
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=5,r=5,t=40),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False)
                        ))

        fig.show()
                