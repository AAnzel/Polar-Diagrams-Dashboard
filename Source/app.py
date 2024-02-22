from dash import Dash, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

from pages import overview_detail, small_multiple

# TODO: Cache all figures and visualize cached values

dash_app = Dash("Polar Diagrams Dashboard",
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                      dbc.icons.FONT_AWESOME],
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width"}],)
dash_app.title = "Polar Diagrams Dashboard"
# dash_app.css.config.serve_locally = True
dash_app.scripts.config.serve_locally = True

layout_first_row = dbc.Row([
    dbc.Col([
        dbc.Button(className='fa-solid fa-bars fa-4x', id="open_offcanvas",
                   n_clicks=0, color="light",
                   style={'height': '90%', 'width': '100%'}),
        dbc.Offcanvas(
            [
                html.H4('Case Studies'),
                dcc.RadioItems(
                    options=[
                        {'label': html.Span('1. Overview+Detail - Machine Learning (ML)', style={'font-size': 20, 'padding-left': 12}), 'value': 'bioinfo'},  # noqa
                        {'label': html.Span('2. Overview+Detail - ML with Training Time', style={'font-size': 20, 'padding-left': 12}), 'value': 'bioinfo-time'},  # noqa
                        {'label': html.Span('3. Small Multiple - Gaussian Processes', style={'font-size': 20, 'padding-left': 12}), 'value': 'gp'},  # noqa
                        ],
                    value='bioinfo',
                    labelStyle={"display": "flex",
                                "align-items": "center"},
                    id='radio_button',
                    style={'margin-bottom': 80},
                    ),
                html.H4('Source Code and Data'),
                html.H6('Polar Diagram Library'),
                html.P(['Anžel, A., Heider, D., & Hattab, G. (2023). ' +
                        'Interactive polar diagrams for model comparison.' +
                        ' In Computer Methods and Programs in Biomedicine ' +
                        '(Vol. 242, p. 107843). Elsevier BV. ',
                        html.A(
                            'https://doi.org/10.1016/j.cmpb.2023.107843',
                            href='https://doi.org/10.1016/j.cmpb.2023.107843',
                            target='_blank', style={'color': 'inherit'})],
                       style={'font-size': 12, 'color': 'dimgray'}),
                html.H5('Data Sets'),
                html.H6('1. & 2. Overview+Detail'),
                html.P(['De Cock, D. (2011). Ames, Iowa: Alternative to ' +
                        'the Boston Housing Data as an End of Semester ' +
                        'Regression Project. In Journal of Statistics ' +
                        'Education (Vol. 19, Issue 3). Informa UK Limited. ',
                        html.A(
                            'https://doi.org/10.1080/10691898.2011.11889627',
                            href='https://doi.org/10.1080/10691898.2011.11889627', # noqa
                            target='_blank', style={'color': 'inherit'})],
                       style={'font-size': 12, 'color': 'dimgray'}),
                html.H6('3. Small Multiple'),
                html.P(['Yang, Z., Dai, X., Dubey, A., Hirche, S., & Hattab,' +
                        'G. (2024). Whom to Trust? Elective Learning for ' +
                        'Distributed Gaussian Process Regression (Version ' +
                        '1). arXiv. ',
                        html.A(
                            'https://doi.org/10.48550/ARXIV.2402.03014',
                            href='https://doi.org/10.48550/ARXIV.2402.03014',
                            target='_blank', style={'color': 'inherit'})],
                       style={'font-size': 12, 'color': 'dimgray'}),
                html.A(
                    html.I(className="fa-brands fa-github fa-5x",
                           style={'margin-top': 40}),
                    href='https://github.com/AAnzel/Polar-Diagrams-Dashboard',
                    target='_blank',
                    className="d-flex justify-content-center",
                    style={'color': 'inherit'})
                ],
            id="offcanvas",
            title=html.H2("Polar Diagrams Dashboard",
                          style={'margin-bottom': 40}),
            is_open=False,
            style={'width': '25%', 'height': '100%'})],
            width=1,
            align='center',
            style={'margin-left': 0, 'margin-right': 0}),
    dbc.Col(
        html.Div(
            html.H1("Case Study - Data set NAME", id='main_title'),
            style={"font-family": 'open sans', 'margin-top': 40,
                   'margin-bottom': 40}),
        width=5,
        align='center',
        style={'margin-left': 0, 'margin-right': 0, 'text-align': 'left'}),
    dbc.Col(
        [
            html.Div(
                html.H3("Polar Diagram Type"),
                style={"font-family": 'open sans'}),
            dcc.Dropdown(
                options=[
                    {'label': 'Taylor Diagram', 'value': 'taylor'},
                    {'label': 'Scaled Mutual Information Diagram',
                        'value': 'mid scaled'},
                    {'label': 'Normalized Mutual Information Diagram',
                        'value': 'mid normalized'},],
                value='taylor',
                id='selected-diagram-type',
                clearable=False,
                searchable=False,
                optionHeight=50,
                style={'height': 40, 'font-size': 22, 'min-height': 10,
                       'text-align': 'bottom'})
        ],
        width=4,
        align='center'),
    ],
    justify="start",
    style={'background-color': 'lightgrey'}
    )

dash_app.layout = dbc.Container(
    [
        layout_first_row,
        dbc.Row(
            className="g-0",
            justify="center",
            id='row_main_content'),
    ],
    fluid=True)

dash_app.validation_layout = dbc.Container(
    [
        layout_first_row,
        dbc.Row(
            [overview_detail.layout],
            className="g-0",
            justify="center",
            id='row_main_content'),
        dbc.Row(
            [small_multiple.layout],
            className="g-0",
            justify="center",
            id='row_main_content'),
    ],
    fluid=True)


@callback(
    Output('row_main_content', 'children'),
    Output('main_title', 'children'),
    Input('radio_button', 'value')
)
def display_main_content(string_button_value):
    if string_button_value == 'bioinfo':
        return overview_detail.layout, 'Case Study - BioInfo'
    elif string_button_value == 'bioinfo-time':
        return '404', 'Case Study - BioInfo and Time'
    elif string_button_value == 'gp':
        return small_multiple.layout, 'Case Study - Gaussian Processes'
    else:
        return '404'


@callback(
    Output("offcanvas", "is_open", allow_duplicate=True),
    [Input("open_offcanvas", "n_clicks"),
     Input("radio_button", "value")],
    [State("offcanvas", "is_open")],
    prevent_initial_call=True
)
def _toggle_offcanvas(button_clicked, radio_clicked, is_open):
    # TODO: I should also add here that any radiobutton click in the canvas
    # TODO: renders the new example

    if button_clicked or radio_clicked:
        return not is_open
    return is_open


if __name__ == '__main__':
    dash_app.run(debug=True)
