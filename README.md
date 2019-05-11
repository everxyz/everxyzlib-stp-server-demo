# 使用说明

**注意**: 本示例为测试版本, 仅仅用于现阶段的测试需求!

**此demo适用于Everxyz的EverAPI产品，运行此demo前，请先阅读[EverAPI开发文档](https://www.everxyz.com/api)的stp格式部分。**

## 环境
1.安装[python3](https://www.python.org/)；
2.操作系统：ubuntu；


## 用途

本示例展示您的后端服务器与 *evercad step api* 交互的示例, 后端服务器采用 python Flask 框架, 数据库使用 sqlite3.



示例主要用于展示:

1. 您的网站用户从上传 step 文件到查看模型的流程.
2. 您的网站服务器如何与 evercad 交互, 并得到 modelid.
3. 网页中如何引入 evercad api, 并渲染出 stp 模型.



## 使用步骤

1. 向 [evercad](https://www.everxyz.com/) 申请 [stp server](https://test.everxyz.com/stp/) 用户名和密码，联系方式见官网

2. 登录 [stp server](https://test.everxyz.com/stp/), 创建新的 clientid, 填写您网站的域名 (eg, `localhost:8080`)

3. 安装依赖包: `pip install -r requirements.txt`

4. 编辑 `config.py`, 配置下列几项:

   ```python
   # 以下 3 条内容需联系 evercad 申请                                
   EVERCAD_USERNAME = os.environ.get('EVERCAD_USERNAME') or 'username'
   EVERCAD_PWD = os.environ.get('EVERCAD_PWD') or 'pwd'               
   CLIENTID = os.environ.get('CLIENTID') or 'your client id'          
   ```

5. 创建数据库:

   ```bash
   $ ./manage.py shell （windows下则运行命令:python manage.py shell）
   >> db.create_all()
   >> quit()
   ```

6. 运行服务器

   ```bash
   $ ./manage.py runserver -p 8080 (windows下则运行命令:python manage.py runserver -p 8080)
   ```
7. 运行后浏览器访问localhost:8080,即可进入前端页面
 
8. 前端页面为模拟用户的主页，主页点“注册”并注册后，用注册的用户名登录，后可上传stp文件并体验渲染。
