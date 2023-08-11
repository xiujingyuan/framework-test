# 项目详情

##一、项目结构

**1.bussiness**
##### 存放各个业务类

**2.common**
#### 存放公共方法，基础类

**3.config**
##### 存放当前使用的环境配置文件

**4.environments**
##### 存放各个环境下对应的配置环境文件

**5.framework**
##### 存放框架主要类及相关方法

**6.initial**
##### 存放初始化方法，如初始化数据库连接，配置文件,日志文件

**7.logs**
##### 存放生成的日志文件

**8.models**
##### 存放所有数据库表model，包括框架的和业务方的

**9.render**
##### 存放一些特殊的需要修改的第三库

##二、依赖包安装

**1.SQLAlchemy**
##### 正常安装，因为mysqldb不支持python3版本，安装好后
##### 需要修改文件[site-packages/sqlalchemy/dialects/mysql
##### /.__init__.py]，添加下面的代码到import mysqldb之前

<code>
import pymysql

pymysql.install_as_MySQLdb()

</code>

 **2.Elixir**
 ##### 由于Elixir不支持python3，我将适合python3的版本放在了render下面
 ##### 先用pip命令正常安装，然后再替换site-packages下面的内容
 
 ##三、本地运行demo
 ##### 环境是Pycharm（其它的环境应该是类似的）
 ##### 1、点击菜单Run，选择下面的Edit Configurations
 ##### 2、选择左上角的【+】选择Python tests下面的pytest,输入名字即可
 ##### 3、在下面填入对应的参数,如下
 <code>
 --project_system_name=tmms_1 --system_module=push_user_api -s --ip=127.0.0.1 --port=3317 --user=cdbiz --pwd=llqK2OpTjIEV2QUJ --database=gaea_framework --alluredir report
 </code>
 
 ##### 4、点击Run，选择刚添加的那个配置，运行即可
 
 ##四、本地单独运行allure
 
 **1.本地安装**
 ##### 由于直接安装历来的lxml库会由于编译文件的缺失报错，需要先使用lxml的whl包先安装
 ##### 文件在render/lxml，使用pip命令安装即可；然后再使用pip命令安装allure即可
 
 **2.配置环境变量**
 ##### mac下面添加allure的bin目录下面的文件地址，如下
 
 <code>
 # Setting PATH for allure
 PATH="/Users/snow/Documents/allure-2.7.0/bin/:${PATH}"
 
 </code>
 
 **3.本地运行**
 ##### 本地有pytest跑出的xml报告
 ##### allure serve  xml报告地址
 ##### allure generate framework/report/ -o framework/report/html
 
 
 
  **4.报告中文问题**
  #####  allure运行完成后有中文显示为unicdoe编码而无法认识，需要将以下文件对应的
  #####  的内容修改即可:首页是安装pytest-allure-adaptor，找到allure/pytest_plugin.py文件
  #####  ，修改第116行代码从
  <code>
    @pytest.mark.hookwrapper
    def pytest_runtest_protocol(self, item, nextitem):
        try:
            # for common items
            description = item.function.__doc__
        except AttributeError:
            # for doctests that has no `function` attribute
            description = item.reportinfo()[2]
        self.test = TestCase(name='.'.join(mangle_testnames([x.name for x in parent_down_from_module(item)])),
                             description=description,
                             start=now(),
                             attachments=[],
                             labels=labels_of(item),
                             status=None,
                             steps=[],
                             id=str(uuid.uuid4()))  # for later resolution in AllureAgregatingListener.pytest_sessionfinish
   </code>
   
   ##### 修改为：
   <code>
   @pytest.mark.hookwrapper
    def pytest_runtest_protocol(self, item, nextitem):
        try:
            # for common items
            description = item.function.__doc__
        except AttributeError:
            # for doctests that has no `function` attribute
            description = item.reportinfo()[2]
        name = parent_down_from_module(item)[-1].name
        if "[" in name and name[-1] == "]":
            name_case = name[name.index("[")+1:-1]
            name = name_case.encode('latin-1').decode('unicode_escape')
        self.test = TestCase(name=name,
                             description=description,
                             start=now(),
                             attachments=[],
                             labels=labels_of(item),
                             status=None,
                             steps=[],
                             id=str(uuid.uuid4()))  # for later resolution in AllureAgregatingListener.pytest_sessionfinish
   
   </code>
   
   ##### 即可