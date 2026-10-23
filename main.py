from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


# --- 1. 定义数据模型 ---
class Item(BaseModel):
  name: str
  price: float


# --- 2. 模拟数据库与依赖项 1：获取数据库会话 ---
class DatabaseSession:

  def __init__(self):
    print("-> 创建数据库连接")

  def close(self):
    print("-> 关闭数据库连接")


def get_db():
  """依赖项：管理数据库会话的生命周期"""
  db = DatabaseSession()
  try:
    yield db  # 使用 yield 支持在请求结束后执行清理/后置代码
  finally:
    db.close()


# --- 3. 模拟用户认证与依赖项 2：获取当前用户 ---
def get_current_user(token: str = "fake-super-token"):
  """依赖项：解析 Token 并验证用户身份"""
  if token != "fake-super-token":
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的认证凭证"
    )
  # 返回解析出的用户信息
  return {"username": "admin", "role": "superuser"}


# --- 4. 依赖项 3：公共的翻页参数解析类 ---
class CommonQueryParams:

  def __init__(self, skip: int = 0, limit: int = 10):
    self.skip = skip
    self.limit = limit


# --- 5. 路径操作函数：使用 Depends 组合多个依赖 ---
@app.get("/items/")
def read_items(
    # 注入翻页参数（基于类）
    commons: CommonQueryParams = Depends(CommonQueryParams),
    # 注入数据库会话
    db: DatabaseSession = Depends(get_db),
    # 注入当前用户
    current_user: dict = Depends(get_current_user),
):
  # 业务逻辑：可以直接使用注入进来的对象
  return {
      "current_user": current_user["username"],
      "skip": commons.skip,
      "limit": commons.limit,
      "message": "成功获取数据",
  }