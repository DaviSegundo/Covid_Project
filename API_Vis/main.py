import pandas as pd
from flask import Flask, make_response, render_template, jsonify

app = Flask("covid")
app.config['SECRET_KEY'] = 'secret key'


@app.before_first_request
def before_first_request():
    global df_state
    global df_city

    df_state = pd.read_csv('data/Covid_Group_State.csv')
    df_state = df_state.rename(
        columns={'state': 'Estado', 'Porcentagem_Populacao_Confirmado': 'Pop_Confirmado_%',
                 'Confirmados_Acumulado': 'Confirmados_Acm',
                 'Obitos_Acumulados': 'Obitos_Acm', 'Populacao_Estimada': 'Pop_Estimada',
                 'Taxa_Mortalidade': 'Taxa_Mor', 'Taxa_Letalidade': 'Taxa_Let'})

    columns = ['Pop_Confirmado_%', 'Taxa_Mor', 'Taxa_Let']
    for col in columns:
        lis = []
        for i in df_state[col]:
            lis.append(f"{i}%")
        df_state[col] = lis

    df_city = pd.read_csv('data/Covid_City.csv')
    df_city = df_city.rename(
        columns={'state': 'Estado', 'Porcentagem_Populacao_Confirmado': 'Pop_Confirmado_%',
                 'Confirmados_Acumulado': 'Confirmados_Acm',
                 'Obitos_Acumulados': 'Obitos_Acm', 'Populacao_Estimada': 'Pop_Estimada',
                 'Taxa_Mortalidade': 'Taxa_Mor', 'Taxa_Letalidade': 'Taxa_Let',
                 'city': 'Cidade'})

    columns = ['Pop_Confirmado_%', 'Taxa_Mor', 'Taxa_Let']
    for col in columns:
        lis = []
        for i in df_city[col]:
            lis.append(f"{i}%")
        df_city[col] = lis


@app.route("/")
@app.route('/estado', methods=['GET'])
def state():
    return render_template("state.html", column_names=df_state.columns.values,
                           row_data=list(df_state.values.tolist()),
                           Zip=zip)


@app.route('/api/estado', methods=['GET'])
def state_api():
    return jsonify(df_state.values.tolist())


@app.route('/estado/<string:state_n>', methods=['GET'])
def state_select(state_n):

    df_state_f = df_state.query(f'Estado == "{state_n.upper()}"')
    return render_template("state.html", column_names=df_state_f.columns.values,
                           row_data=list(df_state_f.values.tolist()),
                           Zip=zip)


@app.route('/cidade', methods=['GET'])
def city():
    return render_template("state.html", column_names=df_city.columns.values,
                           row_data=list(df_city.values.tolist()),
                           Zip=zip)


@app.route('/cidade/<string:st_n>', methods=['GET'])
def city_state(st_n):
    df_city_s = df_city.query(f'Estado == "{st_n.upper()}"')
    return render_template("state.html", column_names=df_city_s.columns.values,
                           row_data=list(df_city_s.values.tolist()),
                           Zip=zip)


@app.route('/cidade/<string:st_n>/<string:city>', methods=['GET'])
def city_state_city(st_n, city):
    df_city_s = df_city.query(f'Estado == "{st_n.upper()}"')
    df_city_s_c = df_city_s.query(f'Cidade == "{city}"')
    return render_template("state.html", column_names=df_city_s_c.columns.values,
                           row_data=list(df_city_s_c.values.tolist()),
                           Zip=zip)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
