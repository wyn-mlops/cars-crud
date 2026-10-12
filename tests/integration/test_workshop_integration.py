from app import database
from app.schemas import CarInput

def test_saved_car_can_be_read_from_sqlite(database_path):
    database.initialize(database_path)
    saved = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue"),
    )
    loaded = database.get_car(database_path, saved.id)

    assert loaded is not None
    assert loaded.id == saved.id
    assert loaded.make == "Toyota"
    assert loaded.year == 2020
def test_deleting_one_car_keeps_the_other(database_path):
    # 1. 初始化一个全新的 SQLite 数据库
    database.initialize(database_path)

    # 2. 创建第一辆车 (Toyota)
    first_car = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Corolla", year=2021, color="White")
    )

    # 3. 创建第二辆车 (Honda)
    second_car = database.create_car(
        database_path,
        CarInput(make="Honda", model="Civic", year=2022, color="Black")
    )

    # 4. 只删除第一辆车
    database.delete_car(database_path, first_car.id)

    # 5. 断言：第一辆车确实找不到（被删掉了）
    assert database.get_car(database_path, first_car.id) is None

    # 6. 断言：第二辆车还在数据库里
    loaded_second = database.get_car(database_path, second_car.id)
    assert loaded_second is not None
    assert loaded_second.make == "Honda"

    # 7. 断言：数据库列表里只剩下一辆车，并且是刚才的第二辆
    all_cars = database.list_cars(database_path)
    assert len(all_cars) == 1
    assert all_cars[0].id == second_car.id
    assert all_cars[0].make == "Honda"