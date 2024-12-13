添加了部分前端请求的后端接口<br>
***文件app.py中是flask后端代码，test.sql是创建数据库的sql语句***<br>
完成的后端接口包括：
### 注册接口
`@app.route('/api/add_user', methods=['POST'])`
### 用户登录接口
`@app.route('/api/userLogin', methods=['POST'])`
### 获取用户id接口
`@app.route('/api/getUserid', methods=['GET'])`
### 查询用户信息接口
`@app.route('/api/get_users', methods=['GET'])`
### 创建新项目接口
`@app.route('/api/createProject', methods=['POST'])`
### 获取用户项目信息接口
`@app.route('/api/getProject', methods=['GET'])`
### 删除项目接口
`@app.route('/api/deleteProject', methods=['DELETE'])`
### 修改项目名称和描述接口
`@app.route('/api/changeProject', methods=['PUT'])`
### 新建用户项目文档接口
`@app.route('/api/createDocument', methods=['POST'])`
### 删除用户项目文档接口
`@app.route('/api/deleteDocument', methods=['DELETE'])`
### 修改用户项目文档信息接口
`@app.route('/api/changeDocument', methods=['PUT'])`
<br>
已创建的数据表包括：
***用户表（user）、项目表（project）、文档表(document)***
