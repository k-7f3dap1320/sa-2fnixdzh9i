""" Google column chart """
from app_cookie import theme_return_this

def get_gcharts_column(chart_id, data, data_label, data_color,
                       data_annotation, title, legend_position, width, height):
    """ Draw column chart """
    return_data = ''
    maxval = 0
    minval = 0
    maxval = max(data)
    if maxval > 0:
        maxval = maxval + (maxval/10)
    else:
        maxval = 0

    minval = min(data)
    if minval < 0:
        minval = minval + (minval/10)
    else:
        minval = 0

    return_data = ' '+\
    '<script type="text/javascript">'+\
    '    google.charts.load("current", {packages:["corechart"]});'+\
    '    google.charts.setOnLoadCallback(drawChart);'+\
    '    function drawChart() {'+\
    '      var data = google.visualization.arrayToDataTable(['+\
    '        ["label", "", { role: "style" }, {role: "annotation"} ],'+\
    get_gcharts_column_data(data, data_label, data_color, data_annotation) +\
    '      ]);'+\
    '      var view = new google.visualization.DataView(data);'+\
    '      var options = {'+\
    '        title: "'+ str(title) +'",'+\
    '        titleTextStyle: {color:"'+ theme_return_this('black', 'white') +'"},'+\
    '        backgroundColor: "transparent",'+\
    '        bar: {groupWidth: "90%"},'+\
    '        legend: { position: "'+ str(legend_position) +'" },'+\
    '        vAxis: {'+\
    '           gridlines: {color: "transparent"},'+\
    '           textStyle: {color: "'+ theme_return_this('black', 'white') +'"},'+\
    '           viewWindow:{min:'+ str(minval) +',max:'+ str(maxval) +'},' +\
    '        },'+\
    '        hAxis: {'+\
    '           gridlines: {color: "transparent"},'+\
    '           textStyle: {color: "'+ theme_return_this('black', 'white') +'"},'+\
    '        }'+\
    '      };'+\
    '      var chart = new google.visualization.ColumnChart(document.getElementById("'+\
    str(chart_id) +'"));'+\
    '      chart.draw(view, options);'+\
    '  }'+\
    '</script>'+\
    '<div id="'+ str(chart_id) +'" style="width: '+\
    str(width) +'; height: '+ str(height) +';"></div>'
    return return_data

def get_gcharts_column_data(data, data_label, data_color, data_annotation):
    """ Get data for the column chart """
    return_data = ''
    j = len(data)-1
    i = 0
    while i <= j:
        return_data = return_data +\
        '["'+ str(data_label[i]) +'", '+\
        str(data[i]) +', "'+\
        str(data_color[i]) +'", "'+\
        str(data_annotation[i]) +'"],'
        i += 1
    return return_data
