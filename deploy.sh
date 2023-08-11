echo "#########################修改系统配置##########################"
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
pip3 install elasticsearch redis
pip3 install numpy_financial==1.0.0

echo "#########################修改supervisor配置##########################"
cd /var/run
touch supervisor.sock
chmod 700 supervisor.sock
pwd
ls -al
sleep 1

echo "#########################拉取代码##########################"
mkdir -p /data/www/wwwroot
cd /data/www/wwwroot
git clone git@git.kuainiujinke.com:cd-test/framework-test.git
git clone git@git.kuainiujinke.com:jc_test/jc-mock.git
sleep 1

echo "#########################修改一些配置##########################"
cp -f /data/www/wwwroot/framework-test/framework.conf /etc/supervisor/conf.d/framework.conf
cp -f /data/www/wwwroot/jc-mock/jc-mock.conf /etc/supervisor/conf.d/jc-mock.conf
cp -f /data/www/wwwroot/jc-mock/environment/k8s/config.py /data/www/wwwroot/jc-mock/app/common/config/config.py
mkdir -p /data/www/wwwroot/framework-test/logs/supervisor
mkdir -p /data/www/wwwroot/framework-test/logs/gunicon
mkdir -p /data/www/wwwroot/jc-mock/logs/supervisor
mkdir -p /data/www/wwwroot/jc-mock/logs/gunicon
mkdir -p /data/www/wwwroot/jc-mock/logs/celery
mkdir -p /data/logs/testing-platform/download/excel
mkdir -p /data/logs/testing-platform/upload
sleep 1

echo "#########################启动web服务##########################"
supervisord -c /etc/supervisor/supervisord.conf
sleep 10
ps -fe


echo "#########################查看日志##########################"
tail -F /data/www/wwwroot/framework-test/logs/framework_test.log

