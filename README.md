# Auto Proxy
## 功能

由于DDNS生效时间过长，对于爬虫等一些时间要求比较紧迫的项目就不太适用，为此本项目根据DDNS基本原理来实现实时获取ADSL拨号主机IP。

## 基本原理

client文件夹由ADSL拨号客户机运行。它会定时执行拨号操作，然后请求某个固定地址的服务器，以便让服务器获取ADSL拨号客户机的IP，主要是定时bash脚本运行。

server文件夹是服务器端运行，利用Python的Flask搭建服务器，然后接收ADSL拨号客户机的请求，得到remote_addr，获取客户机拨号后的IP。

## 项目结构

### server

- config.py 配置文件。
- ip 客户端请求后获取的客户端IP，文本保存。
- main.py Flask主程序，提供两个接口，一个是接收客户端请求，然后将IP保存，另外一个是获取当前保存的IP。

### client

* crontab 定时任务命令示例。
* pppoe.sh 拨号脚本，主要是实现重新拨号的几个命令。
* request.sh 请求服务器的脚本，主要是实现拨号后请求服务器的操作。
* request.conf 配置文件。

## 使用

### 服务器

服务器提供两个功能，record方法是客户机定时请求，然后获取客户机IP并保存。proxy方法是供我们自己用，返回保存的客户机IP，提取代理。

#### 克隆项目

```
git clone https://github.com/Germey/AutoProxy.git
```

#### 安装Python

安装Python版本2.7。

###### Ubuntu、Debian、Deepin

```
sudo apt-get install python2.7 python-pip
```

##### CentOS、RedHat

```
sudo yum install python27 python-pip
```

#### 安装Python包

```
pip install flask werkzeug itsdangerous click
```

#### 修改配置

修改config.py文件

* KEY 是客户端请求服务器时的凭证，在client的request.conf也有相同的配置，二者保持一致即可。

* NEED_AUTH 在获取当前保存的IP（即代理的IP）的时候，为防止自己的主机代理被滥用，在获取IP的时候，需要加权限验证。

* AUTH_USER和AUTH_PASSWORD分别是认证用户名密码。

* PORT默认端口，返回保存的结果中会自动添加这个端口，组成一个IP:PORT的代理形式。

  注意默认是8888，你需要用Squid或者TinyProxy配置下代理，端口是8888，这里端口8888即默认的拨号VPS的代理端口，这里配置下保证输出结果自动拼接端口。

### 运行

```
cd server
nohup python main.py &
```

这样就会在5000端口启动服务，如果想修改端口，可以手动修改main.py里面的端口5000为其他。

### ADSL客户机

#### 克隆项目

```
git clone https://github.com/Germey/AutoProxy.git
```

#### 修改配置

修改request.conf文件

* KEY 是客户端请求服务器时的凭证，在server的config.py也有相同的配置，二者保持一致即可。
* SERVER是服务器项目运行后的地址，一般为http://<服务器IP>:<服务端口>/record。如`http://120.27.14.24:5000/record`。

修改pppoe.sh文件

这里面写上重新拨号的几条命令，记得在前两行配置一下环境变量，配置上拨号命令所在的目录，以防出现脚本无法运行的问题。

比如我的是

```
pppoe-stop
pppoe-start
```

当然有的主机可能是

```
adsl-stop
adsl-start
```

不同主机拨号命令不一样，在这里把停止和启动拨号的命令写上。具体请看服务商提供的拨号命令。

### 运行

设置定时任务

```
crontab -e
```

输入crontab的实例命令

```
*/5 * * * * /var/py/AutoProxy/client/request.sh /var/py/AutoProxy/client/request.conf >> /var/py/AutoProxy/client/request.log
```

注意修改路径，你的项目在哪里，都统一修改成自己项目的路径。

最前面的*/5是5分钟执行一次。

好了，保存之后，定时任务就会开启。

## 验证结果

这样一来，访问服务器地址，就可以得到ADSL拨号客户机的IP了。

```python
import requests

url = 'http://120.27.14.24:5000'
proxy = requests.get(url, auth=('admin', '123')).text
print(proxy)
```

实例结果：

```
116.208.97.22:8888
```

## 扩展

如果你有域名，可以自己解析一个域名，这样就可以直接请求自己的域名，拿到实时好用的代理了，而且定时更新。

![](http://opencdn.cuiqingcai.com/proxy.png)

## 代理设置

### urllib2

```python
import urllib2
proxy_handler = urllib2.ProxyHandler({"http": 'http://' + proxy})
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
response = urllib2.urlopen('http://httpbin.org/get')
print response.read()
```

### requests

```python
import requests
proxies  = {
  'http': 'http://' + proxy,
}
r = requests.get('http://httpbin.org/get', proxies=proxies)
print(r.text)
```