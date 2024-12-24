from functools import wraps

from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from mysql.connector import Error
from datetime import datetime, timedelta

from numpy import number
from werkzeug.security import check_password_hash, generate_password_hash
import jwt

# JWT 密钥
SECRET_KEY = "4c7a3b9e3f2d4f7a6c8e5b7d1a2f0c9e9b4e2a3f1d2c3b4d1f5a7c3d4e2f1b6"  # 替换为你自己的密钥
app = Flask(__name__)
CORS(app)
def token_required(f):
    """装饰器：验证 Token 并提取用户信息"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # 从请求头中获取 Authorization 字段
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401

        token = token.split(" ")[1]  # 提取真正的 Token 部分

        try:
            # 验证 Token 并解码
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = payload["user_id"]  # 将 user_id 保存到 request 中
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)  # 执行实际的路由逻辑
    return decorated
def get_db_connection():
    connection = mysql.connector.connect(
        host='mysql.sqlpub.com',
        user='admin8203',
        password='qO7PDP5Jsg0bQk9I',
        database='ancient',
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
@token_required
def get_project():
    user_id = request.user_id
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
@token_required
def delete_project():
    user_id = request.user_id
    data = request.get_json()

    project_id = data.get('project_id')

    if not project_id:
        return jsonify({'status': 'error', 'message': '请提供项目ID'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    # 删除项目
    query = "DELETE FROM project WHERE project_id = %s"
    try:
        cursor.execute("SELECT * FROM project WHERE project_id = %s AND user_id = %s", (project_id,user_id))
        project = cursor.fetchall()
        if not project:
            return jsonify({"error": "Permission denied or project not found"}), 403
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
    cursor = connection.cursor()

    try:
        # 1. 删除关系表中与该文档相关的记录
        delete_relations_query = """
            DELETE FROM relations
            WHERE doc_id = %s
        """
        cursor.execute(delete_relations_query, (doc_id,))
        relations_deleted_count = cursor.rowcount

        # 2. 删除实体表中与该文档相关的记录
        delete_entities_query = """
            DELETE FROM entities
            WHERE doc_id = %s
        """
        cursor.execute(delete_entities_query, (doc_id,))
        entities_deleted_count = cursor.rowcount

        # 3. 删除实体类表中与该文档相关的记录
        delete_entity_classes_query = """
            DELETE FROM enti_types
            WHERE doc_id = %s
        """
        cursor.execute(delete_entity_classes_query, (doc_id,))
        entity_classes_deleted_count = cursor.rowcount

        # 4. 删除关系类表中与该文档相关的记录
        delete_relation_types_query = """
            DELETE FROM relation_types
            WHERE doc_id = %s
        """
        cursor.execute(delete_relation_types_query, (doc_id,))
        relation_types_deleted_count = cursor.rowcount

        # 5. 删除文档本身
        delete_document_query = """
            DELETE FROM document
            WHERE doc_id = %s
        """
        cursor.execute(delete_document_query, (doc_id,))
        document_deleted_count = cursor.rowcount

        # 提交事务
        connection.commit()

        # 返回删除的结果
        return jsonify({
            'status': 'success',
            'message': '文档及相关数据删除成功',
            'deleted': {
                'relations_deleted': relations_deleted_count,
                'entities_deleted': entities_deleted_count,
                'entity_classes_deleted': entity_classes_deleted_count,
                'relation_types_deleted': relation_types_deleted_count,
                'document_deleted': document_deleted_count
            }
        }), 200

    except Error as e:
        # 捕获数据库错误
        print(f"删除错误: {e}")
        connection.rollback()
        return jsonify({'status': 'error', 'message': '文档删除失败'}), 500
    finally:
        # 确保关闭游标和连接
        cursor.close()
        connection.close()

#列举所有文档表
@app.route('/projects/<int:project_id>/documents', methods=['GET'])
def get_documents(project_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer'):
        return jsonify({"error": "Missing or invalid token"}), 401
    user_id = decode_jwt(auth_header.split(" ")[1])
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401
    connection = get_db_connection()  # 获取数据库连接
    if connection is None:
        return jsonify({'error': '数据库连接失败'}), 500

    cursor = connection.cursor(dictionary=True)  # 获取游标，返回字典格式结果
    query = "SELECT * FROM document WHERE project_id = %s"
    try:
        cursor.execute("SELECT * FROM project WHERE project_id = %s AND user_id = %s", (project_id,user_id))
        project = cursor.fetchall()
        if not project:
            return jsonify({"error": "Permission denied or project not found"}), 403
        cursor.execute(query, (project_id,))
        documents = cursor.fetchall()

        return jsonify(documents)
    except Error as e:
        print(f"查询文档失败: {e}")
        return jsonify({'error': '获取文档失败'}), 500
    finally:
        cursor.close()
        connection.close()

#获取单个文档里的信息（用于验证doc_id）
@app.route('/document/<int:doc_id>', methods=['GET'])
def get_document_verified(doc_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer'):
        return jsonify({"error": "Missing or invalid token"}), 401
    user_id = decode_jwt(auth_header.split(" ")[1])
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401
    connection = get_db_connection()  # 获取数据库连接
    if connection is None:
        return jsonify({'error': '数据库连接失败'}), 500

    cursor = connection.cursor(dictionary=True)  # 获取游标，返回字典格式结果
    try:
        cursor.execute("SELECT * FROM document WHERE doc_id = %s AND user_id = %s", (doc_id,user_id))
        document = cursor.fetchall()
        if not document:
            return jsonify({"error": "Permission denied or document not found"}), 403
        return jsonify("Successfully!")
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

    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401
    if not doc_name:
        return jsonify({'error': '文档名称是必填项'}), 400

    # 获取数据库连接
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': '数据库连接失败'}), 500

    cursor = connection.cursor()
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    # 插入文档记录到数据库
    query = """
        INSERT INTO document (user_id,project_id, doc_name, doc_content, doc_describe, doc_create,doc_modify)
        VALUES (%s,%s, %s, %s, %s, %s,%s)
    """
    try:
        cursor.execute("SELECT * FROM project WHERE project_id = %s AND user_id = %s", (project_id,user_id))
        project = cursor.fetchall()
        if not project:
            return jsonify({"error": "Permission denied or project not found"}), 403
        cursor.execute(query, (user_id,project_id, doc_name, doc_content, doc_desc,now,now))
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
    entity_id = 0
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    d_id = data.get('doc_id')
    user_id = decode_jwt(data.get('user_id'))
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
        # 检查是否提供了 doc_id
        if not d_id:
            # 插入新文档
            insert_doc_sql = """
                       INSERT INTO document (user_id, project_id, doc_name, doc_content, doc_describe, doc_create, doc_modify)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)
                   """
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(insert_doc_sql, (user_id, project_id, doc_name, text, doc_describe, now, now))
            conn.commit()

        doc_id = data.get('doc_id')
        if(not doc_id):
            doc_id = cursor.lastrowid
        # 插入 entities 数据
        entity_mapping = {}  # 原始 entity id -> 数据库 entity_id
        insert_entity_sql = """
            INSERT INTO entities (doc_id, original_id ,start_pos, end_pos, label, text, color_background, color_border, color_fill)
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
            entity_id = entity_db_id
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
        # 插入 relation_types 数据
        insert_relation_types_sql = """
                INSERT INTO relation_types (doc_id, type, start_label, end_label, number, color)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
        for relation_types in data.get('relation_types', []):
            relation_types_params = (
                    doc_id,
                    relation_types['type'],
                    relation_types['start_label'],
                    relation_types['end_label'],
                    relation_types['number'],
                    relation_types['color'],
                )
            cursor.execute(insert_relation_types_sql, relation_types_params)

        conn.commit()
        # 关闭连接
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "doc_id": doc_id,"entity_id":entity_id}), 201

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
        # 获取 relation_types 数据
        cursor.execute("SELECT * FROM relation_types WHERE doc_id = %s", (doc_id,))
        relation_types = cursor.fetchall()
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
            "enti": [],
            "relation_types":[]
        }

        # 构建 entities
        for ent in entities:
            ent_data = {
                "id": ent['entity_id'],
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
                "id":rel['relation_id'],
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
        for relation in relation_types:
            relation_data={
                "id": relation['id'],
                "type": relation['type'],
                "start_label": relation['start_label'],
                "end_label": relation['end_label'],
                "number":relation['number'],
                "color":relation['color']
            }
            response["relation_types"].append(relation_data)
        return jsonify(response), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

# 删除实体及相关关系的接口
@app.route('/delete_entity', methods=['POST'])
def delete_entity():
    try:
        # 获取前端传递的参数
        data = request.json
        entity_id = data.get('entity_id')  # 实体ID
        doc_id = data.get('doc_id')
        if not entity_id:
            return jsonify({'status': 'error', 'message': '实体ID不能为空'}), 400

        # 连接到数据库
        conn = get_db_connection()
        cursor = conn.cursor()

        # 查询实体是否存在
        cursor.execute("SELECT entity_id FROM entities WHERE entity_id = %s AND doc_id=%s", (entity_id,doc_id))
        entity = cursor.fetchone()

        if not entity:
            return jsonify({'status': 'error', 'message': '实体不存在'}), 404

        # 删除与该实体相关的关系
        cursor.execute("DELETE FROM relations WHERE `from_entity_id` = %s OR `to_entity_id` = %s", (entity_id, entity_id))

        # 删除实体
        cursor.execute("DELETE FROM entities WHERE entity_id = %s", (entity_id,))

        # 提交更改
        conn.commit()

        return jsonify({'status': 'success', 'message': '实体及相关关系删除成功'})

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
        return jsonify({'status': 'error', 'message': '数据库操作失败'}), 500

    except Exception as e:
        print(f"错误: {e}")
        return jsonify({'status': 'error', 'message': '服务器内部错误'}), 500


# 更新实体的接口
@app.route('/update_enti', methods=['PUT'])
def update_enti():
    try:
        # 获取前端传递的 JSON 数据
        data = request.json
        doc_id = data.get('doc_id')  # 实体 ID
        label = data.get('label')  # 实体的新标签
        new_number = data.get('number')  # 实体的新属性（可选）

        # 验证数据是否完整
        if not doc_id or not label:
            return jsonify({'status': 'error', 'message': 'ID 和标签是必填项'}), 400
        conn = get_db_connection()

        # 连接到 MySQL 数据库
        cursor = conn.cursor()

        # 更新实体
        update_query = "UPDATE enti_types SET number = %s WHERE doc_id = %s AND label = %s"
        cursor.execute(update_query, ( new_number, doc_id,label,))

        # 提交更改
        conn.commit()

        # 检查受影响的行数
        if cursor.rowcount == 0:
            return jsonify({'status': 'error', 'message': '实体不存在或未更新'}), 404

        return jsonify({'status': 'success', 'message': '实体更新成功', 'updated_id': doc_id})

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
        return jsonify({'status': 'error', 'message': '数据库操作失败'}), 500

    except Exception as e:
        print(f"服务器错误: {e}")
        return jsonify({'status': 'error', 'message': '服务器内部错误'}), 500

@app.route('/delete_enti', methods=['DELETE'])
def delete_enti():
    try:
        # 获取前端传递的 JSON 数据
        data = request.json
        doc_id = data.get('doc_id')
        label = data.get('label')  # 实体类的 label

        if not label or not doc_id:
            return jsonify({'status': 'error', 'message': 'doc_id 和 label 是必填项'}), 400

        # 连接到 MySQL 数据库
        conn = get_db_connection()
        cursor = conn.cursor()

        # 查询符合条件的 entity_id
        cursor.execute("SELECT entity_id FROM entities WHERE label = %s AND doc_id = %s", (label, doc_id))
        entity_ids = cursor.fetchall()  # 获取所有符合条件的 entity_id

        # 如果没有找到实体，则返回错误
        if not entity_ids:
            return jsonify({'status': 'error', 'message': '未找到对应的实体'}), 404
        # 删除关系表中与这些 entity_id 相关的记录
        entity_ids = [row[0] for row in entity_ids]  # 提取所有 entity_id
        cursor.execute(
            "DELETE FROM relations WHERE from_entity_id IN (%s) OR to_entity_id IN (%s)" % (
                ', '.join(['%s'] * len(entity_ids)), ', '.join(['%s'] * len(entity_ids))
            ),
            entity_ids + entity_ids  # 双份的 entity_ids，用于 from_entity_id 和 to_entity_id
        )
        relations_deleted_count = cursor.rowcount
        # 删除实体类
        cursor.execute("DELETE FROM enti_types WHERE label = %s AND doc_id = %s", (label, doc_id))
        enti_deleted_count = cursor.rowcount

        # 删除实体表中具有相同 label 的实体
        cursor.execute("DELETE FROM entities WHERE label = %s AND doc_id = %s", (label, doc_id))
        entities_deleted_count = cursor.rowcount

        # 删除 relation_types 表中 start_label 和 end_label 都不能等于 label 的记录
        cursor.execute(
            "DELETE FROM relation_types WHERE start_label = %s OR end_label = %s", (label, label)
        )
        relation_types_deleted_count = cursor.rowcount

        # 提交事务
        conn.commit()

        return jsonify({
            'status': 'success',
            'message': '删除成功',
            'deleted': {
                'entity_classes_deleted': enti_deleted_count,
                'entities_deleted': entities_deleted_count,
                'relations_deleted': relations_deleted_count,
                'relation_types_deleted':relation_types_deleted_count
            }
        })

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
        return jsonify({'status': 'error', 'message': '数据库操作失败'}), 500

    except Exception as e:
        print(f"服务器错误: {e}")
        return jsonify({'status': 'error', 'message': '服务器内部错误'}), 500

@app.route('/add_relation', methods=['POST'])
def add_relation():
    try:
        # 获取前端传递的 JSON 数据
        data = request.json
        doc_id = data.get('doc_id')
        start_label = data.get('start_label')  # 起始实体标签
        end_label = data.get('end_label')      # 目标实体标签
        type = data.get('type')       # 关系类型
        number = data.get('number', 0)         # 关系数量，默认为 0
        color = data.get('color')              # 关系颜色

        # 参数校验
        if not all([start_label, end_label, type, color]):
            return jsonify({'status': 'error', 'message': '缺少必要参数'}), 400

        # 连接到 MySQL 数据库
        conn = get_db_connection()
        cursor = conn.cursor()

        # 插入关系类数据
        insert_query = """
        INSERT INTO relation_types (start_label, end_label, type, number, color,doc_id)
        VALUES (%s, %s, %s, %s, %s,%s)
        """
        cursor.execute(insert_query, (start_label, end_label, type, number, color,doc_id))

        # 提交事务
        conn.commit()

        return jsonify({'status': 'success', 'message': '关系类新增成功', 'relation_id': cursor.lastrowid})

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
        return jsonify({'status': 'error', 'message': '数据库操作失败'}), 500

    except Exception as e:
        print(f"服务器错误: {e}")
        return jsonify({'status': 'error', 'message': '服务器内部错误'}), 500
@app.route('/relations/instances', methods=['POST'])
def add_instance():
    try:
        # 获取前端传递的 JSON 数据
        data = request.json
        doc_id = data.get('doc_id')
        from_entity_id = data.get('from_entity_id')
        to_entity_id = data.get('to_entity_id')
        type = data.get('type')       # 关系类型
        color = data.get('color')              # 关系颜色

        # 参数校验
        if not all([from_entity_id, to_entity_id, type, color]):
            return jsonify({'status': 'error', 'message': '缺少必要参数'}), 400

        # 连接到 MySQL 数据库
        conn = get_db_connection()
        cursor = conn.cursor()

        # 插入关系类数据
        insert_query = """
        INSERT INTO relations (from_entity_id, to_entity_id, type, color,doc_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (from_entity_id, to_entity_id, type, color,doc_id))

        # 提交事务
        conn.commit()

        return jsonify({'status': 'success', 'message': '关系实例新增成功', 'id': cursor.lastrowid})

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
        return jsonify({'status': 'error', 'message': '数据库操作失败'}), 500

    except Exception as e:
        print(f"服务器错误: {e}")
        return jsonify({'status': 'error', 'message': '服务器内部错误'}), 500
@app.route('/relations/instances/<int:relation_id>', methods=['DELETE'])
def delete_relation_instance(relation_id):
    """
    删除指定的关系实例。
    请求参数：
        - relation_id: 关系实例的唯一ID（路径参数）
        - doc_id: 文档ID（查询参数）
    """
    data = request.args
    doc_id = data.get('doc_id')
    if not doc_id:
        return jsonify({"error": "doc_id is required"}), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        # 验证 doc_id 是否存在
        cursor.execute("SELECT doc_id FROM document WHERE doc_id = %s", (doc_id,))
        existing_doc = cursor.fetchone()
        if not existing_doc:
            return jsonify({"error": f"Document with id {doc_id} does not exist."}), 404

        # 验证关系实例是否存在且属于指定的文档
        cursor.execute("""
            SELECT relation_id FROM relations 
            WHERE relation_id = %s AND doc_id = %s
        """, (relation_id, doc_id))
        relation = cursor.fetchone()
        if not relation:
            return jsonify({"error": f"Relation with id {relation_id} does not exist in document {doc_id}."}), 404

        # 删除关系实例
        cursor.execute("""
            DELETE FROM relations 
            WHERE relation_id = %s AND doc_id = %s
        """, (relation_id, doc_id))
        conn.commit()

        return jsonify({"status": "success", "message": f"Relation {relation_id} deleted successfully."}), 200

    except mysql.connector.Error as err:
        if conn.is_connected():
            conn.rollback()
        print(f"MySQL Error: {err}")
        return jsonify({"error": str(err)}), 500
    except Exception as ex:
        if conn.is_connected():
            conn.rollback()
        print(f"Exception: {ex}")
        return jsonify({"error": str(ex)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# API 路由: 删除关系类及其关联实例
@app.route('/relations/<string:relation_type>', methods=['DELETE'])
def delete_relation(relation_type):
    doc_id = request.args.get('doc_id')  # 获取 doc_id 参数
    if not doc_id:
        return jsonify({"status": "error", "message": "缺少 doc_id 参数"}), 400

    # 调用删除逻辑
    result = delete_relation_kind(doc_id, relation_type)

    # 返回操作结果
    return jsonify(result)


# 删除关系实例和关系类
def delete_relation_kind(doc_id, relation_type):
    try:
        # 获取数据库连接
        connection = get_db_connection()
        if connection is None:
            return {"status": "error", "message": "无法连接数据库"}

        cursor = connection.cursor()

        # 先删除与关系类关联的所有关系实例
        delete_relations_query = "DELETE FROM relations WHERE type = %s AND doc_id=%s"
        cursor.execute(delete_relations_query, (relation_type,doc_id))

        # 然后删除关系类
        delete_relation_type_query = "DELETE FROM relation_types WHERE type = %s AND doc_id=%s"
        cursor.execute(delete_relation_type_query, (relation_type,doc_id))

        # 提交事务
        connection.commit()

        # 关闭数据库连接
        cursor.close()
        connection.close()

        return {"status": "success", "message": "关系类和相关关系实例删除成功"}

    except Error as e:
        return {"status": "error", "message": f"删除失败: {str(e)}"}

# 更新实体的接口
@app.route('/update_relation_types', methods=['PUT'])
def update_relation_types():
    try:
        # 获取前端传递的 JSON 数据
        data = request.get_json()
        relation_type = data.get('type')  # 关系类型
        increment = data.get('increment')  # 布尔值：true 或 false

        if relation_type is None or increment is None:
            return jsonify({'status': 'error', 'message': '缺少必要参数'}), 400

        # 连接到 MySQL 数据库
        conn = get_db_connection()
        cursor = conn.cursor()

        # 根据布尔值增减 `number`
        if increment:
            query = """
                UPDATE relation_types
                SET number = number + 1
                WHERE type = %s
            """
        else:
            query = """
                UPDATE relation_types
                SET number = number - 1
                WHERE type = %s
            """

        cursor.execute(query, (relation_type,))
        conn.commit()

        # 检查受影响的行数
        if cursor.rowcount > 0:
            return jsonify({'status': 'success', 'message': '更新成功', 'affected_rows': cursor.rowcount}), 200
        else:
            return jsonify({'status': 'error', 'message': '未找到对应的关系类型'}), 404

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
        return jsonify({'status': 'error', 'message': '数据库操作失败'}), 500

    except Exception as e:
        print(f"服务器错误: {e}")
        return jsonify({'status': 'error', 'message': '服务器内部错误'}), 500

    finally:
        # 确保关闭数据库连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)