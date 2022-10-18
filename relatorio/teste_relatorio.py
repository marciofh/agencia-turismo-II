from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route("/", methods=["GET"])
def seleciona_filtros():
    _dict = {
        "cidade":["São Paulo", "Porto Alegre", "Belo Horizonte", "Manaus", "Rio de Janeiro"],
    }

    return render_template('Filtros.html', content =_dict)

@app.route("/relatorio", methods=["POST"])
def gerar_relatorio():
    cidade1 = request.form.get('cidade1')
    cidade2 = request.form.get('cidade2')
    
    df = pd.DataFrame({
        'cidade': [cidade1, cidade2],
        'Amount': [4, 5],
        'City': [cidade1, cidade2]
    })

    fig = px.bar(df, x='cidade', y='Amount', color='City', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('Relatorio.html', graphJSON=graphJSON)

if __name__ == "__main__":
    app.run()