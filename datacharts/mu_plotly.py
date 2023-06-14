import plotly.express as px

def plot_grap_green(df):
#df = px.data.gapminder().query("country=='Canada'")
    print (df)
    fig = px.line(df,  y="Biomass", title='Biomass Generation ammount')
    fig.show()