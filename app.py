from flask import Flask, Markup, render_template, request
import run
import pandas as pd
import request as r

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
labels = [
    'Correct', 'Incorrect'
]

values = [
    89, 11
]

colors = [
    "#008000", "#F7464A"]


@app.route('/pie')
def pie():
    pie_labels = labels
    pie_values = values
    return render_template('pie_chart.html', title='Accuracy with ...', max=17000, set=zip(values, labels, colors))
   
@app.route('/square', methods=['POST'])
def square():
    print(request.files)
    csv = request.files['file']
    alg = request.values['type']
    t =  request.values['threshold']
    print("Ahsan")
    print(csv)
    csv.save('data.csv')
    #f = r.get(csv)
    #df = pd.read_csv("data.csv")
    #print(df)
    print(alg)
    if alg == "rb1":
        a = run.main1('./data.csv', t)
    else:
        a = run.main2('./data.csv', t)
    return str(a)
    

if __name__ == '__main__':
    app.run()