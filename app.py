import io
import base64
from flask import Flask,render_template,request,url_for,redirect,Response
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
app = Flask(__name__)

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

# @app.route('/<method>',methods=["POST"])
# def AlgoRoute(method):
#     return f"<h1>{method}</h1>"



@app.route('/Prims',methods=['GET','POST'])
def Prims():
    if request.method =="POST":
        no_of_edges=request.form["edges"]
        message=request.form["message"]
        print(no_of_edges)
        print(message)
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
    img = io.BytesIO()
    xpoints = np.array([0, 6])
    ypoints = np.array([0, 250])
    plt.plot(xpoints,ypoints)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    #plt.savefig('/static/images/new_plot.png')
    return '<img src="data:image/png;base64,{}">'.format(plot_url)


if __name__=="__main__":
    app.run(debug=True)