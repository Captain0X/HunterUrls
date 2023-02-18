# -*- coding: utf-8 -*-
# author: Captain0X
# time:2023年1月14日 23:56:38
#可选参数:mysql  csv 
#强烈推荐使用mysql
save_type="csv"
#mysql配置
tablename='web_url_collection' #存储的表名
username = 'root'  # 数据库用户名称
password= 'root'  # 数据库用户密码
mysql_ip = 'localhost'  # 数据库IP
mysql_port = '3306'  # 数据库端口
db_name = 'ylr_team_db'  # 数据库名称
engine_str = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8"%(username,password,mysql_ip,mysql_port,db_name)
#为了减少不必要的网站链接抓取，可以使用正则表达式对url进行筛选
#比如正则表达式匹配hm\.baidu\.com，那么当链接中存在符合这个表达式的url，会直接剔除，多个匹配规格使用|隔开
#强烈推荐正则表达式在线匹配网站:https://regex101.com/
black_list_reg='hm\.baidu\.com|127\.0\.0\.1|beian\.miit\.gov\.cn'

#对链接开启去重功能,删除重复的参数以及域名，降低数据量，可选参数:True False
pop_duplicate=True