from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from mysql.connector import Error
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import jwt

# JWT 密钥
SECRET_KEY = "4c7a3b9e3f2d4f7a6c8e5b7d1a2f0c9e9b4e2a3f1d2c3b4d1f5a7c3d4e2f1b6"  # 替换为你自己的密钥
app = Flask(__name__)
CORS(app)

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='admin123',
        password='123456',
        database='test',
        auth_plugin='mysql_native_password',
        charset='utf8mb4'  # 确保连接使用 utf8mb4 字符集
    )
    return connection
def decode_jwt(token):#用来解密jwt
    try:
        # 解密并验证 Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")  # 从 payload 提取 user_id
        return user_id
    except jwt.ExpiredSignatureError:
        print("Token 已过期")
        return None
    except jwt.InvalidTokenError:
        print("无效的 Token")
        return None

@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.json
    user_email = data.get('user_email')
    user_password = data.get('user_password')

    if not user_email or not user_password:
        return jsonify({'error': 'Missing required fields'}), 400

    hashed_password = generate_password_hash(user_password)  # 加密密码

    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': '数据库连接失败'}), 500

        cursor = connection.cursor(dictionary=True)

        # 检查邮箱是否存在
        cursor.execute('SELECT user_id FROM user WHERE user_email = %s', (user_email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'error': '邮箱已被注册'}), 400

        # 插入新用户
        cursor.execute(
            'INSERT INTO user (user_email, user_password) VALUES ( %s, %s)',
            (user_email, hashed_password)
        )
        connection.commit()

        return jsonify({'message': 'User added!'}), 201

    except Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 用户登录接口
# 登录接口
@app.route('/api/userLogin', methods=['POST'])
def user_login():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "请求体无效"}), 400

    user_email = data.get('user_email')
    user_password = data.get('user_password')

    if not user_email or not user_password:
        return jsonify({"success": False, "message": "请提供邮箱和密码"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "数据库连接失败"}), 500

    cursor = connection.cursor(dictionary=True)
    query = "SELECT user_id, user_password FROM user WHERE user_email = %s"

    try:
        cursor.execute(query, (user_email,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"success": False, "message": "用户不存在"}), 401

        if check_password_hash(result['user_password'], user_password):
            user_id = result['user_id']

            # 生成 JWT Token
            payload = {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(days=1)  # Token 1天过期
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return jsonify({
                "success": True,
                "message": "Login Successful!",
                "user_id": token  # 返回加密 Token
            }), 200
        else:
            return jsonify({"success": False, "message": "邮箱或密码错误"}), 401

    except Exception as e:
        print(f"查询错误: {e}")
        return jsonify({"success": False, "message": f"查询错误: {e}"}), 500

    finally:
        cursor.close()
        connection.close()

# @app.route('/api/getUserid', methods=['GET'])
# def get_userid():
#     user_email = request.args.get('user_email')
#
#     if not user_email:
#         return jsonify({'user-id': '请提供邮箱'}), 400
#
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#
#     # 查询用户ID
#     query = "SELECT user_id FROM user WHERE user_email = %s"
#     try:
#         cursor.execute(query, (user_email,))
#         result = cursor.fetchone()
#
#         # 处理查询结果
#         if result:
#             return jsonify({'user-id': result['user_id']}), 200
#         else:
#             return jsonify({'user-id': '用户不存在'}), 404
#
#     except Error as e:
#         print(f"查询错误: {e}")
#         return jsonify({'user-id': '查询错误'}), 500
#     finally:
#         # 确保所有结果都被读取，避免“Unread result”错误
#         cursor.fetchall()  # 读取并丢弃未处理的查询结果
#         cursor.close()
#         connection.close()



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
    user_id = decode_jwt(data.get('user_id'))
    project_name = data.get('project_name')
    project_describe = data.get('project_describe')
    #print(user_id, project_name, project_describe)
    if not user_id or not project_name:
        return jsonify({'status': 'error', 'message': '请提供完整的项目参数'}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({'status': 'error', 'message': '数据库连接失败'}), 500

    cursor = connection.cursor()

    # 插入新项目，project_id 字段不需要传入，数据库会自动生成
    query = """INSERT INTO project (user_id, project_name, project_describe, project_create, project_modify)  
               VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"""
    try:
        cursor.execute(query, (user_id, project_name, project_describe))
        connection.commit()

        # 获取新插入的项目的 project_id
        project_id = cursor.lastrowid  # 获取刚插入记录的ID

        return jsonify({'status': 'success', 'message': '项目创建成功', 'project_id': project_id}), 201
    except Error as e:
        print(f"插入错误: {e}")
        return jsonify({'status': 'error', 'message': '项目创建失败'}), 500
    finally:
        cursor.close()
        connection.close()

# 获取用户项目信息接口
@app.route('/api/getProject', methods=['GET'])
def get_project():

    user_id = decode_jwt(request.args.get('user_id'))

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

# # 新建用户项目文档接口
# @app.route('/api/createDocument', methods=['POST'])
# def create_document():
#
#     data = request.get_json()
#
#     user_id = data.get('user_id')
#     project_id = data.get('project_id')
#     doc_id = data.get('doc_id')
#     doc_name = data.get('doc_name')
#     doc_content=data.get('doc_content')
#     doc_describe = data.get('doc_describe')
#
#     # 检查必填参数
#     if not (user_id and project_id and doc_id and doc_name and doc_describe):
#         return jsonify({'status': 'error', 'message': '请提供完整的文档参数'}), 400
#
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#
#     # 插入文档信息
#     query = """INSERT INTO document (user_id, project_id, doc_id, doc_name, doc_content, doc_describe, doc_create, doc_modify)
#                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"""
#     try:
#         cursor.execute(query, (user_id, project_id, doc_id, doc_name, doc_content, doc_describe))
#         connection.commit()
#         return jsonify({'status': 'success', 'message': '文档创建成功'}), 201
#     except Error as e:
#         print(f"插入错误: {e}")
#         return jsonify({'status': 'error', 'message': '文档创建失败'}), 500
#     finally:
#         cursor.close()
#         connection.close()


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
#列举所有文档表
@app.route('/projects/<int:project_id>/documents', methods=['GET'])
def get_documents(project_id):
    connection = get_db_connection()  # 获取数据库连接
    if connection is None:
        return jsonify({'error': '数据库连接失败'}), 500

    cursor = connection.cursor(dictionary=True)  # 获取游标，返回字典格式结果

    query = "SELECT * FROM document WHERE project_id = %s"
    try:
        cursor.execute(query, (project_id,))
        documents = cursor.fetchall()
        return jsonify(documents)
    except Error as e:
        print(f"查询文档失败: {e}")
        return jsonify({'error': '获取文档失败'}), 500
    finally:
        cursor.close()
        connection.close()

#上传文档
@app.route('/projects/<int:project_id>/documents', methods=['POST'])
def create_document(project_id):
    data = request.get_json()

    # 获取前端传递的参数
    doc_name = data.get('name')
    doc_desc = data.get('description', '')  # 如果没有描述，默认空字符串
    doc_content = data.get('content', '')  # 如果没有内容，默认空字符串
    user_id = decode_jwt(data.get('user_id'))
    if not doc_name:
        return jsonify({'error': '文档名称是必填项'}), 400

    # 获取数据库连接
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': '数据库连接失败'}), 500

    cursor = connection.cursor()

    # 插入文档记录到数据库
    query = """
        INSERT INTO document (user_id,project_id, doc_name, doc_content, doc_describe, doc_create,doc_modify)
        VALUES (%s,%s, %s, %s, %s, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)
    """
    try:
        cursor.execute(query, (user_id,project_id, doc_name, doc_content, doc_desc))
        connection.commit()
        new_doc_id = cursor.lastrowid  # 获取刚插入记录的ID

        # 返回新插入的文档信息
        new_doc = {
            'doc_id': new_doc_id,
            'project_id': project_id,
            'doc_name': doc_name,
            'doc_content': doc_content,
            'doc_describe': doc_desc,
            'doc_create': datetime.now().strftime('%Y-%m-%d'),
            'doc_modify': datetime.now().strftime('%Y-%m-%d'),
        }
        return jsonify(new_doc), 201
    except Error as e:
        print(f"插入文档失败: {e}")
        return jsonify({'error': '上传文档失败'}), 500
    finally:
        cursor.close()
        connection.close()

# # 修改用户项目文档信息接口
# @app.route('/api/changeDocument', methods=['PUT'])
# def change_document():
#     data = request.get_json()
#
#     doc_id = data.get('doc_id')
#     doc_name = data.get('doc_name')
#     doc_describe = data.get('doc_describe')
#     doc_content = data.get('doc_content')
#
#     # 检查必填参数
#     if not (doc_id and doc_name and doc_describe):
#         return jsonify({'status': 'error', 'message': '请提供完整的文档参数'}), 400
#
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#
#     # 更新文档信息
#     query = """UPDATE document
#                SET doc_name = %s, doc_describe = %s, doc_content = %s, doc_modify = CURRENT_TIMESTAMP
#                WHERE doc_id = %s"""
#     try:
#         cursor.execute(query, (doc_name, doc_describe, doc_content, doc_id))
#         connection.commit()
#
#         # 检查受影响的行数
#         if cursor.rowcount > 0:
#             return jsonify({'status': 'success', 'message': '文档修改成功'}), 200
#         else:
#             return jsonify({'status': 'error', 'message': '文档不存在'}), 404
#     except Error as e:
#         print(f"更新错误: {e}")
#         return jsonify({'status': 'error', 'message': '文档修改失败'}), 500
#     finally:
#         cursor.close()
#         connection.close()
#上传关系和实体和实体类 至数据库三个表
@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    user_id = data.get('user_id')
    project_id = data.get('project_id')
    if not user_id or not project_id:
        return jsonify({"error": "user_id and project_id are required"}), 400

    doc_name = data.get('doc_name', 'Unnamed Document')
    doc_describe = data.get('doc_describe', '')
    text = data.get('text', '')

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        # 插入 document 数据
        insert_doc_sql = """
            INSERT INTO document (user_id, project_id, doc_name, doc_content, doc_describe, doc_create, doc_modify)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(insert_doc_sql, (user_id, project_id, doc_name, text, doc_describe, now, now))
        conn.commit()
        doc_id = cursor.lastrowid

        # 插入 entities 数据
        entity_mapping = {}  # 原始 entity id -> 数据库 entity_id
        insert_entity_sql = """
            INSERT INTO entities (doc_id, original_id, start_pos, end_pos, label, text, color_background, color_border, color_fill)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for ent in data.get('entities', []):
            ent_params = (
                doc_id,
                ent['id'],
                ent['start'],
                ent['end'],
                ent['label'],
                ent.get('text'),
                ent['color']['background'],
                ent['color']['border'],
                ent['color']['fill']
            )
            cursor.execute(insert_entity_sql, ent_params)
            entity_db_id = cursor.lastrowid
            entity_mapping[ent['id']] = entity_db_id

        conn.commit()

        # 插入 relations 数据
        insert_relation_sql = """
            INSERT INTO relations (doc_id, from_entity_id, to_entity_id, type, color)
            VALUES (%s, %s, %s, %s, %s)
        """
        for rel in data.get('relations', []):
            from_id = rel['from']
            to_id = rel['to']
            if from_id not in entity_mapping or to_id not in entity_mapping:
                conn.rollback()
                return jsonify({"error": f"Relation references undefined entities: from {from_id} to {to_id}"}), 400

            rel_params = (
                doc_id,
                entity_mapping[from_id],
                entity_mapping[to_id],
                rel.get('type'),
                rel.get('color')
            )
            cursor.execute(insert_relation_sql, rel_params)

        conn.commit()

        # 插入 enti_types 数据
        insert_enti_type_sql = """
            INSERT INTO enti_types (doc_id, label, number, disabled, color_background, color_border, color_fill)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for enti in data.get('enti', []):
            enti_params = (
                doc_id,
                enti['label'],
                enti.get('number'),
                enti.get('disabled', False),
                enti['color']['background'],
                enti['color']['border'],
                enti['color']['fill']
            )
            cursor.execute(insert_enti_type_sql, enti_params)

        conn.commit()

        # 关闭连接
        cursor.close()
        conn.close()

        return jsonify({"message": "Data inserted successfully", "doc_id": doc_id}), 201

    except mysql.connector.Error as err:
        if conn.is_connected():
            conn.rollback()
        return jsonify({"error": str(err)}), 500
    except Exception as ex:
        if conn.is_connected():
            conn.rollback()
        return jsonify({"error": str(ex)}), 400
#获取实体表，关系表和实体类表
@app.route('/get/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        # 获取 document 数据
        cursor.execute("SELECT * FROM document WHERE doc_id = %s", (doc_id,))
        document = cursor.fetchone()
        if not document:
            return jsonify({"error": "Document not found"}), 404

        # 获取 entities 数据
        cursor.execute("SELECT * FROM entities WHERE doc_id = %s", (doc_id,))
        entities = cursor.fetchall()

        # 获取 relations 数据
        cursor.execute("SELECT * FROM relations WHERE doc_id = %s", (doc_id,))
        relations = cursor.fetchall()

        # 获取 enti_types 数据
        cursor.execute("SELECT * FROM enti_types WHERE doc_id = %s", (doc_id,))
        enti_types = cursor.fetchall()

        # 关闭连接
        cursor.close()
        conn.close()

        # 构建响应数据
        response = {
            "doc_id": document['doc_id'],
            "project_id": document['project_id'],
            "doc_name": document['doc_name'],
            "doc_content": document['doc_content'],
            "doc_describe": document['doc_describe'],
            "doc_create": document['doc_create'].isoformat() if document['doc_create'] else None,
            "doc_modify": document['doc_modify'].isoformat() if document['doc_modify'] else None,
            "entities": [],
            "relations": [],
            "enti": []
        }

        # 构建 entities
        for ent in entities:
            ent_data = {
                "id": ent['original_id'],
                "start": ent['start_pos'],
                "end": ent['end_pos'],
                "label": ent['label'],
                "text": ent['text'],
                "color": {
                    "background": ent['color_background'],
                    "border": ent['color_border'],
                    "fill": ent['color_fill']
                }
            }
            response["entities"].append(ent_data)

        # 构建 relations
        for rel in relations:
            rel_data = {
                "from": rel['from_entity_id'],
                "to": rel['to_entity_id'],
                "type": rel['type'],
                "color": rel['color']
            }
            response["relations"].append(rel_data)

        # 构建 enti_types
        for enti in enti_types:
            enti_data = {
                "label": enti['label'],
                "number": enti['number'],
                "disabled": enti['disabled'],
                "color": {
                    "background": enti['color_background'],
                    "border": enti['color_border'],
                    "fill": enti['color_fill']
                }
            }
            response["enti"].append(enti_data)

        return jsonify(response), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400
if __name__ == '__main__':
    app.run(debug=True)