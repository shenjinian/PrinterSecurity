# PrinterSecurity

校内打印机安全相关事项，包括进行扫描排查、提醒处理。本代码为测试性质，请勿用于违法用途，否则后果自负。

## 使用方法

### 系统环境

Python不能是3.8可能。

建议Ubuntu 18.04 LTS，Git Clone本代码到某个目录，进入目录。


### 安装必备软件

```sh
sudo apt install python3-venv python3-pip -y
sudo apt install nmap -y
sudo apt install cups-bsd cups-ipp-utils -y
```

### 建立Python虚拟环境，下载Chrome

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pyppeteer-install
```

### 修改本地配置文件

```sh
cd script
cp local_settings.template.py local_settings.py
touch data/0-CIDRs.txt
vi data/0-CIDRs.txt
```

上传自定义通知信息到 inc-temp-notify-A4.pdf 到script目录

### 运行

进入Git目录

```sh
source .venv/bin/activate
cd script
python 1-TAB补全
```

- 1-find-printer.py，根据data/0-CIDRs.txt （校内网段）发现打印机到data/1-printer-list.txt
- 3-py ，根据data/1-printer-list.txt 获取指纹信息到data目录和data/screenshot
- 9-print-notify.py，打印inc-temp-notify-A4.pdf到用户打印机上

## 参考文献

<https://www.sonicwall.com/support/knowledge-base/which-ports-are-used-by-network-printers/170503664134344/>
<https://en.wikipedia.org/wiki/Internet_Printing_Protocol>
<https://zhuanlan.zhihu.com/p/27420791>
<https://www.xianjichina.com/special/detail_404918.html>
<https://python-forum.io/Thread-Is-there-in-2018-a-python3-library-that-implements-the-Internet-Printing-Protocol>
<http://hacking-printers.net/wiki/index.php/Main_Page>
<https://courses.csail.mit.edu/6.857/2018/project/kritkorn-cattalyy-korrawat-suchanv-Printer.pdf>
<https://www.andreafortuna.org/2018/02/28/some-thought-about-network-printers-security/>
<https://github.com/RUB-NDS/PRET>
<https://www.zdnet.com/article/80000-printers-are-exposing-their-ipp-port-online/>
<https://0x00sec.org/t/an-introduction-to-printer-exploitation/3565>
<https://www.freebuf.com/articles/web/205636.html>
<https://www.anquanke.com/post/id/86900>
