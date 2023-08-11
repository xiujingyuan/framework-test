# -*- coding: utf-8 -*-
# @Time    : 公元18-11-26 下午4:47
# @Author  : 张廷利
# @Site    : 
# @File    : XmlTools.py
# @Software: IntelliJ IDEA
import xml.dom.minidom
import collections
import os

from common.tools.BaseUtils import BaseUtils
from common.tools.CommUtils import CommUtils

class XmlTools(object):

    def __init__(self):
        self.commutils = CommUtils()


    def get_dom_for_fristxml(self,path):
        test_result = {}
        result = self.commutils.search_filewithext_first('.xml',path)
        print(result)
        dom = xml.dom.minidom.parse(result)
        testcases = dom.getElementsByTagName("test-case")
        for case in testcases:
            if case.hasAttribute("status"):
                key = case.getAttribute("status")
                if key not in test_result.keys():
                    test_result[key] = 0
                test_result[key] = test_result[key] +1
            if case.hasAttribute("start") and case.hasAttribute("stop"):
                if 'duration' not in test_result.keys():
                    test_result['duration'] = 0
                test_result['duration'] = test_result['duration'] + (int(case.getAttribute('stop')) - int(case.getAttribute('start')))
        return test_result



    def get_dom(self,mappername):
        '''
        解析xml,返回整个xml dom
        :param mappername: mapper文件名称
        :return:
        '''
        mappers = self.commutils.search_file_withext(".xml")
        mapperxml = mappers[mappername]
        dom = xml.dom.minidom.parse(mapperxml)
        return dom

    def get_special_node(self,mapperxmlname, name):
        '''
        返回该mapper 文件中指定sql节点的内容'
        :param mapperxmlname:  mapper 文件名称
        :param name:sql节点上name 属性的值
        :return: 返回该sql 节点下的所有内容
        '''
        dom = self.get_dom(mapperxmlname)
        sqls = dom.getElementsByTagName("sql")
        for sql in sqls:
            if sql.hasAttribute("name"):
                if sql.getAttribute("name") ==name:
                    return sql


    def get_special_sqlstatement(self,mapperxmlname,name):
        '''
        获取指定node 节点中的sql 语句
        :param mapperxmlname: mapper 文件名称
        :param name: sql节点上name 属性值的值
        :return: 返回该sql 节点上单纯的sql 语句。
        '''
        sqlnode = self.get_special_node(mapperxmlname,name)
        if sqlnode == None:
            return
        return sqlnode.firstChild.wholeText.strip()
    
    
    def get_special_sqlparams(self,mapperxmlname,name):
        '''
        查找指定mapper文件，指定的某个sql 节点的参数列表
        :param mapperxmlname: mapper 文件名称
        :param name: sql节点上name 属性的值
        :return: 返回该sql 节点参数的list
        '''
        paramlist =[]
        sqlnode = self.get_special_node(mapperxmlname,name)
        if sqlnode == None:
            return
        params = sqlnode.getElementsByTagName("param")
        for param in params:
            temp = {}
            if param.hasAttribute("name"):
                temp['name'] = param.getAttribute('name')
            if param.hasAttribute('type'):
                temp['type']=param.getAttribute('type')
            paramlist.append(temp)
    
    
        return paramlist




    def get_complete_sqlentity(self,mapperxmlname,name,inputs=None):
        '''
    
        :param mapperxmlname: 指定的mapper 文件，在创建mapper 文件的时候，千万不要重名，否则会被覆盖，也不会有提示消息
        @TODO 后续可以改进mapper 文件重名时的提示信息。这个跟命名空间没有关系。因为在查找文件的时候，用的文件名称做key
        :param name: mapper 文件中sql 节点的name属性的值
        :param inputs: json 格式的数据，就直接传一个字典类型数据，不要传字符串过来。否则会报参数不匹配
        :return: sqlentity 字典类型数据，sqlentity.database, sqlentity.sql, sqlentity.params
        '''
    
        sqlenity = {}
        #
        temp_params=[]
        #获取指定node
        xmlsql = self.get_special_node(mapperxmlname,name)
        #获取xml 中配置的参数
        params = xmlsql.getElementsByTagName('param')
        #获取指定的sql语句
        sqlStatement = xmlsql.firstChild.wholeText.strip()
        if BaseUtils.object_is_notnull(inputs) and len(inputs) and len(params):
                #and BaseUtils.object_is_notnull(params) \

            #参数与inputs 中的参数替换
            for param in params:
                if param.hasAttribute('name'):
                    paramname = str.strip(param.getAttribute('name'))
                    value = inputs[paramname]
                    if isinstance(value,dict):
                        value = BaseUtils.transfer_dict_to_string(value)
                    temp_params.append(value)
                    replacename = '#{'+paramname+'}'
                    if paramname in inputs:
                        if param.hasAttribute('type'):
                            type = param.getAttribute('type')
                            if type.lower() == 'string':
                                sqlStatement = sqlStatement.replace(replacename," %s ")
                            else:
                                sqlStatement = sqlStatement.replace(replacename," %s ")
            sqlenity['params'] = tuple(temp_params)
            sqlenity['sql'] = sqlStatement
            sqlenity['name'] = name
            if xmlsql.hasAttribute('database'):
                sqlenity['database'] = xmlsql.getAttribute('database')
        elif (len(params) ==0 or params == None) and inputs == None:
            sqlenity['params'] = None
            sqlenity['sql'] = sqlStatement
            sqlenity['name'] = name
            if xmlsql.hasAttribute('database'):
                sqlenity['database'] = xmlsql.getAttribute('database')
        else:
            return "参数为空，或者配置sql 参数为空，或者参数格式不匹配"
        return sqlenity




    def get_actual_sqlentity(self,sqlstring,params,database):
        sqlenity ={}
        if BaseUtils.object_is_notnull(database) and BaseUtils.object_is_notnull(sqlstring):
            if isinstance(params,dict) ==False:
                params = BaseUtils.transfer_string_to_dict(params)
            sql_params = collections.OrderedDict()
            sql_params = params
            sql_params_values = list(sql_params.values())
            temp_values = []
            for values in sql_params_values:
                values = BaseUtils.transfer_dict_to_string(values)
                temp_values.append(values)
            sqlenity['params'] = tuple(temp_values)
            sqlenity['sql'] = sqlstring
            sqlenity['name'] = 'sample'
            sqlenity['database'] = database
        return sqlenity
