CentOS上安装所需依赖包：

yum -y install flex byacc  libpcap ncurses ncurses-devel libpcap-devel

Debian上安装所需依赖包：

apt-get install -r flex byacc libncurses5-dev libpcap-dev libpcap0.8 libncurses5 build-essential

下载iftop

cd /usr/local/

wget http://www.ex-parrot.com/pdw/iftop/download/iftop-1.0pre4.tar.gz

tar zxvf iftop-1.0pre4.tar.gz

cd iftop-1.0pre4

./configure --prefix=/usr/local/iftop

make && make install


运行：/usr/local/iftop/sbin/iftop -i eth1 -N -n -B -P -m 25M


界面上面显示的是类似刻度尺的刻度范围，为显示流量图形的长条作标尺用的。

中间的“<=” “=>”这两个左右箭头，表示的是流量的方向。 

TX：发送流量 

RX：接收流量 

TOTAL：总流量 

Cumm：运行iftop到目前时间的总流量 

peak：流量峰值 

rates：分别表示过去 2s 10s 40s 的平均流量

一些常见问题

1、make: yacc: Command not found 

make: *** [grammar.c] Error 127 

解决方法：apt-get install byacc   /   yum install byacc 

2、configure: error: Curses! Foiled again! 

(Can’t find a curses library supporting mvchgat.) 

Consider installing ncurses. 

解决方法：apt-get install libncurses5-dev  /    yum  install ncurses-devel
