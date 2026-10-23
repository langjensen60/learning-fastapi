'''
Author: langjensen60 langjensen60@gmail.com
Date: 2026-10-22 15:10:03
LastEditors: langjensen60 langjensen60@gmail.com
LastEditTime: 2026-10-22 15:10:17
FilePath: fastapi-learning/.vscode/test_main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "current_user": "admin",
        "skip": 0,
        "limit": 10,
        "message": "成功获取数据",
    }