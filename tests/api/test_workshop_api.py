def test_post_car_returns_201_and_json(client):
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 2018,
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)

    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"



def test_invalid_year_is_not_saved(client):
    # 1. 发送一个年份为 1800 的无效请求
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 1800,  # 故意使用无效年份
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)

    # 2. 断言：API 应该拒绝并返回 422 状态码（验证错误）
    assert response.status_code == 422

    # 3. 发送 GET 请求，断言数据库里确实是空的，没有保存进去
    response_get = client.get("/api/cars")
    assert response_get.json() == []