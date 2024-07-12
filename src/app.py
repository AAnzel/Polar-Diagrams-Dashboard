from dash import Dash, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

from pages import overview_detail, small_multiple


dash_app = Dash("Polar Diagrams Dashboard",
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                      dbc.icons.FONT_AWESOME],
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width"}],)
dash_app.title = "Polar Diagrams Dashboard"
# dash_app.css.config.serve_locally = True
dash_app.scripts.config.serve_locally = True
server = dash_app.server

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
                        {'label': html.Span(
                            '1. Overview+Detail - Climate',
                            style={'font-size': 20, 'padding-left': 12}),
                         'value': 'climate'
                         },
                        {'label': html.Span(
                            '2. Overview+Detail - Wine',
                            style={'font-size': 20, 'padding-left': 12}),
                         'value': 'wine'
                         },
                        {'label': html.Span(
                            '3. Overview+Detail - ML with Training Time',
                            style={'font-size': 20, 'padding-left': 12}),
                         'value': 'ml'
                         },
                        {'label': html.Span(
                            '4. Small Multiple - Gaussian Processes',
                            style={'font-size': 20, 'padding-left': 12}),
                         'value': 'gp'
                         },
                        ],
                    value='climate',
                    labelStyle={"display": "flex",
                                "align-items": "center"},
                    id='radio_button',
                    style={'margin-bottom': 40},
                    ),
                dbc.Row([
                    dbc.Col(html.H4('Source Code and Data'), width=8),
                    dbc.Col(
                        html.A(
                            html.I(className="fa-brands fa-github fa-4x",
                                   style={'margin-top': 0}),
                            href='https://github.com/AAnzel/Polar-Diagrams-Dashboard', # noqa
                            target='_blank',
                            className="d-flex justify-content-center",
                            style={'color': 'inherit'}), width=4)],
                        className="g-0", align="center",
                        style={'margin-bottom': 10}),
                html.H6('Polar Diagrams Library'),
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
                html.H6('1. Overview+Detail - Climate'),
                html.P(['• WCRP Coupled Model Intercomparison Project – ' +
                        'Phase 5: Special Issue of the ',
                        html.A(
                            'CLIVAR Exchanges Newsletter, No. 56, Vol. 15, No. 2', # noqa
                            href='http://www.clivar.org/publications/exchanges/Exchanges_56.pdf?id=45', # noqa
                            target='_blank', style={'color': 'inherit'}),
                        html.Br(),
                        '• Taylor, K.E., R.J. Stouffer, G.A. Meehl: An ' +
                        'Overview of CMIP5 and the experiment design.” Bull.' +
                        ' Amer. Meteor. Soc., 93, 485-498, 2012 ',
                        html.A(
                            'doi:10.1175/BAMS-D-11-00094.1',
                            href='http://dx.doi.org/10.1175/BAMS-D-11-00094.1',
                            target='_blank', style={'color': 'inherit'}),
                        html.Br(),
                        '• Meehl, Gerald A., and Coauthors: Decadal ' +
                        'Prediction. Bull. Amer. Meteor. Soc., 90, ' +
                        '1467–1485, 2009 ',
                        html.A(
                            'doi:10.1175/2009BAMS2778.1',
                            href='http://dx.doi.org/10.1175/2009BAMS2778.1',
                            target='_blank', style={'color': 'inherit'}),
                        html.Br(),
                        '• Meehl, G.A., and K.A. Hibbard, 2007: ',
                        html.A(
                            'A strategy for climate change stabilization ' +
                            'experiments with AOGCMs and ESMs.',
                            href='http://www.clivar.org/organization/wgcm/wgcm-10/Aspen_WhitePaper_1final.pdf?id=42', # noqa
                            target='_blank', style={'color': 'inherit'}),
                        ' WCRP Informal ' +
                        'Report No. 3/2007, ICPO Publication No. 112, IGBP ' +
                        'Report No. 57, World Climate Research Programme: ' +
                        'Geneva, 35 pp.',
                        html.Br(),
                        '• Hibbard, K. A., G. A. Meehl, P. Cox, and P. ' +
                        'Friedlingstein (2007): A strategy for climate ' +
                        'change stabilization experiments. EOS, 88, 217, ',
                        html.A(
                            'doi:10.1029/2007EO200002',
                            href='http://dx.doi.org/10.1029/2007EO200002',
                            target='_blank', style={'color': 'inherit'}),
                        html.Br(),
                        '• Waliser, D., Gleckler, P. J., Ferraro, R., Taylor' +
                        ', K. E., Ames, S., Biard, J., Bosilovich, M. G., ' +
                        'Brown, O., Chepfer, H., Cinquini, L., Durack, P. ' +
                        'J., Eyring, V., Mathieu, P.-P., Lee, T., Pinnock, ' +
                        'S., Potter, G. L., Rixen, M., Saunders, R., Schulz,' +
                        ' J., Thépaut, J.-N., and Tuma, M (2020): ' +
                        'Observations for Model Intercomparison Project ' +
                        '(Obs4MIPs): status for CMIP6, Geosci. Model Dev., ' +
                        '13, 2945–2958, ',
                        html.A(
                            'https://doi.org/10.5194/gmd-13-2945-2020',
                            href='https://doi.org/10.5194/gmd-13-2945-2020',
                            target='_blank', style={'color': 'inherit'}),
                        ],
                       style={'font-size': 12, 'color': 'dimgray'}),
                html.H6('2. Overview+Detail - Wine'),
                html.P(['Cortez, P., Cerdeira, A., Almeida, F., Matos, T., ' +
                        '& Reis, J. (2009). Modeling wine preferences by ' +
                        'data mining from physicochemical properties. In ' +
                        'Decision Support Systems (Vol. 47, Issue 4, pp. ' +
                        '547–553). Elsevier BV. ',
                        html.A(
                            'https://doi.org/10.1016/j.dss.2009.05.016',
                            href='https://doi.org/10.1016/j.dss.2009.05.016',
                            target='_blank', style={'color': 'inherit'})],
                       style={'font-size': 12, 'color': 'dimgray'}),
                html.H6('3. Overview+Detail - ML with Training Time'),
                html.P(['Horton, P., & Nakai, K. (1996, June). A ' +
                        'probabilistic classification system for predicting ' +
                        'the cellular localization sites of proteins. In ' +
                        'Ismb (Vol. 4, pp. 109-115). ',
                        html.A(
                            'https://dl.acm.org/doi/10.5555/645631.662879',
                            href='https://dl.acm.org/doi/10.5555/645631.662879', # noqa
                            target='_blank', style={'color': 'inherit'})],
                       style={'font-size': 12, 'color': 'dimgray'}),
                html.H6('4. Small Multiple - Gaussian Processes'),
                html.P(['Yang, Z., Dai, X., Dubey, A., Hirche, S., & Hattab,' +
                        'G. (2024). Whom to Trust? Elective Learning for ' +
                        'Distributed Gaussian Process Regression (Version ' +
                        '1). arXiv. ',
                        html.A(
                            'https://doi.org/10.48550/ARXIV.2402.03014',
                            href='https://doi.org/10.48550/ARXIV.2402.03014',
                            target='_blank', style={'color': 'inherit'})],
                       style={'font-size': 12, 'color': 'dimgray'})
                ],
            id="offcanvas",
            title=html.H2("Polar Diagrams Dashboard",
                          style={'margin-bottom': 0}),
            is_open=False,
            style={'width': '25%', 'height': '100%'})],
            width=1,
            align='center',
            style={'margin-left': 0, 'margin-right': 0,
                   'overflow': 'scroll'}),
    dbc.Col(
        html.Div(
            html.H1("Case Study", id='main_title'),
            style={"font-family": 'open sans', 'margin-top': 40,
                   'margin-bottom': 40}),
        width=5,
        align='center',
        style={'margin-left': 0, 'margin-right': 0, 'text-align': 'left'}),
    dbc.Col(
        [
            html.Div(
                html.H3("Select diagram"),
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
            [overview_detail._layout_return(False)],
            className="g-0",
            justify="center",
            id='row_main_content'),
        dbc.Row(
            [overview_detail._layout_return(True)],
            className="g-0",
            justify="center",
            id='row_main_content'),
        dbc.Row(
            [small_multiple._layout_return()],
            className="g-0",
            justify="center",
            id='row_main_content'),
    ],
    fluid=True)


@callback(
    Output('row_main_content', 'children'),
    Output('main_title', 'children'),
    Output('selected-diagram-type', 'value'),
    Input('radio_button', 'value')
)
def display_main_content(string_button_value):
    if string_button_value == 'climate':
        return (overview_detail._layout_return(0),
                'Case Study - Climate', 'taylor')
    elif string_button_value == 'wine':
        return (overview_detail._layout_return(1),
                'Case Study - Wine', 'taylor')
    elif string_button_value == 'ml':
        return (overview_detail._layout_return(2),
                'Case Study - ML with Training Time', 'taylor')
    elif string_button_value == 'gp':
        return (small_multiple._layout_return(),
                'Case Study - Gaussian Processes', 'taylor')
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
    if button_clicked or radio_clicked:
        return not is_open
    return is_open


if __name__ == '__main__':
    dash_app.run(debug=False)
