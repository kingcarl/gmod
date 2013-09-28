gmod
====

Global Monitor on DNS

# Global Monitor on DNS

## 关于
gmod 是一个运行在 Linux 平台的DNS全国监控工具，此工具需要具有全国IDC资源，在全国各节点统一部署gserver，并又gclient统一下发监控指令。

## 快速开始
下载源码：

    git clone https://github.com/kingcarl/gmod/gmod.git
    cd gmod
    
安装：

	tar zxvf pydns-2.3.6.tar.gz
    cd ./server && python setup.py install 
    
python支持：

		python2.3以上
		
运行

    Client:
		python gclient [port]

	Server:
		python gserver [port]
