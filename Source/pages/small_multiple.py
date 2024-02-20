import os
import warnings
# import numpy as np
import pandas as pd
import polar_diagrams


from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate
# import plotly.graph_objects as go


_INT_CHART_WIDTH = 1400
_INT_CHART_HEIGHT = 500
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
list_pretty_names = ['Sigma F: ' + i.split('_')[0][-3:] + ', ' +
                     'Sigma L: ' + i.split('_')[1][-3:]
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

    '''
    _FLOAT_MAX_THETA =  90.0 if df_left_input[
        string_angle_measure].max() < 90 else 180.0
    float_width_division = 3.2 if _FLOAT_MAX_THETA == 180.0 else 3.6
    float_height_subtraction = 230 if _FLOAT_MAX_THETA == 180.0 else 240
    dict_margin = {'l':0, 'r':0, 't':0,
                   'b': 0} if _FLOAT_MAX_THETA == 180.0 else {'t':10, 'b':20,
                                                              'r':0}
    '''
    chart_result.update_layout(
        showlegend=False,
        width=round(_INT_CHART_WIDTH / 3.6),
        height=_INT_CHART_HEIGHT - 230)
    # width=round(_INT_CHART_WIDTH / float_width_division),
    # height=_INT_CHART_HEIGHT - float_height_subtraction,
    # margin=dict_margin)

    return chart_result, list_warnings


def _list_create_rows(df_input, string_reference_model,
                      string_diagram_type='taylor', string_mid_type='scaled'):
    list_rows = []
    list_row = []
    for int_i, tuple_dfs in enumerate(list(zip(df_input, df_input[1:]))):
        if int_i % 4 == 0:
            list_rows.append(dbc.Row(list_row, id='Row_' + str(int_i/4)))
            list_row = []

        chart_result, list_warnings = _chart_warning_create(
            list(tuple_dfs), string_reference_model, string_diagram_type,
            string_mid_type)

        list_row.append(
            dbc.Col(
                [
                    dcc.Graph(
                        id="chart_" + str(int_i),
                        figure=chart_result,
                        config={
                            'toImageButtonOptions': _DICT_FIGURE_SAVE_CONFIG,
                            'displayModeBar': True,
                            'displaylogo': False,
                            'showAxisDragHandles': False},
                        style={'margin-bottom': 0, 'margin-top': 0}),
                    html.Div(
                        dbc.Alert(
                            list_warnings,
                            color="warning",
                            id='alert-warnings',
                            is_open=True if list_warnings else False,
                            className="d-flex align-items-left",
                            style={'margin-top': 30}))
                ],
                width=3,
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
