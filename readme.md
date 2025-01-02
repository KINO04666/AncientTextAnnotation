前端默认登录用户为123456@qq.com 123456
换了npm源之后可以直接在front里输入npm install安装依赖 并输入npm run dev运行
如果不想使用云端服务可以将axios文件夹里的api改成本地的
# API 文档
本文档简要介绍了该 Flask 应用程序的 API 接口，涵盖用户管理、项目管理及文档管理等功能。认证采用 JSON Web Tokens (JWT)。

## 目录

1. [认证](#认证)
2. [用户管理](#用户管理)
    - [注册新用户](#注册新用户)
    - [用户登录](#用户登录)
    - [获取所有用户](#获取所有用户)
3. [项目管理](#项目管理)
    - [创建项目](#创建项目)
    - [获取用户项目](#获取用户项目)
    - [删除项目](#删除项目)
    - [修改项目](#修改项目)
4. [文档管理](#文档管理)
    - [列出项目文档](#列出项目文档)
    - [上传文档](#上传文档)
    - [上传实体和关系](#上传实体和关系)
    - [获取文档详情](#获取文档详情)
    - [删除文档](#删除文档)
5. [错误处理](#错误处理)

---

## 认证

API 使用 JWT 进行认证。成功登录后，将返回一个 JWT 令牌，后续需要认证的请求需在请求头中携带该令牌。

---

## 用户管理

### 注册新用户

**接口:** `/api/add_user`

**方法:** `POST`

**描述:** 注册新用户，需提供邮箱和密码。

**请求体:**
```json
{
    "user_email": "user@example.com",
    "user_password": "securepassword"
}
```

**响应:**

- **201 创建成功**
    ```json
    {
        "message": "User added!"
    }
    ```
- **400 请求错误**
    ```json
    {
        "error": "Missing required fields"
    }
    ```
    ```json
    {
        "error": "邮箱已被注册"
    }
    ```
- **500 服务器错误**
    ```json
    {
        "error": "数据库连接失败"
    }
    ```

---

### 用户登录

**接口:** `/api/userLogin`

**方法:** `POST`

**描述:** 用户登录，验证邮箱和密码后返回 JWT 令牌。

**请求体:**
```json
{
    "user_email": "user@example.com",
    "user_password": "securepassword"
}
```

**响应:**

- **200 登录成功**
    ```json
    {
        "success": true,
        "message": "Login Successful!",
        "user_id": "jwt_token_here"
    }
    ```
- **400 请求错误**
    ```json
    {
        "success": false,
        "message": "请求体无效"
    }
    ```
- **401 未授权**
    ```json
    {
        "success": false,
        "message": "用户不存在"
    }
    ```
    ```json
    {
        "success": false,
        "message": "邮箱或密码错误"
    }
    ```
- **500 服务器错误**
    ```json
    {
        "success": false,
        "message": "数据库连接失败"
    }
    ```

---

### 获取所有用户

**接口:** `/api/get_users`

**方法:** `GET`

**描述:** 获取所有注册用户的信息。

**响应:**

- **200 获取成功**
    ```json
    [
        {
            "user_id": 1,
            "user_email": "user1@example.com",
            "user_password": "hashed_password"
        },
        {
            "user_id": 2,
            "user_email": "user2@example.com",
            "user_password": "hashed_password"
        }
        // 更多用户...
    ]
    ```
- **500 服务器错误**
    ```json
    {
        "error": "数据库连接失败"
    }
    ```

---

## 项目管理

### 创建项目

**接口:** `/api/createProject`

**方法:** `POST`

**描述:** 为认证用户创建新项目。

**请求体:**
```json
{
    "user_id": "jwt_token_here",
    "project_name": "项目名称",
    "project_describe": "项目描述"
}
```

**响应:**

- **201 创建成功**
    ```json
    {
        "status": "success",
        "message": "项目创建成功",
        "project_id": 123
    }
    ```
- **400 请求错误**
    ```json
    {
        "status": "error",
        "message": "请提供完整的项目参数"
    }
    ```
- **500 服务器错误**
    ```json
    {
        "status": "error",
        "message": "项目创建失败"
    }
    ```

---

### 获取用户项目

**接口:** `/api/getProject`

**方法:** `GET`

**描述:** 获取认证用户所有项目。

**查询参数:**
- `user_id`: JWT 令牌

**响应:**

- **200 获取成功**
    ```json
    {
        "project-list": [
            {
                "project_id": 1,
                "project_name": "项目1",
                "project_describe": "描述1",
                "project_create": "2023-01-01T12:00:00",
                "project_modify": "2023-01-02T12:00:00"
            },
            // 更多项目...
        ]
    }
    ```
- **400 请求错误**
    ```json
    {
        "project-list": "请提供用户id"
    }
    ```
- **500 服务器错误**
    ```json
    {
        "project-list": "查询错误"
    }
    ```

---

### 删除项目

**接口:** `/api/deleteProject`

**方法:** `DELETE`

**描述:** 删除指定项目。

**请求体:**
```json
{
    "project_id": 123
}
```

**响应:**

- **200 删除成功**
    ```json
    {
        "status": "success",
        "message": "项目删除成功"
    }
    ```
- **400 请求错误**
    ```json
    {
        "status": "error",
        "message": "请提供项目ID"
    }
    ```
- **404 未找到**
    ```json
    {
        "status": "error",
        "message": "项目不存在"
    }
    ```
- **500 服务器错误**
    ```json
    {
        "status": "error",
        "message": "项目删除失败"
    }
    ```

---

### 修改项目

**接口:** `/api/changeProject`

**方法:** `PUT`

**描述:** 更新项目名称和描述。

**请求体:**
```json
{
    "project_id": 123,
    "project_name": "更新后的项目名称",
    "project_describe": "更新后的项目描述"
}
```

**响应:**

- **200 更新成功**
    ```json
    {
        "status": "success",
        "message": "项目修改成功"
    }
    ```
- **400 请求错误**
    ```json
    {
        "status": "error",
        "message": "请提供完整的项目参数"
    }
    ```
- **404 未找到**
    ```json
    {
        "status": "error",
        "message": "项目不存在"
    }
    ```
- **500 服务器错误**
    ```json
    {
        "status": "error",
        "message": "项目修改失败"
    }
    ```

---

## 文档管理

### 列出项目文档

**接口:** `/projects/<project_id>/documents`

**方法:** `GET`

**描述:** 获取指定项目下的所有文档。

**路径参数:**
- `project_id`: 项目ID

**响应:**

- **200 获取成功**
    ```json
    [
        {
            "doc_id": 1,
            "user_id": 1,
            "project_id": 123,
            "doc_name": "文档1",
            "doc_content": "文档内容1",
            "doc_describe": "文档描述1",
            "doc_create": "2023-01-01T12:00:00",
            "doc_modify": "2023-01-02T12:00:00"
        },
        // 更多文档...
    ]
    ```
- **500 服务器错误**
    ```json
    {
        "error": "获取文档失败"
    }
    ```

---

### 上传文档

**接口:** `/projects/<project_id>/documents`

**方法:** `POST`

**描述:** 向指定项目上传新文档。

**路径参数:**
- `project_id`: 项目ID

**请求体:**
```json
{
    "name": "新文档",
    "description": "新文档描述",
    "content": "新文档内容",
    "user_id": "jwt_token_here"
}
```

**响应:**

- **201 创建成功**
    ```json
    {
        "doc_id": 123,
        "project_id": 456,
        "doc_name": "新文档",
        "doc_content": "新文档内容",
        "doc_describe": "新文档描述",
        "doc_create": "2024-04-27",
        "doc_modify": "2024-04-27"
    }
    ```
- **400 请求错误**
    ```json
    {
        "error": "文档名称是必填项"
    }
    ```
- **500 服务器错误**
    ```json
    {
        "error": "上传文档失败"
    }
    ```

---

### 上传实体和关系

**接口:** `/upload`

**方法:** `POST`

**描述:** 上传文档相关的实体、关系及实体类型。

**请求体:**
```json
{
    "user_id": "jwt_token_here",
    "project_id": 123,
    "doc_name": "文档名称",
    "doc_describe": "文档描述",
    "text": "文档全文内容。",
    "entities": [
        {
            "id": "e1",
            "start": 0,
            "end": 10,
            "label": "人名",
            "text": "张三",
            "color": {
                "background": "#FFFFFF",
                "border": "#000000",
                "fill": "#FFEEAA"
            }
        }
        // 更多实体...
    ],
    "relations": [
        {
            "from": "e1",
            "to": "e2",
            "type": "认识",
            "color": "#FF0000"
        }
        // 更多关系...
    ],
    "enti": [
        {
            "label": "人名",
            "number": 1,
            "disabled": false,
            "color": {
                "background": "#FFFFFF",
                "border": "#000000",
                "fill": "#FFEEAA"
            }
        }
        // 更多实体类型...
    ]
}
```

**响应:**

- **201 上传成功**
    ```json
    {
        "message": "Data inserted successfully",
        "doc_id": 123
    }
    ```
- **400 请求错误**
    ```json
    {
        "error": "user_id and project_id are required"
    }
    ```
    ```json
    {
        "error": "Relation references undefined entities: from e1 to e2"
    }
    ```
- **500 服务器错误**
    ```json
    {
        "error": "数据库连接失败"
    }
    ```

---

### 获取文档详情

**接口:** `/get/<doc_id>`

**方法:** `GET`

**描述:** 获取指定文档的详细信息，包括实体、关系及实体类型。

**路径参数:**
- `doc_id`: 文档ID

**响应:**

- **200 获取成功**
    ```json
    {
        "doc_id": 123,
        "user_id": 1,
        "project_id": 456,
        "doc_name": "文档名称",
        "doc_content": "文档全文内容。",
        "doc_describe": "文档描述",
        "doc_create": "2024-04-27T12:00:00",
        "doc_modify": "2024-04-28T12:00:00",
        "entities": [
            {
                "id": "e1",
                "start": 0,
                "end": 10,
                "label": "人名",
                "text": "张三",
                "color": {
                    "background": "#FFFFFF",
                    "border": "#000000",
                    "fill": "#FFEEAA"
                }
            }
            // 更多实体...
        ],
        "relations": [
            {
                "from": 1,
                "to": 2,
                "type": "认识",
                "color": "#FF0000"
            }
            // 更多关系...
        ],
        "enti": [
            {
                "label": "人名",
                "number": 1,
                "disabled": false,
                "color": {
                    "background": "#FFFFFF",
                    "border": "#000000",
                    "fill": "#FFEEAA"
                }
            }
            // 更多实体类型...
        ]
    }
    ```
- **404 未找到**
    ```json
    {
        "error": "Document not found"
    }
    ```
- **500 服务器错误**
    ```json
    {
        "error": "获取文档失败"
    }
    ```

---

### 删除文档

**接口:** `/api/deleteDocument`

**方法:** `DELETE`

**描述:** 删除指定文档。

**请求体:**
```json
{
    "doc_id": 123
}
```

**响应:**

- **200 删除成功**
    ```json
    {
        "status": "success",
        "message": "文档删除成功"
    }
    ```
- **400 请求错误**
    ```json
    {
        "status": "error",
        "message": "请提供文档ID"
    }
    ```
- **404 未找到**
    ```json
    {
        "status": "error",
        "message": "文档不存在"
    }
    ```
- **500 服务器错误**
    ```json
    {
        "status": "error",
        "message": "文档删除失败"
    }
    ```

---

## 错误处理

所有接口会根据请求结果返回相应的 HTTP 状态码和错误信息：

- **200 OK:** 请求成功。
- **201 Created:** 资源创建成功。
- **400 Bad Request:** 请求参数有误或缺失。
- **401 Unauthorized:** 认证失败或权限不足。
- **404 Not Found:** 请求的资源不存在。
- **500 Internal Server Error:** 服务器内部错误。

**错误响应示例:**
```json
{
    "error": "详细错误信息。"
}
```
或
```json
{
    "status": "error",
    "message": "详细错误信息。"
}
```

---

## 备注

- **认证:** 需要认证的接口要求在请求头中携带有效的 JWT 令牌，建议使用 `Authorization: Bearer <token>` 方式传递。
- **数据库:** 应确保 MySQL 数据库正确配置，并且应用程序能够正常连接。
- **密码安全:** 用户密码采用哈希加密存储，确保安全性。
- **CORS:** 跨域资源共享（CORS）已启用，需根据实际需求调整访问权限。
- **日志记录:** 当前仅在控制台输出错误信息，建议在生产环境中使用更完善的日志记录机制。
- **安全性增强:** 
    - 实现输入验证，防止 SQL 注入等安全漏洞。
    - 添加速率限制，防止 API 滥用。

如有疑问或需要进一步帮助，请联系开发团队。
