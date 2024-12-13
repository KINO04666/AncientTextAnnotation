from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='test'
    )
    return connection

@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.json
    user_email = data.get('user_email')
    user_password = data.get('user_password')

    if not user_email or not user_password:
        return jsonify({'error': 'Missing email or password'}), 400

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # 检查 user_email 是否已存在
                cursor.execute('SELECT user_id FROM user WHERE user_email = %s', (user_email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    return jsonify({'error': 'User email already exists'}), 400

                # 插入新用户
                cursor.execute('INSERT INTO user (user_email, user_password) VALUES (%s, %s)', (user_email, user_password))
                connection.commit()

        return jsonify({'message': 'User added!'}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


# 用户登录接口
@app.route('/api/userLogin', methods=['POST'])
def user_login():
    data = request.get_json()

    if not data:
        return jsonify({'user-login': '请求体无效'}), 400

    user_email = data.get('user_email')
    user_password = data.get('user_password')

    if not user_email or not user_password:
        return jsonify({'user-login': '请提供邮箱和密码'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'user-login': '数据库连接失败'}), 500

    cursor = connection.cursor(dictionary=True)

    # 查询用户
    query = "SELECT user_password FROM user WHERE user_email = %s"
    try:
        cursor.execute(query, (user_email,))
        result = cursor.fetchone()

        # 检查用户是否存在
        if not result:
            return jsonify({'user-login': '用户不存在'}), 401

        # 密码检查
        if result['user_password'] == user_password:
            return jsonify({'user-login': '成功'}), 200
        else:
            return jsonify({'user-login': '邮箱或密码错误'}), 401

    except Error as e:
        print(f"查询错误: {e}")
        return jsonify({'user-login': f'查询错误: {e}'}), 500

    finally:
        # 确保结果已被读取或处理完
        cursor.fetchall()  # 防止未读取的结果造成错误
        cursor.close()
        connection.close()


@app.route('/api/getUserid', methods=['GET'])
def get_userid():
    user_email = request.args.get('user_email')

    if not user_email:
        return jsonify({'user-id': '请提供邮箱'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 查询用户ID
    query = "SELECT user_id FROM user WHERE user_email = %s"
    try:
        cursor.execute(query, (user_email,))
        result = cursor.fetchone()

        # 处理查询结果
        if result:
            return jsonify({'user-id': result['user_id']}), 200
        else:
            return jsonify({'user-id': '用户不存在'}), 404

    except Error as e:
        print(f"查询错误: {e}")
        return jsonify({'user-id': '查询错误'}), 500
    finally:
        # 确保所有结果都被读取，避免“Unread result”错误
        cursor.fetchall()  # 读取并丢弃未处理的查询结果
        cursor.close()
        connection.close()



# 查询用户信息接口
@app.route('/api/get_users', methods=['GET'])
def get_users():
    try:
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM user')
                users = cursor.fetchall()
        return jsonify(users)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


# 创建新项目接口
@app.route('/api/createProject', methods=['POST'])
def create_project():
    data = request.get_json()

    user_id = data.get('user_id')
    project_id = data.get('project_id')
    project_name = data.get('project_name')
    project_describe = data.get('project_describe')

    if not user_id or not project_id or not project_name or not project_describe:
        return jsonify({'status': 'error', 'message': '请提供完整的项目参数'}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({'status': 'error', 'message': '数据库连接失败'}), 500

    cursor = connection.cursor()

    # 插入新项目
    query = """INSERT INTO project (user_id, project_id, project_name, project_describe, project_create, project_modify)  
               VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"""
    try:
        cursor.execute(query, (user_id, project_id, project_name, project_describe))
        connection.commit()
        return jsonify({'status': 'success', 'message': '项目创建成功'}), 201
    except Error as e:
        print(f"插入错误: {e}")
        return jsonify({'status': 'error', 'message': '项目创建失败'}), 500
    finally:
        cursor.close()
        connection.close()

# 获取用户项目信息接口
@app.route('/api/getProject', methods=['GET'])
def get_project():

    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'project-list': '请提供用户id'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 查询用户项目
    query = "SELECT project_id, project_name, project_describe, project_create, project_modify FROM project WHERE user_id = %s"
    try:
        cursor.execute(query, (user_id,))
        projects = cursor.fetchall()

        # 返回项目信息
        return jsonify({'project-list': projects}), 200
    except Error as e:
        print(f"查询错误: {e}")
        return jsonify({'project-list': '查询错误'}), 500
    finally:
        cursor.close()
        connection.close()


# 删除项目接口
@app.route('/api/deleteProject', methods=['DELETE'])
def delete_project():
    data = request.get_json()

    project_id = data.get('project_id')

    if not project_id:
        return jsonify({'status': 'error', 'message': '请提供项目ID'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    # 删除项目
    query = "DELETE FROM project WHERE project_id = %s"
    try:
        cursor.execute(query, (project_id,))
        connection.commit()

        # 检查受影响的行数
        if cursor.rowcount > 0:
            return jsonify({'status': 'success', 'message': '项目删除成功'}), 200
        else:
            return jsonify({'status': 'error', 'message': '项目不存在'}), 404
    except Error as e:
        print(f"删除错误: {e}")
        return jsonify({'status': 'error', 'message': '项目删除失败'}), 500
    finally:
        cursor.close()
        connection.close()


# 修改项目名称和描述接口
@app.route('/api/changeProject', methods=['PUT'])
def change_project():
    data = request.get_json()

    project_id = data.get('project_id')
    project_name = data.get('project_name')
    project_describe = data.get('project_describe')

    if not project_id or not project_name or not project_describe:
        return jsonify({'status': 'error', 'message': '请提供完整的项目参数'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    # 更新项目信息
    query = """UPDATE project   
               SET project_name = %s, project_describe = %s, project_modify = CURRENT_TIMESTAMP
               WHERE project_id = %s"""
    try:
        cursor.execute(query, (project_name, project_describe, project_id))
        connection.commit()

        # 检查受影响的行数
        if cursor.rowcount > 0:
            return jsonify({'status': 'success', 'message': '项目修改成功'}), 200
        else:
            return jsonify({'status': 'error', 'message': '项目不存在'}), 404
    except Error as e:
        print(f"更新错误: {e}")
        return jsonify({'status': 'error', 'message': '项目修改失败'}), 500
    finally:
        cursor.close()
        connection.close()

# 新建用户项目文档接口
@app.route('/api/createDocument', methods=['POST'])
def create_document():

    data = request.get_json()

    user_id = data.get('user_id')
    project_id = data.get('project_id')
    doc_id = data.get('doc_id')
    doc_name = data.get('doc_name')
    doc_content=data.get('doc_content')
    doc_describe = data.get('doc_describe')

    # 检查必填参数
    if not (user_id and project_id and doc_id and doc_name and doc_describe):
        return jsonify({'status': 'error', 'message': '请提供完整的文档参数'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 插入文档信息
    query = """INSERT INTO document (user_id, project_id, doc_id, doc_name, doc_content, doc_describe, doc_create, doc_modify)   
                   VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"""
    try:
        cursor.execute(query, (user_id, project_id, doc_id, doc_name, doc_content, doc_describe))
        connection.commit()
        return jsonify({'status': 'success', 'message': '文档创建成功'}), 201
    except Error as e:
        print(f"插入错误: {e}")
        return jsonify({'status': 'error', 'message': '文档创建失败'}), 500
    finally:
        cursor.close()
        connection.close()


# 删除用户项目文档接口
@app.route('/api/deleteDocument', methods=['DELETE'])
def delete_document():
    data = request.get_json()

    doc_id = data.get('doc_id')

    if not doc_id:
        return jsonify({'status': 'error', 'message': '请提供文档ID'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 删除文档信息
    query = "DELETE FROM document WHERE doc_id = %s"
    try:
        cursor.execute(query, (doc_id,))
        connection.commit()

        # 检查受影响的行数
        if cursor.rowcount > 0:
            return jsonify({'status': 'success', 'message': '文档删除成功'}), 200
        else:
            return jsonify({'status': 'error', 'message': '文档不存在'}), 404
    except Error as e:
        print(f"删除错误: {e}")
        return jsonify({'status': 'error', 'message': '文档删除失败'}), 500
    finally:
        cursor.close()
        connection.close()


# 修改用户项目文档信息接口
@app.route('/api/changeDocument', methods=['PUT'])
def change_document():
    data = request.get_json()

    doc_id = data.get('doc_id')
    doc_name = data.get('doc_name')
    doc_describe = data.get('doc_describe')
    doc_content = data.get('doc_content')

    # 检查必填参数
    if not (doc_id and doc_name and doc_describe):
        return jsonify({'status': 'error', 'message': '请提供完整的文档参数'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 更新文档信息
    query = """UPDATE document   
               SET doc_name = %s, doc_describe = %s, doc_content = %s, doc_modify = CURRENT_TIMESTAMP
               WHERE doc_id = %s"""
    try:
        cursor.execute(query, (doc_name, doc_describe, doc_content, doc_id))
        connection.commit()

        # 检查受影响的行数
        if cursor.rowcount > 0:
            return jsonify({'status': 'success', 'message': '文档修改成功'}), 200
        else:
            return jsonify({'status': 'error', 'message': '文档不存在'}), 404
    except Error as e:
        print(f"更新错误: {e}")
        return jsonify({'status': 'error', 'message': '文档修改失败'}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run()