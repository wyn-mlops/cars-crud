import re
from playwright.sync_api import expect

def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()
    
    # 等待 URL 跳转到详情页，而不是立刻去查标题
    expect(page).to_have_url(re.compile(r"/cars/\d+$"), timeout=15000)
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible(timeout=15000)

def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 打开新建页面，创建 Honda Civic
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("White")
    page.get_by_role("button", name="Create car").click()
    
    # 2. 点击 Edit car 链接
    expect(page.get_by_role("link", name="Edit car")).to_be_visible(timeout=15000)
    page.get_by_role("link", name="Edit car").click()
    
    # 3. 关键修复：等待表单加载出旧数据，再动手修改（避免页面没准备好就填表单）
    expect(page.get_by_label("Model", exact=True)).to_have_value("Civic", timeout=15000)
    expect(page.get_by_label("Year", exact=True)).to_have_value("2022", timeout=15000)
    
    # 4. 修改数据并点击保存
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")
    page.get_by_role("button", name="Save changes").click()
    
    # 5. 等待 URL 跳转回详情页（证明保存请求已经处理完毕）
    expect(page).to_have_url(re.compile(r"/cars/\d+$"), timeout=15000)
    
    # 6. 断言详情页内容（确保页面已经加载完毕）
    expect(page.locator("#car-model")).to_have_text("Accord", timeout=15000)
    expect(page.locator("#car-year")).to_have_text("2023", timeout=15000)
    
    # 7. 刷新页面验证持久化
    page.reload()
    expect(page.locator("#car-model")).to_have_text("Accord", timeout=15000)
    expect(page.locator("#car-year")).to_have_text("2023", timeout=15000)