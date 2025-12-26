import feedparser
import requests
import os
import time
import json

# 配置参数
TOKEN = os.environ.get('TG_TOKEN')
CHAT_ID = os.environ.get('TG_CHAT_ID')
DB_FILE = "sent_links.txt"
CONFIG_FILE = "feeds.json"

def load_config():
    """从配置文件加载 RSS 列表"""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("feeds", [])
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return []

def load_sent_links():
    """读取已发送过的链接记录"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_sent_link(link):
    """将新发送的链接追加到记录文件"""
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(link + "\n")

def send_tg_message(title, link):
    """发送消息到 Telegram，包含频率限制处理"""
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    # 使用 HTML 格式，标题加粗
    text = f"<b>{title}</b>\n\n{link}"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(api_url, data=payload, timeout=20)
        # 处理 Telegram 的 429 Too Many Requests
        if response.status_code == 429:
            retry_after = response.json().get('parameters', {}).get('retry_after', 10)
            print(f"触发频率限制，等待 {retry_after} 秒...")
            time.sleep(retry_after)
            return requests.post(api_url, data=payload).status_code
        return response.status_code
    except Exception as e:
        print(f"Telegram 发送失败: {e}")
        return None

def main():
    if not TOKEN or not CHAT_ID:
        print("错误: 请确保已设置 TG_TOKEN 和 TG_CHAT_ID 环境变量")
        return

    feeds = load_config()
    sent_links = load_sent_links()
    print(f"已加载 {len(sent_links)} 条历史记录")
    
    for url in feeds:
        print(f"正在抓取: {url}")
        try:
            # 修改了解析逻辑，防止部分 RSS 格式兼容问题
            feed = feedparser.parse(url)
            
            # 倒序处理：从 RSS 中最旧的文章开始推，这样群里显示最新文章在最下面
            for entry in reversed(feed.entries):
                link = entry.link
                
                if link not in sent_links:
                    print(f"发现新文章: {entry.title}")
                    status = send_tg_message(entry.title, link)
                    
                    if status == 200:
                        save_sent_link(link)
                        sent_links.add(link)
                        # 严格避开群组每秒消息限制
                        time.sleep(2.0) 
                    else:
                        print(f"发送失败，状态码: {status}")
                else:
                    # 已推过的文章直接跳过
                    continue
                    
        except Exception as e:
            print(f"抓取源 {url} 时出错: {e}")

if __name__ == "__main__":
    main()
