# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_portf_perf(uid):

    descr_box = ''


    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs_s:
            symbol = row[0]


        descr_box = '' +\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        '                   <div><h5>XXXX Portfolio 1-Year Performance</h5></div>'+\
        '                   <script>'+\
        '                       google.charts.load("current", {"packages":["corechart"]});'+\
        '                        google.charts.setOnLoadCallback(drawChart);'+\
        '                        function drawChart() {'+\
        '                         var data = google.visualization.arrayToDataTable(['+\
        '                            ["Year", "Sales"],'+\
        '                            ["2013",  1000],'+\
        '                          ]);'+\
        '                          var options = {'+\
        '                            legend: "none",'+\
        '                            vAxis: {minValue: 0},'+\
        '                            series:{0: {areaOpacity: 0.1, color: "black", lineWidth: 1} }'+\
        '                          };'+\
        '                          var chart = new google.visualization.AreaChart(document.getElementById("portf_perf_chart"));'+\
        '                          chart.draw(data, options);'+\
        '                        }'+\
        '                   </script>'+\
        '               <div id="portf_perf_chart"></div>'+\
        '            </div>'+\
        '        </div>'


        cr.close()
        connection.close()


    except Exception as e: print(e)

    return descr_box
