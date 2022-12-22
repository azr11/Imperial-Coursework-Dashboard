import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv("modules.csv")
df2 = pd.read_csv("lectures.csv")
df["Start Date"] = pd.to_datetime(df['Start Date'], format="%d/%m/%Y %H:%M")
df["End Date"] = pd.to_datetime(df['End Date'], format="%d/%m/%Y")
df2["Start Time"] = pd.to_datetime(df2['Start Time'], format="%H:%M")#.dt.time
df2["End Time"] = pd.to_datetime(df2['End Time'], format="%H:%M")#.dt.time

app.layout = html.Div(children=[
    html.H1(children='Coursework Deadline Viewer (In Progress)'),
    html.Div(children='''
        A calendar view for courseworks in term 1 of academic year 2022-23.
    '''),
    dcc.Dropdown(["1","2","3/4"],id="year_dropdown", multi=False),
    dcc.Dropdown(id='coursework_dropdown', multi=True),
    html.H2("Coursework Timetable"),
    dcc.Graph(id='coursework_graph'),
    html.H2("Lecture Timetable"),
    dcc.Graph(id="lecture_graph")

])

@app.callback(
    Output(component_id="coursework_dropdown", component_property="options"),
    [Input(component_id="year_dropdown", component_property="value")]
)
def update_dropdown(year):
    dff = df.loc[df["Year Group"].str.contains(year)]
    dff2 = df2.loc[df2["Year Group"].str.contains(year)]
    return list(set([i for i in dff["Module Name"].unique()]+[i for i in dff2["Module Name"].unique()]))


@app.callback(
    Output(component_id="coursework_graph", component_property="figure"),
    [Input(component_id="coursework_dropdown", component_property="value")]
)
def update_graph(values):
    dff = df.loc[df["Module Name"].isin(values)]
    length = len(dff["Module Name"].unique())
    fig = px.timeline(dff, x_start="Start Date",
                  x_end="End Date", y="Module Name",height=80*length+120,
                  color="Value", text="Coursework Name", range_color=[0,dff["Value"].max()],
                  range_x=["2022-10-03", "2022-12-16"], hover_name="Value",
                  hover_data=None)

    fig.update_layout(bargap=0.5,bargroupgap=0.1, barmode="group")
    return (fig)


@app.callback(
    Output(component_id="lecture_graph", component_property="figure"),
    [Input(component_id="coursework_dropdown", component_property="value")]
)
def update_graph(values):
    dff2 = df2.loc[df2["Module Name"].isin(values)]

    fig = px.timeline(dff2, x_start="Start Time",
                  x_end="End Time", y="Day",height=1200,
                  color="Module Name", text="Module Name",
                  hover_data=None)

    fig.update_layout(bargap=0.5,bargroupgap=0.1, barmode="group",
    showlegend=False)
    return (fig)


if __name__ == '__main__':
    app.run_server(debug=True)