# -*- coding: utf-8 -*-
# @Time    : 公元18-11-26 下午3:59
# @Author  : 张廷利
# @Site    :
# @File    : Commutils.py
# @Software: IntelliJ IDEA

import os,platform,time
from common.tools.BaseUtils import BaseUtils
import pytest


class CommUtils(object):



    def get_project_dir(self):
        #当前目录
        system_name = platform.system()
        currentdir = os.path.dirname(os.path.abspath(__file__));
        system_names = ['linux','darwin']
        if system_name.lower() in system_names:
            dirarry =  currentdir.split("/")[:-2]
            dirarry = "/".join(dirarry)
        else:
            dirarry =  currentdir.split("\\")[:-2]
            dirarry = "\\".join(dirarry)
        return dirarry


    def search_file(self,file_name,path =None):
        '''
        按照文件名称在指定目录以及子目录中查找，返回一个数组。隐藏目录不会遍历，以及名称为venv 的目录不会查找
        :param search_name: 被查找的文件名称，string
        :param path:  查找指定的目录，不传时，默认为当前工程目录。 string
        :return: 返回一个数组，包含查找到所有符合条件的文件的全路径。
        '''
        result = []
        if path == None:
            path = self.get_project_dir()
        if BaseUtils.object_is_null(file_name):
            return "查找的文件名称不能为空！"

        def search_file_inner(path,file_name):
            lists = os.listdir(path)
            for fileorfolder in lists:
                if fileorfolder[0] =="." or fileorfolder =="venv":
                    continue
                temp = os.path.join(path ,fileorfolder)
                if os.path.isfile(temp):
                    if temp.endswith(file_name):
                        result.append(temp)
                if os.path.isdir(temp):
                    search_file_inner(temp,file_name)
            return result
        return search_file_inner(path,file_name)



    def search_file_first(self,file_name,path=None):
        '''
        :param file_name:
        :param path:
        :return: 查找到的文件列表中的第一个路径
        '''
        return self.search_file(file_name,path)[0]




    def search_file_withext(self,file_name,path=None):
        '''
        按照文件的后缀名称查找文件，返回的是一个字典类型的数据，key 是文件名称，value 是文件路径
        隐藏目录不会遍历，以及名称为venv 的目录不会查找
        :param search_ext_name: 需要查找的扩展名称，eg :.xml , .py  string
        :param path: 指定查找的目录  string
        :return:  返回一个字典类型数据，不管是在哪个文件夹文件名称不能重复，否则将会被覆盖。
        '''
        resultext = {}
        if path == None:
            path = self.get_project_dir()
        if BaseUtils.object_is_null(file_name):
            return "查找的文件扩展名称不能为空！"

        def search_file_ext_inner(path,file_name):
            lists = os.listdir(path)
            for fileorfolder in lists:
                if fileorfolder[0]=="." or fileorfolder =="venv":
                    continue
                temp = os.path.join(path,fileorfolder)
                if os.path.isfile(temp):
                    extname = os.path.splitext(fileorfolder)[1]
                    if extname == file_name:
                        resultext[fileorfolder] = temp
                if os.path.isdir(temp):
                    search_file_ext_inner(temp,file_name)
            return resultext
        return search_file_ext_inner(path,file_name)



    def search_filewithext_first(self,file_name,path=None):
        '''
        :param file_name:
        :param path:
        :return: 查找到的文件列表中的第一个路径
        '''
        result = self.search_file_withext(file_name,path)
        if len(result) >=1:
            for value in result.values():
                return value
        else:
            return None






    def get_database_config(self):
        '''

        :param env: 数据库配置全名，不包含路径
        :return:
        '''

        env = pytest.config.getoption('--env', default=None)
        if BaseUtils.object_is_notnull(env):
            env = "database_dev.config"
        else:
            env = "database.config"
        path =  self.search_file_first(env)
        all_database = self.read_file(path)
        database_config = BaseUtils.transfer_string_to_dict(all_database)
        return database_config['databases']



    def get_project_mapper(self):
        return self.search_file_withext(".xml")

    @staticmethod
    def wait_exec_time(second):
        if BaseUtils.object_is_null(second):
            return
        time.sleep(second)




    def write_file(self,pathandfile,content):
        '''
        :param pathandfile: 即将写入的路径
        :param content: 即将写入的字符串
        :return: 返回写入的路径
        '''

        if os.path.exists(pathandfile)==False:
            dirname,filename = os.path.split(pathandfile)
            if os.path.exists(dirname)==False:
                os.makedirs(dirname)
            #os.mknod(filename)
        with open(pathandfile,'w') as file:
            file.write(content)
            file.close()
        return pathandfile





    def read_file(self,path):
        if os.path.exists(path)== False:
            return ""
        f = open(path,"r")
        data = BaseUtils.transfer_string_to_dict(f.read())
        f.close()
        return data











    def write_env(self,envstring):
        '''
        在运行时写入env.config
        :param envstring:
        :return:
        '''
        file= self.search_file_first("env.config");
        self.write_file(file,envstring)

    def get_env(self):

        file= self.search_file_first("env.config");
        f = open(file,"r")
        data = BaseUtils.transfer_string_to_dict(f.read())
        f.close()
        return data['env']



    def get_special_database(self,database_name):
        '''
        获取database.config 文件中，指定database 的配置信息
        :param databasename: 数据库名称，就是database.config 文件中的dbserver
        :return: 返回一个config 的具体内容，包括host，port，password，username
        '''
        databases = self.get_database_config()
        db = []
        for database in databases:
            if database["dbserver"].lower() ==  database_name.lower():
                db.append(database)
                return db



