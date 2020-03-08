from flask import Flask, Markup, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()