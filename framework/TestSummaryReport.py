# -*- coding: utf-8 -*-
# @Time    : 公元19-02-27 上午11:13
# @Author  : 张廷利
# @Site    : 
# @File    : TestSummaryReport.py
# @Software: IntelliJ IDEA

import os,pytest


from common.tools.XmlTools import XmlTools
from common.tools.CommUtils import CommUtils

class TestSummaryReport(object):

    def analysis_result(self):
        path = os.path.abspath('..')
        report_path = path + '/report'
        print(report_path)
        results = XmlTools().get_dom_for_fristxml(report_path)
        fail_count = 0
        skip_count = 0
        success_count=0
        duration=0
        report ={}
        for key,value in results.items():
            if key =='passed':
                success_count = value
            elif key =='failed':
                fail_count = value
            elif key =='skiped':
                skip_count =value
            elif key =='duration':
                duration = value
            else:
                fail_count = fail_count + value

        total_count = fail_count + skip_count+success_count
        report['success_count'] = success_count
        report['fail_count'] = fail_count
        report['skip_count'] = skip_count
        report['durations'] = duration
        report['case_count'] = total_count
        reporthtml = self.gengerate_summary_report(report)
        writefile = "{0}/allure-report/summary-report.html".format(path);
        CommUtils().write_file(writefile,reporthtml)


    def gengerate_summary_report(self,report):
        reporthtml =''
        reporthtml = reporthtml + '''<!DOCTYPE html>
                    <html lang="en">
                    <body>
                    <p>
                        &nbsp;
                        &nbsp;
                        &nbsp;
                        &nbsp;
                        &nbsp;
                    </p>
                    <table width="90%" bordercolor="#000000" align="center" border="1px" cellpadding="5px" cellspacing="0px"
                           style="border-collapse:collapse">
                           <tr align="center">
                               <th colspan="6"> Summary Report </th>
                           </tr>
                           <tr bgcolor="#add8e6">
                             <th>case_count</th>
                              <th >success</th>
                              <th>fail</th>
                              <th>skip</th>
                              <th>success rate</th>
                              <th>durations(ms)</th>
                          </tr>
                          <tr>
                             <td width="15%" >{case_count}</td>
                              <td width="15%" bgcolor='#00600' >{success_count}</td>
                              <td width="15%" bgcolor="red" >{fail_count}</td>
                              <td width="15%" bgcolor="yellow">{skip_count}</td>
                              <td width="15%">{percent}</td>
                              <td width="15%">{durations}</td>
    
                          </tr>
                    </table>
                    </body>
                    </html>'''
        reporthtml = reporthtml.format(case_count=report['case_count'],
                                       success_count=report['success_count'],
                                       fail_count=report['fail_count'],
                                       skip_count=report['skip_count'],
                                       percent=round(report['success_count']/report['case_count'] * 100,2),
                                       durations=report['durations'])
        return reporthtml



    def test_report_generate(self):
        #project_name =  pytest.config.getoption('--project_system_name')
        self.analysis_result()


if __name__ =="__main__":
    pytest.main(" TestSummaryReport.py --capture=no --project_system_name=framework-test")
