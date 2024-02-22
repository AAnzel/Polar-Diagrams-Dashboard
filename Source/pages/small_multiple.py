import os
import warnings
import pandas as pd
import polar_diagrams

from dash import dcc, html, Input, Output, callback, Patch, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


_INT_CHART_WIDTH = 1400
_INT_CHART_HEIGHT = 500
_INT_TICK_SIZE = 9
_INT_TITLE_SIZE = 12
_DICT_FIGURE_SAVE_CONFIG = {
    'format': 'png',  # one of png, svg, jpeg, webp
    'filename': 'polar_diagram',
    # 'height': 500,
    # 'width': 700,
    'scale': 6  # Multiply title/legend/axis/canvas sizes by this factor
}

path_root_data = os.path.join('..', 'Data')
path_gp_data = os.path.join(path_root_data, 'Case_Study_Gaussian_Processes',
                            'results_agent1')
list_csv_files = os.listdir(path_gp_data)
list_pretty_names = ['σ_F: ' + i.split('_')[0][-3:] + ', ' +
                     'σ_L: ' + i.split('_')[1][-3:]
                     for i in list_csv_files]
list_df = [pd.read_csv(os.path.join(path_gp_data, i)) for i in list_csv_files]

int_num_of_versions = len(list_df)


def _chart_warning_create(df_input, string_reference_model,
                          string_diagram_type, string_mid_type):
    # We monkey patch the function that prints the warnings so that it doesn't
    # require some inputs and only returns the warning message that we need
    warnings.formatwarning = lambda msg, *args, **kwargs: str(msg)

    if string_diagram_type == 'mid':
        with warnings.catch_warnings(record=True) as warning_tmp:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("default")
            chart_result = polar_diagrams.chart_create_mi_diagram(
                df_input, string_reference_model=string_reference_model,
                string_mid_type=string_mid_type)

            list_warning_caught = warning_tmp
    else:
        with warnings.catch_warnings(record=True) as warning_tmp:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("default")
            chart_result = polar_diagrams.chart_create_taylor_diagram(
                df_input,
                string_reference_model=string_reference_model)

            list_warning_caught = warning_tmp

    list_warnings = []
    int_i = 1
    for warning_tmp in list_warning_caught:
        if 'RuntimeWarning' in warnings.formatwarning(warning_tmp):
            string_one_warning = ' ' + warnings.formatwarning(
                warning_tmp)[11:].split(').')[0].replace('\\n', ' ') + ').'
            if string_one_warning in list_warnings:
                continue
            else:
                list_warnings += [
                    html.I(className="fa-solid fa-triangle-exclamation",
                           style={'margin-top': 3}),
                    string_one_warning,
                    html.Br()]
                int_i += 1

    chart_result.update_layout(
        showlegend=False,
        polar_angularaxis_tickvals=chart_result[
            'layout']['polar']['angularaxis']['tickvals'][::2],
        polar_angularaxis_ticktext=chart_result[
            'layout']['polar']['angularaxis']['ticktext'][::2],
        polar_sector=[0, 180 if string_mid_type == 'scaled' else 90],
        polar_angularaxis_tickfont_size=_INT_TICK_SIZE,
        polar_radialaxis_tickfont_size=_INT_TICK_SIZE,
        polar_radialaxis_title_font_size=_INT_TITLE_SIZE,
        title_font_size=_INT_TITLE_SIZE,
        width=round(_INT_CHART_WIDTH / 2.6),
        height=_INT_CHART_HEIGHT - 120,
        margin={'l': 50, 'r': 50},
        dragmode='select')

    return chart_result, list_warnings


def _list_create_rows(df_input, string_reference_model,
                      string_diagram_type='taylor', string_mid_type='scaled'):
    list_rows = []
    list_row = []
    list_tuple_pretty_names = list(
        zip(list_pretty_names, list_pretty_names[1:]))

    for int_i, tuple_dfs in enumerate(list(zip(df_input, df_input[1:]))):
        if int_i % 3 == 0:
            list_rows.append(dbc.Row(list_row, id='Row_' + str(int_i/4)))
            list_row = []

        # We only want to show 2 rows of 3 diagrams
        if int_i == 6:
            break

        string_hyperparam_info = (
            'Version 0 (' + list_tuple_pretty_names[int_i][0] + ')<br>' +
            'Version 1 (' + list_tuple_pretty_names[int_i][1] + ')')

        chart_result, list_warnings = _chart_warning_create(
            list(tuple_dfs), string_reference_model, string_diagram_type,
            string_mid_type)
        chart_result.add_annotation(
            dict(x=1, y=1.2, xref="paper", yref="paper", showarrow=False,
                 text=string_hyperparam_info,
                 font=dict(size=_INT_TICK_SIZE, color="black")))

        if int_i == 3:
            chart_result.update_layout(
                height=_INT_CHART_HEIGHT - 50,
                showlegend=True, legend_xref='paper',
                legend_yref='paper', legend_xanchor='left',
                legend_yanchor='bottom', legend_orientation='h', legend_y=-0.8)

        list_row.append(
            dbc.Col(
                [
                    dcc.Graph(
                        id="chart_" + str(int_i),
                        figure=chart_result,
                        config={
                            'toImageButtonOptions': _DICT_FIGURE_SAVE_CONFIG,
                            'modeBarButtonsToRemove': [
                                'zoom', 'pan', 'lasso', 'zoomIn', 'zoomOut',
                                'select', 'autoScale', 'resetScale'],
                            'displaylogo': False,
                            'showAxisDragHandles': False},
                        style={'margin-bottom': 0, 'margin-top': 0,
                               'margin-left': 0, 'margin-right': 0}),
                ],
                width=4,
                align='start',
                style={'margin-left': 0, 'margin-right': 0})
        )

    return list_rows


# ============================================================================
_STRING_DIAGRAM_TYPE = 'taylor'
_STRING_MID_TYPE = 'normalized'
_DF_INPUT = list_df
_STRING_REFERENCE_MODEL = 'True'

list_rows = _list_create_rows(_DF_INPUT, _STRING_REFERENCE_MODEL,
                              _STRING_DIAGRAM_TYPE, _STRING_MID_TYPE)
# ============================================================================


layout = dbc.Container(
    list_rows,
    id='small_multiple_rows',
    fluid=True
)


@callback(
    Output(component_id="small_multiple_rows", component_property="children",
           allow_duplicate=True),
    Input('selected-diagram-type', 'value'),
    prevent_initial_call=True
)
def update_output(string_selected_diagram_type):
    if string_selected_diagram_type == 'taylor':
        string_diagram_type = 'taylor'
        string_mid_type = None
    elif string_selected_diagram_type == 'mid scaled':
        string_diagram_type = 'mid'
        string_mid_type = 'scaled'
    else:
        string_diagram_type = 'mid'
        string_mid_type = 'normalized'

    list_rows = _list_create_rows(
        _DF_INPUT, _STRING_REFERENCE_MODEL,
        string_diagram_type, string_mid_type)

    return list_rows


@callback(
    Output(component_id="chart_0", component_property="figure",
           allow_duplicate=True),
    Output(component_id="chart_1", component_property="figure",
           allow_duplicate=True),
    Output(component_id="chart_2", component_property="figure",
           allow_duplicate=True),
    Output(component_id="chart_4", component_property="figure",
           allow_duplicate=True),
    Output(component_id="chart_5", component_property="figure",
           allow_duplicate=True),
    Input(component_id="chart_3", component_property="restyleData"),
    State('chart_0', 'figure'),
    State('chart_1', 'figure'),
    State('chart_2', 'figure'),
    State('chart_3', 'figure'),
    State('chart_4', 'figure'),
    State('chart_5', 'figure'),
    prevent_initial_call=True,
)
def _list_update_legends(list_legend_points, dict_0, dict_1, dict_2, dict_3,
                         dict_4, dict_5):

    chart_0 = Patch()
    chart_1 = Patch()
    chart_2 = Patch()
    chart_4 = Patch()
    chart_5 = Patch()

    # We check if we have an event and if the click was not empty
    if list_legend_points and list_legend_points[0]:
        # ----- One legend click gives the following output:
        # [{"visible": ["legendonly"]}, [10]]
        # [{"visible": [true]}, [1]]
        # ----- Group click:
        # [{'visible': ['legendonly', 'legendonly', True, True, 'legendonly',
        #               'legendonly', 'legendonly', 'legendonly', 'legendonly',
        #               'legendonly', 'legendonly', 'legendonly']},
        #  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        # ----- Empty legend click:
        # [{}, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        if list_legend_points:
            for int_i, int_legend_point in enumerate(list_legend_points[1]):
                if isinstance(
                    list_legend_points[0]['visible'][int_i],
                        bool) and list_legend_points[0]['visible'][int_i]:
                    chart_0['data'][int_legend_point]['visible'] = True
                    chart_1['data'][int_legend_point]['visible'] = True
                    chart_2['data'][int_legend_point]['visible'] = True
                    chart_4['data'][int_legend_point]['visible'] = True
                    chart_5['data'][int_legend_point]['visible'] = True
                else:
                    chart_0['data'][int_legend_point]['visible'] = False
                    chart_1['data'][int_legend_point]['visible'] = False
                    chart_2['data'][int_legend_point]['visible'] = False
                    chart_4['data'][int_legend_point]['visible'] = False
                    chart_5['data'][int_legend_point]['visible'] = False
    else:
        raise PreventUpdate

    return chart_0, chart_1, chart_2, chart_4, chart_5
