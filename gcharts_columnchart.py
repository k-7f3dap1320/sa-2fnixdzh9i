# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_cookie import *
from sa_func import *

def get_gcharts_column(chart_id,data,data_label,data_color,data_annotation,title,legend_position,width,height):
    r = ''
    maxval = 0
    minval = 0
    try:
        maxval = max(data)
        minval = min(data)

        r = ' '+\
        '<script type="text/javascript">'+\
        '    google.charts.load("current", {packages:["corechart"]});'+\
        '    google.charts.setOnLoadCallback(drawChart);'+\
        '    function drawChart() {'+\
        '      var data = google.visualization.arrayToDataTable(['+\
        '        ["label", "", { role: "style" }, {role: "annotation"} ],'+\
        get_gcharts_column_data(data,data_label,data_color,data_annotation) +\
        '      ]);'+\
        '      var view = new google.visualization.DataView(data);'+\
        '      var options = {'+\
        '        title: "'+ str(title) +'",'+\
        '        titleTextStyle: {color:"'+ theme_return_this('black','white') +'"},'+\
        '        backgroundColor: "transparent",'+\
        '        bar: {groupWidth: "90%"},'+\
        '        legend: { position: "'+ str(legend_position) +'" },'+\
        '        vAxis: {'+\
        '           gridlines: {color: "transparent"},'+\
        '           textStyle: {color: "'+ theme_return_this('black','white') +'"},'+\
        '           viewWindow:{min:'+ str(minval) +',max:'+ str(maxval) +'},' +\
        '        },'+\
        '        hAxis: {'+\
        '           gridlines: {color: "transparent"},'+\
        '           textStyle: {color: "'+ theme_return_this('black','white') +'"},'+\
        '        }'+\
        '      };'+\
        '      var chart = new google.visualization.ColumnChart(document.getElementById("'+ str(chart_id) +'"));'+\
        '      chart.draw(view, options);'+\
        '  }'+\
        '</script>'+\
        '<div id="'+ str(chart_id) +'" style="width: '+ str(width) +'; height: '+ str(height) +';"></div>'

        print(r)

    except Exception as e: print(e)
    return r

def get_gcharts_column_data(data,data_label,data_color,data_annotation):
    r = ''
    try:
        j = len(data)-1
        i = 0
        while i <= j:
            r = r +\
            '["'+ str(data_label[i]) +'", '+ str(data[i]) +', "'+ str(data_color[i]) +'", "'+ str(data_annotation[i]) +'"],'
            i += 1

    except Exception as e: print(e)
    return r
