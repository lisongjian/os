## 服务器端

### 初始化开发环境

```bash
git init
git clone 
cd os
sudo apt-get install python-pip python-mysqldb python-lxml
pip install -i http://pypi.douban.com/simple -r requirements.txt
python app.py
```

### RUN

```bash
python app.py
```

```
Usage: app.py [OPTIONS]

Options:

  --address                        绑定指定地址 (default 127.0.0.1)
  --autoreload                     代码变化的时候是否自动加载代
                                    (default False)
  --config                         配置文件路径 (default settings.yaml)
  --debug                          是否开启Debug模式 (default False)
  --help                           show this help information
  --port                           绑定指定端口 (default 8888)
  --process                        是否开启都进程模式，默认不开
                                   ，0表示跟CPU核数一样 (default -1)

/usr/local/lib/python2.7/dist-packages/tornado/log.py options:

  --log_file_max_size              max size of log files before rollover
                                   (default 100000000)
  --log_file_num_backups           number of log files to keep (default 10)
  --log_file_prefix=PATH           Path prefix for log files. Note that if you
                                   are running multiple tornado processes,
                                   log_file_prefix must be different for each
                                   of them (e.g. include the port number)
  --log_to_stderr                  Send log output to stderr (colorized if
                                   possible). By default use stderr if
                                   --log_file_prefix is not set and no other
                                   logging is configured.
  --logging=debug|info|warning|error|none 
                                   Set the Python log level. If 'none', tornado
                                   won't touch the logging configuration.
                                   (default info)
```
