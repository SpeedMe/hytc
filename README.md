CentOS上安装所需依赖包：
yum -y install flex byacc  libpcap ncurses ncurses-devel libpcap-devel

Debian上安装所需依赖包：
apt-get install flex byacc libncurses5-dev libpcap-dev libpcap0.8 libncurses5
下载iftop
cd /usr/local/
wget http://www.ex-parrot.com/pdw/iftop/download/iftop-1.0pre4.tar.gz
tar zxvf iftop-1.0pre4.tar.gz
cd iftop-1.0pre4
./configure --prefix=/usr/local/iftop
make && make install


运行：/usr/local/iftop/sbin/iftop -i eth1 -N -n -B -P -m 25M
