前端默认登录用户为123456@qq.com 123456 换了 npm 源之后可以直接在 front 里输入 npm install 安装依赖 并输入 npm run dev 运行 如果不想使用云端服务可以将 axios 文件夹里的 axios 的 api 改成本地的 back 为后端 front 为前端

# API 文档

本文档详细介绍了该 Flask 应用程序的所有 API 接口，涵盖用户管理、项目管理、文档管理、实体管理及关系管理等功能。认证采用 JSON Web Tokens (JWT)。

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
   - [更新文档](#更新文档)
5. [实体管理](#实体管理)
   - [删除实体及相关关系](#删除实体及相关关系)
   - [添加实体类型](#添加实体类型)
   - [更新实体类型](#更新实体类型)
6. [关系管理](#关系管理)
   - [分析关系](#分析关系)
   - [添加关系类型](#添加关系类型)
   - [删除关系类型及其关联实例](#删除关系类型及其关联实例)
   - [添加关系实例](#添加关系实例)
   - [删除关系实例](#删除关系实例)
   - [更新关系类型计数](#更新关系类型计数)
7. [错误处理](#错误处理)
8. [备注](#备注)

---

## 认证

API 使用 JWT 进行认证。成功登录后，将返回一个 JWT 令牌，后续需要认证的请求需在请求头中携带该令牌，格式为 `Authorization: Bearer <token>`。

---

## 用户管理

### 注册新用户

**接口**: `/api/add_user`

**方法**: `POST`

**描述**: 注册新用户，需提供邮箱和密码。

**请求体**:

```json
{
  "user_email": "user@example.com",
  "user_password": "securepassword"
}
```

**响应**:

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

### 用户登录

**接口**: `/api/userLogin`

**方法**: `POST`

**描述**: 用户登录，验证邮箱和密码后返回 JWT 令牌。

**请求体**:

```json
{
  "user_email": "user@example.com",
  "user_password": "securepassword"
}
```

**响应**:

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

### 获取所有用户

**接口**: `/api/get_users`

**方法**: `GET`

**描述**: 获取所有注册用户的信息。

**响应**:

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

**接口**: `/api/createProject`

**方法**: `POST`

**描述**: 为认证用户创建新项目。

**请求体**:

```json
{
  "user_id": "jwt_token_here",
  "project_name": "项目名称",
  "project_describe": "项目描述"
}
```

**响应**:

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

### 获取用户项目

**接口**: `/api/getProject`

**方法**: `GET`

**描述**: 获取认证用户所有项目。

**查询参数**:

- `user_id`: JWT 令牌

**响应**:

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
      }
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

### 删除项目

**接口**: `/api/deleteProject`

**方法**: `DELETE`

**描述**: 删除指定项目。

**请求体**:

```json
{
  "project_id": 123
}
```

**响应**:

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

### 修改项目

**接口**: `/api/changeProject`

**方法**: `PUT`

**描述**: 更新项目名称和描述。

**请求体**:

```json
{
  "project_id": 123,
  "project_name": "更新后的项目名称",
  "project_describe": "更新后的项目描述"
}
```

**响应**:

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

**接口**: `/projects/<project_id>/documents`

**方法**: `GET`

**描述**: 获取指定项目下的所有文档。

**路径参数**:

- `project_id`: 项目 ID

**请求头**:

- `Authorization: Bearer <token>`

**响应**:

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
    }
    // 更多文档...
  ]
  ```

- **403 权限不足或项目不存在**

  ```json
  {
    "error": "Permission denied or project not found"
  }
  ```

- **500 服务器错误**

  ```json
  {
    "error": "获取文档失败"
  }
  ```

### 上传文档

**接口**: `/projects/<project_id>/documents`

**方法**: `POST`

**描述**: 向指定项目上传新文档。

**路径参数**:

- `project_id`: 项目 ID

**请求体**:

```json
{
  "name": "新文档",
  "description": "新文档描述",
  "content": "新文档内容",
  "user_id": "jwt_token_here"
}
```

**响应**:

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

- **403 权限不足或项目不存在**

  ```json
  {
    "error": "Permission denied or project not found"
  }
  ```

- **500 服务器错误**

  ```json
  {
    "error": "上传文档失败"
  }
  ```

### 上传实体和关系

**接口**: `/upload`

**方法**: `POST`

**描述**: 上传文档相关的实体、关系及实体类型。

**请求体**:

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

**响应**:

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

### 获取文档详情

**接口**: `/get/<doc_id>`

**方法**: `GET`

**描述**: 获取指定文档的详细信息，包括实体、关系及实体类型。

**路径参数**:

- `doc_id`: 文档 ID

**响应**:

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
    ],
    "relation_types": [
      {
        "id": 1,
        "type": "认识",
        "start_label": "人名",
        "end_label": "地点",
        "number": 2,
        "color": "#FF0000"
      }
      // 更多关系类型...
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

### 删除文档

**接口**: `/api/deleteDocument`

**方法**: `DELETE`

**描述**: 删除指定文档及其相关数据。

**请求体**:

```json
{
  "doc_id": 123
}
```

**响应**:

- **200 删除成功**

  ```json
  {
    "status": "success",
    "message": "文档及相关数据删除成功",
    "deleted": {
      "relations_deleted": 5,
      "entities_deleted": 10,
      "entity_classes_deleted": 3,
      "relation_types_deleted": 2,
      "document_deleted": 1
    }
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

### 更新文档

**接口**: `/update_document`

**方法**: `POST`

**描述**: 更新指定文档的内容。

**请求体**:

```json
{
  "doc_id": 123,
  "doc_content": "更新后的文档内容"
}
```

**响应**:

- **200 更新成功**

  ```json
  {
    "message": "Document updated successfully",
    "document": {
      "doc_id": 123,
      "user_id": 1,
      "project_id": 456,
      "doc_name": "文档名称",
      "doc_content": "更新后的文档内容",
      "doc_describe": "文档描述",
      "doc_create": "2024-04-27T12:00:00",
      "doc_modify": "2024-04-28T12:00:00"
    }
  }
  ```

- **400 请求错误**

  ```json
  {
    "error": "doc_id is required"
  }
  ```

  ```json
  {
    "error": "doc_content is required"
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
    "error": "查询错误: ...",
    "error": "数据库连接失败"
  }
  ```

---

## 实体管理

### 删除实体及相关关系

**接口**: `/delete_entity`

**方法**: `POST`

**描述**: 删除指定实体及其相关关系。

**请求体**:

```json
{
  "entity_id": 456,
  "doc_id": 123
}
```

**响应**:

- **200 删除成功**

  ```json
  {
    "status": "success",
    "message": "实体及相关关系删除成功"
  }
  ```

- **400 请求错误**

  ```json
  {
    "status": "error",
    "message": "实体ID不能为空"
  }
  ```

- **404 未找到**

  ```json
  {
    "status": "error",
    "message": "实体不存在"
  }
  ```

- **500 服务器错误**

  ```json
  {
    "status": "error",
    "message": "数据库操作失败"
  }
  ```

### 添加实体类型

**接口**: `/add_enti`

**方法**: `POST`

**描述**: 添加新的实体类型。

**请求体**:

```json
{
  "doc_id": 123,
  "label": "组织",
  "color": {
    "background": "#FFFFFF",
    "border": "#000000",
    "fill": "#FFEEAA"
  }
}
```

**响应**:

- **201 添加成功**

  ```json
  {
    "status": "success",
    "message": "关系类新增成功",
    "relation_id": 789
  }
  ```

- **400 请求错误**

  ```json
  {
    "status": "error",
    "message": "缺少必要参数"
  }
  ```

- **500 服务器错误**

  ```json
  {
    "status": "error",
    "message": "数据库操作失败"
  }
  ```

### 更新实体类型

**接口**: `/update_enti`

**方法**: `PUT`

**描述**: 更新实体类型的数量。

**请求体**:

```json
{
  "doc_id": 123,
  "label": "人名",
  "number": 5
}
```

**响应**:

- **200 更新成功**

  ```json
  {
    "status": "success",
    "message": "实体更新成功",
    "updated_id": 123
  }
  ```

- **400 请求错误**

  ```json
  {
    "status": "error",
    "message": "ID 和标签是必填项"
  }
  ```

- **404 未找到**

  ```json
  {
    "status": "error",
    "message": "实体不存在或未更新"
  }
  ```

- **500 服务器错误**

  ```json
  {
    "status": "error",
    "message": "数据库操作失败"
  }
  ```

---

## 关系管理

### 分析关系

**接口**: `/analyze_relation`

**方法**: `POST`

**描述**: 分析文档中的关系并存储到数据库。

**请求体**:

```json
{
  "doc_id": 123,
  "doc_content": "文档内容...",
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
  "relation_types": [
    {
      "type": "认识",
      "start_label": "人名",
      "end_label": "地点",
      "color": "#FF0000"
    }
    // 更多关系类型...
  ]
}
```

**响应**:

- **200 分析成功**

  ```json
  {
    "relations": [
      {
        "from": 1,
        "to": 2,
        "type": "认识",
        "color": "#FF0000"
      }
      // 更多关系...
    ],
    "relation_types": [
      {
        "type": "认识",
        "start_label": "人名",
        "end_label": "地点",
        "color": "#FF0000",
        "number": 3
      }
      // 更多关系类型...
    ]
  }
  ```

- **400 请求错误**

  ```json
  {
    "error": "无效输入，请提供'doc_content'和'entities'字段。"
  }
  ```

- **500 服务器错误**

  ```json
  {
    "error": "发生意外错误。",
    "details": "详细错误信息。"
  }
  ```

### 添加关系类型

**接口**: `/add_relation`

**方法**: `POST`

**描述**: 添加新的关系类型。

**请求体**:

```json
{
  "doc_id": 123,
  "start_label": "人物",
  "end_label": "地点",
  "type": "到达",
  "color": "#92c9d7"
}
```

**响应**:

- **201 添加成功**

  ```json
  {
    "status": "success",
    "message": "关系类新增成功",
    "relation_id": 456
  }
  ```

- **400 请求错误**

  ```json
  {
    "status": "error",
    "message": "缺少必要参数"
  }
  ```

- **500 服务器错误**

  ```json
  {
    "status": "error",
    "message": "数据库操作失败"
  }
  ```

### 删除关系类型及其关联实例

**接口**: `/relations/<relation_type>`

**方法**: `DELETE`

**描述**: 删除指定关系类型及其所有关联的关系实例。

**路径参数**:

- `relation_type`: 关系类型名称

**查询参数**:

- `doc_id`: 文档 ID

**响应**:

- **200 删除成功**

  ```json
  {
    "status": "success",
    "message": "关系类和相关关系实例删除成功"
  }
  ```

- **400 请求错误**

  ```json
  {
    "status": "error",
    "message": "缺少 doc_id 参数"
  }
  ```

- **404 未找到**

  ```json
  {
    "error": "Relation with type ... does not exist."
  }
  ```

- **500 服务器错误**

  ```json
  {
    "status": "error",
    "message": "删除失败: 详细错误信息"
  }
  ```

### 添加关系实例

**接口**: `/relations/instances`

**方法**: `POST`

**描述**: 添加新的关系实例。

**请求体**:

```json
{
  "doc_id": 123,
  "from_entity_id": 1,
  "to_entity_id": 2,
  "type": "认识",
  "color": "#FF0000"
}
```

**响应**:

- **201 添加成功**

  ```json
  {
    "status": "success",
    "message": "关系实例新增成功",
    "id": 789
  }
  ```

- **400 请求错误**

  ```json
  {
    "status": "error",
    "message": "缺少必要参数"
  }
  ```

- **500 服务器错误**

  ```json
  {
    "status": "error",
    "message": "数据库操作失败"
  }
  ```

### 删除关系实例

**接口**: `/relations/instances/<relation_id>`

**方法**: `DELETE`

**描述**: 删除指定的关系实例。

**路径参数**:

- `relation_id`: 关系实例的唯一 ID

**查询参数**:

- `doc_id`: 文档 ID

**响应**:

- **200 删除成功**

  ```json
  {
    "status": "success",
    "message": "Relation 123 deleted successfully."
  }
  ```

- **400 请求错误**

  ```json
  {
    "error": "doc_id is required"
  }
  ```

- **404 未找到**

  ```json
  {
    "error": "Relation with id 123 does not exist in document 456."
  }
  ```

- **500 服务器错误**

  ```json
  {
    "error": "数据库错误: 详细错误信息"
  }
  ```

### 更新关系类型计数

**接口**: `/update_relation_types`

**方法**: `PUT`

**描述**: 更新关系类型的数量，支持增加或减少。

**请求体**:

```json
{
  "type": "认识",
  "increment": true
}
```

**响应**:

- **200 更新成功**

  ```json
  {
    "status": "success",
    "message": "更新成功",
    "affected_rows": 1
  }
  ```

- **400 请求错误**

  ```json
  {
    "status": "error",
    "message": "缺少必要参数"
  }
  ```

- **404 未找到**

  ```json
  {
    "status": "error",
    "message": "未找到对应的关系类型"
  }
  ```

- **500 服务器错误**

  ```json
  {
    "status": "error",
    "message": "数据库操作失败"
  }
  ```

---

## 错误处理

所有接口会根据请求结果返回相应的 HTTP 状态码和错误信息：

- **200 OK**: 请求成功。
- **201 Created**: 资源创建成功。
- **400 Bad Request**: 请求参数有误或缺失。
- **401 Unauthorized**: 认证失败或权限不足。
- **403 Forbidden**: 权限不足。
- **404 Not Found**: 请求的资源不存在。
- **500 Internal Server Error**: 服务器内部错误。

**错误响应示例**:

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

- **认证**: 需要认证的接口要求在请求头中携带有效的 JWT 令牌，建议使用 `Authorization: Bearer <token>` 方式传递。
- **数据库**: 应确保 MySQL 数据库正确配置，并且应用程序能够正常连接。
- **密码安全**: 用户密码采用哈希加密存储，确保安全性。
- **CORS**: 跨域资源共享（CORS）已启用，需根据实际需求调整访问权限。
- **日志记录**: 当前仅在控制台输出错误信息，建议在生产环境中使用更完善的日志记录机制。
- **安全性增强**:
  - 实现输入验证，防止 SQL 注入等安全漏洞。
  - 添加速率限制，防止 API 滥用。

如有疑问或需要进一步帮助，请联系开发团队。
