from curl_cffi import requests
import time
from datetime import datetime, timedelta
import os

def read_file(file_path):
    """从文件读取 pump 列表"""
    try:
        with open(file_path, 'r') as file:
            pump = [line.strip() for line in file if line.strip()]
        return pump
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def write_file(file_path, data):
    """将 pump_reslut 写入文件"""
    try:
        with open(file_path, 'w') as file:
            for item in data:
                file.write(f"{item}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def handle_file(file_path):
    """
    判断指定文件是否存在，如存在则按行读取内容存入列表；
    如不存在则创建文件并写入字符串 "begin"，然后将该字符串作为列表元素返回。

    参数:
        file_path (str): 文件路径

    返回:
        list: 文件内容按行分割后的列表
    """
    result_list = []
    if os.path.exists(file_path):
        with open(file_path, 'r',encoding='utf-8') as file:
            for line in file:  # 使用 split 方法提取 " " 之前的部分
                parts = line.split(' ')
                if parts:
                    result_list.append(parts[0].strip())  # 去除前后空格
    else:
        with open(file_path, 'w') as file:
            file.write("begin \n")
        result_list = ['begin ']
    
    return result_list

def send_message_via_telegram(bot_token, chat_id, message):
    """Send message to a Telegram group."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Message sent successfully")
    except:
        print(f"Failed to send message")
