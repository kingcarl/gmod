gmod
====

Global Monitor on DNS

# Global Monitor on DNS

## ����
gmod ��һ�������� Linux ƽ̨��DNSȫ����ع��ߣ��˹�����Ҫ����ȫ��IDC��Դ����ȫ�����ڵ�ͳһ����gserver������gclientͳһ�·����ָ�

## ���ٿ�ʼ
����Դ�룺

    git clone https://github.com/kingcarl/gmod/gmod.git
    cd gmod
    
��װ��

	tar zxvf pydns-2.3.6.tar.gz
    cd ./server && python setup.py install 
    
python֧�֣�

		python2.3����
		
����

    Client:
		python gclient [port]

	Server:
		python gserver [port]
