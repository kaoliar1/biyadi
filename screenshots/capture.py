# -*- coding: utf-8 -*-
"""
移动端 H5 截图脚本（Playwright）
- 移动视口：375 × 812（iPhone 尺寸，2 倍清晰度）
- 自动启动本地静态服务器，依次切换四个 Tab，输出整页截图
运行：
  PLAYWRIGHT_BROWSERS_PATH=<浏览器路径> python3 screenshots/capture.py
"""
import functools
import os
import threading

from playwright.sync_api import sync_playwright

try:
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer
except ImportError:  # py2 fallback，实际不需要
    raise

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(BASE_DIR, "screenshots")
PORT = int(os.environ.get("H5_PORT", "8123"))


def start_server():
    handler = functools.partial(SimpleHTTPRequestHandler, directory=BASE_DIR)
    httpd = TCPServer(("127.0.0.1", PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


def main():
    os.makedirs(SHOTS, exist_ok=True)
    httpd = start_server()
    url = f"http://127.0.0.1:{PORT}/index.html"
    tabs = [
        ("行情走势", "01-kline.png", True),
        ("描述统计", "02-stats.png", True),
        ("收益分布", "03-dist.png", True),
        ("分析过程", "04-process.png", True),
    ]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 375, "height": 812},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
            user_agent=("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                        "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"),
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_selector(".price-card", timeout=15000)

        # 默认首屏（非整页，模拟真实首屏）
        page.wait_for_timeout(1200)
        page.screenshot(path=os.path.join(SHOTS, "00-first-screen.png"))

        for label, fname, full in tabs:
            page.get_by_text(label, exact=True).first.click()
            page.wait_for_timeout(1400)  # 等待图表懒加载/重绘
            page.screenshot(path=os.path.join(SHOTS, fname), full_page=full)
            print("saved", fname)

        browser.close()
    httpd.shutdown()
    print("全部截图完成 ->", SHOTS)


if __name__ == "__main__":
    main()
