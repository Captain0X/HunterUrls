# -*- coding: utf-8 -*-
# author: Captain0X
# time:2023年1月14日 23:56:38
from flask import Flask, request
import base64,time,queue,os,re
import pandas as pd
from server_conf import engine_str,save_type,tablename,pop_duplicate
from urllib.parse import urlparse
from sqlalchemy import create_engine
if save_type=="mysql":
    engine=create_engine(engine_str)
else:
    engine=""

def init_table():
    if save_type=="mysql":
        sql=f'''
            CREATE TABLE IF NOT EXISTS `{tablename}` (
        `url` text,
        `referer` text,
        `update_time` text,
        `reg_uni_key` varchar(250),
        PRIMARY KEY (`reg_uni_key`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            '''
        try:
            engine.execute(sql)
            print("表初始化成功!")
        except Exception as exp:
            print("无法创建mysql数据表:",exp)

def insert_ignore_mysql(tablename,field_list, multiparams, insert_many_row= False):
    '''
    tablename : 表名
    field_list : 字段名列表
    values : list 插入数据，默认情况下只有一维列表
    insert_many_row : bool 插入一行数据还是多行数据
    '''

    new_col = [f"`{x}`" for x in field_list]
    sql = f'insert ignore into `{tablename}`({",".join(new_col)})values'
    if insert_many_row:
        row_length = len(multiparams[0])
    else:
        row_length = len(multiparams)
    sql = sql + f'({",".join(["%s" for _ in range(row_length)])})'
    result = engine.execute(sql, multiparams)
    print(tablename,"插入数据结果 影响行数:", result.rowcount)
    return result.rowcount

def gen_url_rule(url):
    '''生成url规则字典
    返回域名+正则表达式的字典
    '''
    parse_url=urlparse(url)
    host=parse_url.netloc
    re_key_list=['\d+','\w+','\w+\.\w+','\w+\d+']
    key_re = []
    arg_key = re.findall('[?&](.*?)=', url)
    for x in parse_url.path.split('/'):
        if x:
            key_len=len(x)
            for rk in re_key_list:
                fr=re.findall(rk,x)
                if fr:
                    if len(fr[0])==key_len:  #命中规则
                        key_re.append(rk+"*"+str(key_len))
                        break
    return f'{host}{"/".join(key_re)}?{"&".join(arg_key)}'

def save_data(data_str):
    
    # data_str="eyJiYnMua2FueHVlLmNvbSI6WyJodHRwczovL3d3dy5rYW54dWUuY29tL3VzZXItb25saW5lX3NlbmRtc2cuaHRtIiwiaHR0cHM6Ly96aHVhbmxhbi5rYW54dWUuY29tL2FydGljbGUtMS5odG0iLCJodHRwOi8vYmVpYW4ubWlpdC5nb3YuY24vIiwiaHR0cDovL3d3dy5iZWlhbi5nb3YuY24vcG9ydGFsL3JlZ2lzdGVyU3lzdGVtSW5mbz9kb21haW5uYW1lPSUyN3BlZGl5LmNvbSUyNyZyZWNvcmRjb2RlPTMxMDExNTAyMDA2NjExIiwiaHR0cHM6Ly9iYnMua2FueHVlLmNvbS9sYW5nL3poLWNuL2Jicy5qcz8xLjUiLCJodHRwczovL2Jicy5rYW54dWUuY29tL3ZpZXcvanMvanF1ZXJ5LTMuMS4wLmpzPzEuNSIsImh0dHBzOi8vYmJzLmthbnh1ZS5jb20vdmlldy9qcy9wb3BwZXIuanM/MS41IiwiaHR0cHM6Ly9iYnMua2FueHVlLmNvbS92aWV3L2pzL2Jvb3RzdHJhcC5qcz8xLjUiLCJodHRwczovL2Jicy5rYW54dWUuY29tL3ZpZXcvanMveGl1bm8uanM/MTY3MzcwOTA3OCIsImh0dHBzOi8vYmJzLmthbnh1ZS5jb20vdmlldy9qcy9zdG9yYWdlUGx1cy5qcyIsImh0dHBzOi8vd3d3Lmthbnh1ZS5jb20vdmlldy9qcy9ib290c3RyYXAtcGx1Z2luLmpzPzEuNSIsImh0dHBzOi8vd3d3Lmthbnh1ZS5jb20vdmlldy9qcy9sYXllci9sYXllci5qcyIsImh0dHBzOi8vYmJzLmthbnh1ZS5jb20vdmlldy9qcy9hc3luYy5qcz8xLjUiLCJodHRwczovL2Jicy5rYW54dWUuY29tL3ZpZXcvanMvZm9ybS5qcz8xLjUiLCJodHRwczovL2Jicy5rYW54dWUuY29tL3ZpZXcvanMvYmJzLmpzPzEuNSIsImh0dHBzOi8vYmJzLmthbnh1ZS5jb20vdmlldy9qcy9ncm91cC9pY29uZm9udC5qcyIsImh0dHBzOi8vYmJzLmthbnh1ZS5jb20vdmlldy9qcy9mYWNlLmpzPzEuNSIsImh0dHBzOi8vcGFzc3BvcnQua2FueHVlLmNvbS9wYy92aWV3L2pzL3FxTGV2ZWwuanMiLCJodHRwczovL2Jicy5rYW54dWUuY29tL3ZpZXcvanMvdG9jYm90Lm1pbi5qcyJdfQ=="
    data=base64.b64decode(data_str).decode()
    resp=eval(data)
    for referer,urls in resp.items():
        values=[[x] for x in urls]
        df=pd.DataFrame(values,columns=['url'],dtype=str)
        df['referer']=referer
        df['update_time']=time.strftime('%Y-%m-%d %H:%M:%S')
        df['reg_uni_key'] = df.url.apply(gen_url_rule)  # 去掉以.html结尾的静态页面
        if pop_duplicate:
            df.drop_duplicates(subset=['reg_uni_key'], inplace=True)
        if save_type=="mysql":
            try:
                insert_ignore_mysql(tablename,df.columns.tolist(), df.values.tolist(), insert_many_row= True)
            except Exception as exp:
                print("数据库写入数据失败，请检查配置:",exp)
        elif save_type=="csv":
            try:
                file_name=os.path.split(os.path.realpath(__file__))[0]+'/'+tablename+".csv"
                df.to_csv(file_name,index=False,mode="a",encoding="utf-8",header=False,columns=df.columns.tolist())
                print("数据成功存入文件:",file_name)
            except PermissionError as exp:
                print("请不要打开csv文件，否则无法写入新数据")


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def ask_route():
    msg = """数据存储服务启动完毕..."""
    return msg


@app.errorhandler(404)
def page_not_found(e):
    return '民国三年等不到一场雨,一生等不到表哥一句我带你！', 404


@app.errorhandler(500)
def page_not_found(e):
    return '接口似乎被外星人吃了！', 500


@app.route("/save_api", methods=['GET'])
def save_api():
    data_base64 = request.args.get("data_base64")
    save_data(data_base64)
    return "save success!"


if __name__ == '__main__':
    init_table()
    app.run('127.0.0.1', 12587)