import os
import pandas as pd
import warnings
import itertools
import numpy as np
import polar_diagrams
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

from dash import dcc, html, Input, Output, callback, State, Patch
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go


_INT_CHART_WIDTH = 1400
_INT_CHART_HEIGHT = 500
_STR_COLOR_SELECTION_GREY = '#D3D3D3'
_STR_COLOR_BACKGROUND_GREY = '#FBFBFB'
_DICT_FIGURE_SAVE_CONFIG = {
    'format': 'png',  # one of png, svg, jpeg, webp
    'filename': 'polar_diagram',
    # 'height': 500,
    # 'width': 700,
    'scale': 6  # Multiply title/legend/axis/canvas sizes by this factor
}
_DICT_MI_PARAMETERS = dict(
    string_entropy_method='auto',
    int_mi_n_neighbors=3,
    bool_discrete_reference_model=True,
    discrete_models=True,
    int_random_state=42)
_FLOAT_MAX_R = 0.0
_FLOAT_MAX_THETA = 0.0
_DICT_CLUSTER_MODEL = {}
_LIST_MODEL_NAMES = []
_STRING_REFERENCE_MODEL = 'Ground_Truth'
_STRING_DIAGRAM_TYPE = 'taylor'
_STRING_MID_TYPE = 'normalized'


def _grid_search(df_left_input, string_reference_model, list_measures):

    # We save the row with the reference model
    df_reference_row = df_left_input.loc[
        df_left_input['Model'] == string_reference_model]
    # We remove the reference row from the dataframe
    df_input_no_reference = df_left_input.drop(
        df_reference_row.index)[list_measures]

    list_min_samples = np.arange(2, 15, step=2)
    # TODO: Improve choosing epsilon depending on the data
    list_epsilons = np.linspace(0.01, 10, num=50)
    list_hyperparam = list(itertools.product(list_epsilons, list_min_samples))

    list_scores = []
    list_labels_over_runs = []

    for i, (float_eps, int_min_samples) in enumerate(list_hyperparam):
        constructor_DBSCAN = DBSCAN(
            eps=float_eps, min_samples=int_min_samples, n_jobs=-1)
        constructor_DBSCAN.fit_predict(df_input_no_reference)
        list_labels = constructor_DBSCAN.labels_
        # We check if we have all outliers or all elements in seperate clusters
        # These are the edge cases which we do not want
        if len(set(list_labels)) == 1 or (
                len(set(list_labels)) == len(list_labels)):
            continue

        list_scores.append(
            silhouette_score(df_input_no_reference, list_labels))
        list_labels_over_runs.append(list_labels)

    int_best_score_index = np.argmax(list_scores)
    np_array_best_labels = list(list_labels_over_runs[int_best_score_index])
    # We add the label for the reference model at the same place that model
    # was before we removed the entire row it was contained in
    # We add a value of df_input.shape[0] because the model must not be a part
    # of any cluster
    np_array_best_labels.insert(
        df_reference_row.index.values[0], df_left_input.shape[0])

    tuple_best_hyperparam = list_hyperparam[int_best_score_index]

    return tuple_best_hyperparam, np_array_best_labels


def _tuple_group_left_dataframe(df_left_input, string_reference_model):
    dict_aggregate_rules = {'Model': '; '.join}
    for i in df_left_input.columns.to_list():
        if i not in ['Model', 'Label']:
            dict_aggregate_rules[i] = 'mean'

    df_grouped_rows = df_left_input.groupby(
        'Label', as_index=False, sort=False).agg(
        dict_aggregate_rules).reset_index(drop=True)
    df_grouped_rows['Cluster Count'] = [
        int_i.count('; ') + 1 for int_i in list(df_grouped_rows['Model'])]

    dict_model_cluster_correspondence = {}
    list_new_model_names = []
    for int_i, str_model in enumerate(df_grouped_rows['Model'].to_list()):

        # The code below names only Clusters those traces that have multiple
        # model names. If there is only one model name, then it is left as is
        # and not named 'Cluster number'
        # if '; ' in str_model:
        #    list_new_model_names.append('Cluster ' + str(int_i + 1))
        # else:
        #    list_new_model_names.append(str_model)

        # The code below names only Clusters those traces that are different
        # than the reference model
        if string_reference_model == str_model:
            list_new_model_names.append(str_model)
        else:
            list_new_model_names.append('Cluster ' + str(int_i + 1))

        for str_one_model in str_model.split('; '):
            if str_one_model == string_reference_model:
                dict_model_cluster_correspondence[
                    str_one_model] = string_reference_model
            else:
                dict_model_cluster_correspondence[
                    str_one_model] = 'Cluster ' + str(int_i + 1)

    df_grouped_rows['Model'] = list_new_model_names

    return df_grouped_rows, dict_model_cluster_correspondence


def _chart_create_left_chart(df_grouped_data, string_reference_model,
                             string_diagram_type, string_mid_type,
                             string_relevant_measure):

    chart_left = polar_diagrams.polar_diagrams._chart_create_diagram(
        [df_grouped_data],
        string_reference_model=string_reference_model,
        string_diagram_type=string_diagram_type,
        string_mid_type=string_mid_type,
        bool_normalized_measures=False)

    int_max_cluster = df_grouped_data['Cluster Count'].max()
    dict_left = chart_left.to_dict()
    for int_i in range(len(dict_left['data'])):
        dict_left['data'][int_i]['showlegend'] = False

        if dict_left['data'][int_i]['name'].split(
                '. ')[1] == string_reference_model:
            continue

        dict_left['data'][int_i]['mode'] = 'markers+text'
        dict_left['data'][int_i]['text'] = '<b>' + str(
            df_grouped_data['Model'][int_i]).split(' ')[1] + '</b>'
        dict_left['data'][int_i]['marker']['color'] = 'rgba(100,100,100,0)'
        dict_left['data'][int_i]['marker']['line']['color'] = [
            df_grouped_data[string_relevant_measure][int_i]]
        dict_left['data'][int_i]['marker']['size'] = [df_grouped_data[
            'Cluster Count'][int_i]]
        dict_left['data'][int_i]['marker']['sizemin'] = 1
        dict_left['data'][int_i]['marker']['sizemode'] = 'area'
        # https://stackoverflow.com/questions/57417164/is-there-a-way-to-calculate-optimal-sizeref-value-for-plotly-scatter3d  # noqa
        dict_left['data'][int_i]['marker']['sizeref'] = int_max_cluster / 30**2

    chart_left = go.Figure(dict_left).update_traces(
        marker_coloraxis='coloraxis',
        marker_line_coloraxis='coloraxis',
        marker_line_reversescale=True,)

    float_cmin = df_grouped_data[
        df_grouped_data['Model'] != string_reference_model][
        string_relevant_measure].min()
    float_cmax = df_grouped_data[
        df_grouped_data['Model'] != string_reference_model][
        string_relevant_measure].max() * 1.15

    chart_left.update_layout(
        coloraxis={'colorscale': 'gray', 'showscale': False,
                   'cmin': float_cmin, 'cmax': float_cmax},
        dragmode='zoom', clickmode='event+select', hovermode=False)

    list_legend_ticks = list(df_grouped_data['Cluster Count'].unique())

    chart_left_size_legend = go.Figure(go.Scatter(
        x=df_grouped_data['Cluster Count'], y=[1]*df_grouped_data.shape[0],
        showlegend=False,
        marker={'size': df_grouped_data['Cluster Count'], 'sizemode': 'area',
                'sizeref': df_grouped_data['Cluster Count'].max() / 30**2,
                'color': 'rgba(100,100,100,0)',
                'line': {'color': 'black', 'width': 2}}))
    chart_left_size_legend.update_layout(
        yaxis={'zeroline': False, 'showline': False, 'showticklabels': False,
               'ticks': '', 'showgrid': False},
        xaxis={'zeroline': False, 'tickmode': 'array', 'showgrid': False,
               'tickvals': list_legend_ticks, 'title': 'Cluster size',
               'linecolor': _STR_COLOR_SELECTION_GREY},
        template='simple_white',
        dragmode=False,
        hovermode=False,
        width=round(_INT_CHART_WIDTH/3.6),
        height=110,
        margin={'r': 50, 'l': 130, 't': 0, 'b': 0})

    return chart_left, chart_left_size_legend


def _tuple_create_initial_left_diagram(df_input, string_reference_model,
                                       string_diagram_type, string_mid_type):
    # Here we create a DataFrame for the left chart with the clustered models
    # First we check if this is a list
    if isinstance(df_input, list):
        # If so, we then check if we have a second version or scalar data set
        if len(df_input) != 2:
            raise ValueError('The list of data sets contains only 1 data set' +
                             ' instead of 2.')
        else:
            if df_input[1].shape[0] == 1:
                df_new_input = df_input[0].copy()
            else:
                raise ValueError('The dashboard does not support two version' +
                                 ' data set functionality yet.')
                # If we have two versions, we merge them vertically to create
                # clusters of combined data
                # df_new_input = pd.concat(df_input, ignore_index=True, axis=0)
    else:
        df_new_input = df_input

    if string_diagram_type == 'taylor':
        df_left_input = polar_diagrams.df_calculate_td_properties(
            df_new_input, string_reference_model)
        list_relevant_measures = ['Standard Deviation', 'Correlation', 'CRMSE']
    else:
        df_left_input = polar_diagrams.df_calculate_mid_properties(
            df_new_input, string_reference_model,
            dict_mi_parameters=_DICT_MI_PARAMETERS)
        if string_mid_type == 'scaled':
            list_relevant_measures = ['Entropy', 'Scaled MI', 'VI']
        else:
            list_relevant_measures = ['Root Entropy', 'Normalized MI', 'RVI']

    tuple_hyperparam, np_array_labels = _grid_search(
        df_left_input,
        string_reference_model=string_reference_model,
        list_measures=list_relevant_measures)
    df_left_input['Label'] = np_array_labels

    df_left_grouped, dict_model_cluster = _tuple_group_left_dataframe(
        df_left_input, string_reference_model)

    chart_left, chart_left_size_legend = _chart_create_left_chart(
        df_left_grouped, string_reference_model, string_diagram_type,
        string_mid_type, list_relevant_measures[-1])

    return chart_left, chart_left_size_legend, dict_model_cluster


def _tuple_create_initial_right_diagram(df_input, string_reference_model,
                                        string_diagram_type, string_mid_type):

    list_warning_caught = None
    # We monkey patch the function that prints the warnings so that it doesn't
    # require some inputs and only returns the warning message that we need
    warnings.formatwarning = lambda msg, *args, **kwargs: str(msg)

    if string_diagram_type == 'mid':
        with warnings.catch_warnings(record=True) as warning_tmp:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("default")
            chart_right = polar_diagrams.chart_create_mi_diagram(
                df_input, string_reference_model=string_reference_model,
                string_mid_type=string_mid_type,
                dict_mi_parameters=_DICT_MI_PARAMETERS).update_layout(
                dragmode='select', clickmode='event+select',
                width=int(_INT_CHART_WIDTH*0.9),
                height=_INT_CHART_HEIGHT*1.3,
                margin={'l': 0, 'r': 0})

            list_warning_caught = warning_tmp
    else:
        with warnings.catch_warnings(record=True) as warning_tmp:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("default")
            chart_right = polar_diagrams.chart_create_taylor_diagram(
                df_input,
                string_reference_model=string_reference_model).update_layout(
                dragmode='select', clickmode='event+select',
                width=int(_INT_CHART_WIDTH*0.9),
                height=_INT_CHART_HEIGHT*1.3,
                margin={'l': 0, 'r': 0})

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

    # ====================================================================
    # This is done only for the sake of showing at least one diagram with
    # both quadrants
    if string_diagram_type == 'mid' and string_mid_type == 'scaled':
        chart_right.update_layout(polar_sector=[0, 180])
    # ====================================================================

    return chart_right, list_warnings


def _tuple_style_both_diagrams(chart_left, chart_right, dict_model_cluster):
    # We use the same radial and angular axis range for both diagrams. This
    # fixes the edge cases where we have different axis ranges because of the
    # left overview diagram. This diagram can have for example the angular axis
    # 0-90 and not 0-180 as the right diagram because of the aggregation of
    # some models during clustering (thus aggregating their coordinates)
    global _FLOAT_MAX_THETA
    _FLOAT_MAX_THETA = chart_right['layout']['polar']['sector'][1]

    chart_left.update_layout(
        title=None,
        polar_radialaxis_range=chart_right[
            'layout']['polar']["radialaxis"]["range"],
        polar_radialaxis_ticklen=0,
        polar_radialaxis_showticklabels=False,
        polar_radialaxis_linewidth=0.5,
        polar_radialaxis_layer='below traces',
        polar_radialaxis_autorange=False,
        polar_radialaxis_rangemode='normal',
        polar_radialaxis_title=None,
        polar_angularaxis=chart_right['layout']['polar']["angularaxis"],
        polar_angularaxis_layer='below traces',
        polar_angularaxis_ticklen=0,
        polar_angularaxis_showticklabels=False,
        polar_angularaxis_linewidth=0.5,
        polar_angularaxis_showgrid=False,
        polar_sector=[0, _FLOAT_MAX_THETA])

    # We disable a legend for the second diagram by traversing traces
    dict_right = chart_right.to_dict()
    for int_i in range(len(dict_right['data'])):
        str_model_name = dict_right['data'][int_i]['name'].split('. ')[1]
        dict_right['data'][int_i]['legendgroup'] = dict_model_cluster[
            str_model_name]
        if str_model_name != dict_model_cluster[str_model_name]:
            dict_right['data'][int_i][
                'legendgrouptitle_text'] = dict_model_cluster[str_model_name]

    chart_right = go.Figure(dict_right)
    chart_right.update_layout(legend_tracegroupgap=20,
                              legend_title='<b>Data Points</b><br>',
                              legend_title_font_size=14,
                              legend_groupclick="toggleitem",
                              legend_xref='container',
                              legend_yref='container',
                              legend_xanchor='left',
                              legend_yanchor='top',
                              legend_orientation='v',
                              legend_y=0.9)

    float_width_division = 3.2 if _FLOAT_MAX_THETA == 180.0 else 3.6
    float_height_subtraction = 230 if _FLOAT_MAX_THETA == 180.0 else 240
    dict_margin = {'l': 0, 'r': 0, 't': 0,
                   'b': 0} if _FLOAT_MAX_THETA == 180.0 else {'t': 10, 'b': 20,
                                                              'r': 0}
    chart_left.update_layout(
        width=round(_INT_CHART_WIDTH / float_width_division),
        height=_INT_CHART_HEIGHT - float_height_subtraction,
        margin=dict_margin)

    return chart_left, chart_right


def _tuple_create_both_diagrams(df_input, string_reference_model,
                                string_diagram_type='taylor',
                                string_mid_type='normalized'):

    list_valid_diagram_types = ['taylor', 'mid']
    list_valid_mid_types = ['scaled', 'normalized']

    if string_diagram_type not in list_valid_diagram_types:
        raise ValueError('string_diagram_type not in ' +
                         str(list_valid_diagram_types))

    if string_diagram_type == 'mid' and (
            string_mid_type not in list_valid_mid_types):
        raise ValueError('string_mid_type not in ' +
                         str(list_valid_mid_types))

    (chart_left, chart_left_size_legend,
     dict_model_cluster) = _tuple_create_initial_left_diagram(
        df_input, string_reference_model, string_diagram_type, string_mid_type)

    chart_right, list_warnings = _tuple_create_initial_right_diagram(
        df_input, string_reference_model, string_diagram_type, string_mid_type)

    chart_left, chart_right = _tuple_style_both_diagrams(
        chart_left, chart_right, dict_model_cluster)

    global _FLOAT_MAX_R
    global _FLOAT_MAX_THETA
    global _DICT_CLUSTER_MODEL
    global _LIST_MODEL_NAMES
    _FLOAT_MAX_R = chart_left['layout']['polar']['radialaxis']['range'][1]

    _DICT_CLUSTER_MODEL = {}
    for string_model in dict_model_cluster:
        string_cluster = dict_model_cluster[string_model]
        if string_cluster not in _DICT_CLUSTER_MODEL:
            _DICT_CLUSTER_MODEL[string_cluster] = [string_model]
        else:
            _DICT_CLUSTER_MODEL[string_cluster].append(string_model)

    _LIST_MODEL_NAMES = [dict_one_trace['name'].split('. ')[1]
                         for dict_one_trace in chart_right['data']]

    # ====================================================================
    # This is done only for the sake of showing at least one diagram with
    # both quadrants
    if string_diagram_type == 'mid' and string_mid_type == 'scaled':
        chart_left.update_layout(polar_sector=[0, 180])
        chart_right.update_layout(polar_sector=[0, 180])
    # ====================================================================

    return chart_left, chart_left_size_legend, chart_right, list_warnings


def _layout_return(bool_with_scalar):
    global _DF_INPUT
    if bool_with_scalar:
        _DF_INPUT = [
            pd.read_csv(os.path.join('..', 'data', 'Case_Study_Ecoli',
                                     'ecoli_evaluation.csv')),
            pd.read_csv(os.path.join('..', 'data', 'Case_Study_Ecoli',
                                     'ecoli_time_evaluation.csv'))
            ]
    else:
        _DF_INPUT = pd.read_csv(
            os.path.join('..', 'data', 'Case_Study_Ecoli',
                         'ecoli_evaluation.csv'))

    (chart_left, chart_left_size_legend, chart_right,
     list_warnings) = _tuple_create_both_diagrams(
         _DF_INPUT, _STRING_REFERENCE_MODEL, _STRING_DIAGRAM_TYPE,
         _STRING_MID_TYPE)

    layout = [
        dbc.Col([
            html.Div(
                html.H3("Overview"),
                style={"font-family": 'open sans',
                       'text-align': 'center', 'margin-bottom': 40,
                       'margin-top': 80}),
            dcc.Graph(
                id="chart-left",
                figure=chart_left,
                config={
                    'toImageButtonOptions': _DICT_FIGURE_SAVE_CONFIG,
                    'modeBarButtonsToRemove': [
                        'zoom', 'select', 'pan', 'lasso', 'zoomIn',
                        'zoomOut', 'autoScale', 'resetScale'],
                    'staticPlot': False,
                    'displaylogo': False,
                    'showAxisDragHandles': False}
            ),
            dcc.Graph(
                id="chart-left-legend",
                figure=chart_left_size_legend,
                config={
                    'toImageButtonOptions': _DICT_FIGURE_SAVE_CONFIG,
                    'modeBarButtonsToRemove': [
                        'zoom', 'pan', 'lasso', 'zoomIn', 'zoomOut', 'select',
                        'autoScale', 'resetScale'],
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
                    style={'margin-top': 30}))],
            width=3,
            align='start',
            style={'margin-left': 0, 'margin-right': 0}),
        dbc.Col([
            html.Div(
                html.H3("Detail"),
                style={"font-family": 'open sans',
                       'text-align': 'center', 'margin-bottom': 40,
                       'margin-top': 80}),
            dcc.Graph(
                id="chart-right",
                figure=chart_right,
                config={
                    'toImageButtonOptions': _DICT_FIGURE_SAVE_CONFIG,
                    'modeBarButtonsToRemove': [
                        'zoom', 'pan', 'lasso', 'zoomIn', 'zoomOut', 'select',
                        'autoScale', 'resetScale'],
                    'displaylogo': False,
                    'showAxisDragHandles': False})],
                width=True,
                align='start')
        ]

    return layout


@callback(
    Output(component_id="chart-left", component_property="figure",
           allow_duplicate=True),
    Output(component_id="chart-left-legend", component_property="figure",
           allow_duplicate=True),
    Output(component_id="chart-right", component_property="figure",
           allow_duplicate=True),
    Output('alert-warnings', 'children'),
    Output('alert-warnings', 'is_open'),
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

    (chart_left, chart_left_size_legend, chart_right,
     list_warnings) = _tuple_create_both_diagrams(
        _DF_INPUT, _STRING_REFERENCE_MODEL,
        string_diagram_type, string_mid_type)

    bool_is_open = True if list_warnings else False

    return (chart_left, chart_left_size_legend, chart_right, list_warnings,
            bool_is_open)


@callback(
    Output(component_id="chart-left", component_property="figure",
           allow_duplicate=True),
    Output(component_id="chart-right", component_property="figure",
           allow_duplicate=True),
    Input(component_id="chart-left", component_property="relayoutData"),
    State('chart-left', 'figure'),
    State('chart-right', 'figure'),
    prevent_initial_call=True
)
def _list_update_zooms(dict_selected_range, dict_left, dict_right):

    chart_left_updated = Patch()
    chart_right_updated = Patch()

    if dict_selected_range and (
            'polar.radialaxis.range' in dict_selected_range):

        dict_radial_range = dict_selected_range['polar.radialaxis.range']

        for int_i, trace in enumerate(dict_left['data']):
            if 'name' in trace and trace['name'] == 'Selection':
                del chart_left_updated['data'][int_i]

        # Here we check if double click was not detected. If it was detected
        # we just had to remove the Selection trace, which we did above.
        # If it was not detected, that means we have to create a new Selection
        # {  'polar.angularaxis.rotation': 0,
        #    'polar.radialaxis.angle': 0,
        #    'polar.radialaxis.range': [0, 16.353330541878254]
        # }
        if 'polar.angularaxis.rotation' not in dict_selected_range and (
                'polar.radialaxis.angle' not in dict_selected_range):

            # We create a circular rectangle of 60 points by creating them and
            # connecting them with a line
            np_alpha = np.linspace(0, _FLOAT_MAX_THETA, 60).tolist()
            np_selection_theta = np_alpha + np_alpha[::-1] + [np_alpha[0]]

            chart_left_updated['data'].append(
                go.Scatterpolar(r=[dict_radial_range[0]]*60 +
                                  [dict_radial_range[1]]*60 +
                                  [dict_radial_range[0]],
                                theta=np_selection_theta,
                                name='Selection',
                                fill='toself',
                                mode='lines',
                                showlegend=False,
                                line=dict(
                                    color=_STR_COLOR_SELECTION_GREY,
                                    dash='dot',
                                    width=2)))
            # We also update the color
            chart_right_updated['layout']['polar']["radialaxis"][
                "linecolor"] = _STR_COLOR_SELECTION_GREY
            chart_right_updated['layout']['polar']["radialaxis"][
                "linewidth"] = 4
            chart_right_updated['layout']['polar']["angularaxis"][
                "linecolor"] = _STR_COLOR_SELECTION_GREY
            chart_right_updated['layout']['polar']["angularaxis"][
                "linewidth"] = 4
            chart_right_updated['layout']['polar'][
                "bgcolor"] = _STR_COLOR_BACKGROUND_GREY

            # We update the right chart radial boundaries with the selection
            chart_right_updated['layout']['polar']["radialaxis"][
                "range"] = [dict_radial_range[0], dict_radial_range[1]]

            # We update the legend with the selected points
            for int_i, dict_one_trace in enumerate(dict_right['data']):
                if dict_radial_range[0] <= dict_one_trace['r'][0] <=\
                        dict_radial_range[1]:
                    chart_right_updated['data'][int_i]['visible'] = True
                else:
                    chart_right_updated['data'][int_i][
                        'visible'] = 'legendonly'

        else:
            # We reset the color to black on doubleclick
            chart_right_updated['layout']['polar']["radialaxis"][
                "linecolor"] = 'black'
            chart_right_updated['layout']['polar']["radialaxis"][
                "linewidth"] = 1
            chart_right_updated['layout']['polar']["angularaxis"][
                "linecolor"] = 'black'
            chart_right_updated['layout']['polar']["angularaxis"][
                "linewidth"] = 1
            chart_right_updated['layout']['polar'][
                "bgcolor"] = '#fff'

            # We reset the radial axis boundaries of the right chart
            chart_right_updated['layout']['polar']["radialaxis"][
                "range"] = [dict_radial_range[0], _FLOAT_MAX_R]

            # We also reset the legend trace visibility
            for int_i, dict_one_trace in enumerate(dict_right['data']):
                chart_right_updated['data'][int_i]['visible'] = True

        chart_left_updated['layout']['polar']["radialaxis"][
            "autorange"] = False
        chart_left_updated['layout']['polar']["radialaxis"][
            'rangemode'] = 'normal'
        chart_right_updated['layout']['polar']["radialaxis"][
            "autorange"] = False
        chart_right_updated['layout']['polar']["radialaxis"][
            'rangemode'] = 'normal'
        chart_left_updated['layout']['polar']["radialaxis"][
            "range"] = [0, _FLOAT_MAX_R]

    else:
        raise PreventUpdate

    return chart_left_updated, chart_right_updated
