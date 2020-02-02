# 2019nCoV

#### 介绍
获得疫情最新状况

#### 软件架构
python3<br>
sqlite3<br>

#### 安装教程
pip install -r requirements.txt<br>

#### 使用说明
Main.py update 更新数据<br>
Main.py send   发送邮件<br>
Main.py aoto   自动(更新数据->发送邮件),一般定时执行这个<br>
Server.py      启动http服务

### 注意
1.订阅添加,暂时先直接去database数据库的emails表添加邮箱,后期会完善邮箱操作<br>
2.根据.env-template文件提示配置<br>