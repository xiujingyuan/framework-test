cd /data/www/wwwroot
git clone https://jc_mock:1LqUuzYMJXUS_io7Ab9q@git.kuainiujinke.com/cd-test/auto-test.git
git clone https://jc_mock:1LqUuzYMJXUS_io7Ab9q@git.kuainiujinke.com/cd-test/framework-test.git
git clone https://jc_mock:1LqUuzYMJXUS_io7Ab9q@git.kuainiujinke.com/jc_test/jc-mock.git
cd
cp /data/www/wwwroot/auto-test/deploy.sh /data/www/deploy.sh
cd /data/www
sleep 2
sh deploy.sh