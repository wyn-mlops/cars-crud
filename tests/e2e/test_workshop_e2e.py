import re
from playwright.sync_api import expect

def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()
    
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()


def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 打开新建页面，创建 Honda Civic 2022
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("White")
    page.get_by_role("button", name="Create car").click()

    # 2. 点击 Edit car 链接
    page.get_by_role("link", name="Edit car").click()

    # 3. 修改型号为 Accord，年份为 2023
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")
    page.get_by_role("button", name="Save changes").click()

    # 4. 断言详情页显示 Honda Accord
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()

    # 5. 刷新页面
    page.reload()

    # 6. 断言刷新后数据依然存在（通过 id 定位元素，PDF 提示用 #car-model 和 #car-year）
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")