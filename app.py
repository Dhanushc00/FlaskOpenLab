import io
import base64
from flask import Flask,render_template,request,url_for,redirect,Response
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from queue import PriorityQueue
from random import randint, uniform
import sys

import networkx as nx
import matplotlib as mpl
from matplotlib import animation,rc

rc('animation', html='html5')
mpl.rcParams['animation.ffmpeg_path'] = r'G:\\ffmpeg\\bin\\ffmpeg.exe'

app = Flask(__name__)
graph = nx.Graph()
pos = nx.spring_layout(graph)
fig, ax = plt.subplots(figsize=(6, 4))
all_edges = None


def random_node(NUM_NODES):
    return randint(1, NUM_NODES)

def prims(NUM_NODES):
    pqueue = PriorityQueue()
    global graph
    print(list(graph.nodes))
    print(list(graph.edges))
    edges_in_mst = set()
    nodes_on_mst = set()

    start_node = random_node(NUM_NODES)
    for neighbor in graph.neighbors(start_node):
        edge_data = graph.get_edge_data(start_node, neighbor)
        edge_weight = edge_data["weight"]
        pqueue.put((edge_weight, (start_node, neighbor)))

    # Loop until all nodes are in the MST
    while len(nodes_on_mst) < NUM_NODES:
        # Get the edge with smallest weight from the priority queue
        _, edge = pqueue.get(pqueue)
        print(_, edge)

        if edge[0] not in nodes_on_mst:
            new_node = edge[0]
        elif edge[1] not in nodes_on_mst:
            new_node = edge[1]
        else:
            # skip if nodes already exist
            continue

        # Every time a new node is added to the priority queue, add
        # all edges that it sits on to the priority queue.
        for neighbor in graph.neighbors(new_node):
            edge_data = graph.get_edge_data(new_node, neighbor)
            edge_weight = edge_data["weight"]
            pqueue.put((edge_weight, (new_node, neighbor)))

        # Add this edge to the MST.
        edges_in_mst.add(tuple(sorted(edge)))
        nodes_on_mst.add(new_node)

        # Yield edges in the MST to plot.
        yield edges_in_mst

def define_graph(graph, NUM_NODES,message):
    edges = message.split(',')
    for e in edges:
        n1,n2,ew = e.split(':')
        graph.add_edge(int(n1),int(n2),weight=int(ew))

def update(mst_edges):
    #print("Updated",mst_edges)
    global pos,fig,ax,graph,all_edges
    print(pos)
    ax.clear()
    labels = nx.get_edge_attributes(graph,'weight')
    nodes ={}
    for node in graph.nodes():
        nodes[node] = node
    nx.draw_networkx_nodes(graph, pos, node_size=300, ax=ax, node_color="blue", linewidths=5)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    nx.draw_networkx_labels(graph, pos, nodes, font_color='white')
    nx.draw_networkx_edges(
        graph, pos, edgelist=all_edges-mst_edges, alpha=0.25,
        edge_color='blue', width=1, ax=ax
    )
    nx.draw_networkx_edges(
        graph, pos, edgelist=mst_edges, alpha=1.0,
        edge_color='red', width=1, ax=ax
    )

def do_nothing():
    # FuncAnimation requires an initialization function. We don't
    # do any initialization, so we provide a no-op function.
    pass
    
@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method =="POST":
        meth=request.form["method"]
        if meth=='Prims':
            return redirect(url_for('Prims'))
        if meth=='BellManFord':
            return redirect(url_for('BellManFord'))
        if meth=='Dijkstra':
            return redirect(url_for('Dijkstra'))
    else:
        return render_template('index.html')

@app.route('/Prims',methods=['GET','POST'])
def Prims():
    global pos,fig,ax,graph,all_edges
    if request.method =="POST":
        message=request.form["message"]
        print(message)
        NUM_NODES = int(request.form["nodes"])


        define_graph(graph,NUM_NODES, message)
        print(list(graph.nodes))
        pos = nx.spring_layout(graph)

        all_edges = set(
            tuple(sorted((n1, n2))) for n1, n2 in graph.edges()
        )
        fig, ax = plt.subplots(figsize=(6, 4))
        ani = animation.FuncAnimation(
                fig,
                update,
                init_func=do_nothing,
                frames=prims(NUM_NODES),
                interval=600,
                repeat=False
            )
        FFwriter = animation.FFMpegWriter(fps=1)
        ani.save('static/animation.mp4', writer=FFwriter)
        return redirect(url_for('plot'))
    else:
        return render_template('Prims.html')

@app.route('/BellManFord',methods=['GET','POST'])
def BellManFord():
    if request.method =="POST":
        no_of_edges=request.form["edges"]
        message=request.form["message"]
        print(no_of_edges)
        print(message)
        return '<h1>success</h1>'
    else:
        return render_template('BellMannFord.html')

@app.route('/Dijkstra',methods=['GET','POST'])
def Dijkstra():
    if request.method =="POST":
        no_of_edges=request.form["edges"]
        message=request.form["message"]
        print(no_of_edges)
        print(message)
        return '<h1>success</h1>'
    else:
        return render_template('dijkstra.html')

@app.route('/plot',methods=['GET','POST'])
def plot():
    return render_template('plot.html')

if __name__=="__main__":

    app.run(debug=True)
