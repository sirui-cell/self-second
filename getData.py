import json
from curl_cffi import requests
import time
from datetime import datetime, timedelta
import os
import config as c

def get_header():
    """返回请求头信息"""
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6,ar;q=0.5,ru;q=0.4,kk;q=0.3,uz;q=0.2,th;q=0.1,mt;q=0.1,da;q=0.1",
        "baggage": "sentry-environment=production,sentry-release=20250806-2043-a5aa1db,sentry-public_key=93c25bab7246077dc3eb85b59d6e7d40,sentry-trace_id=327626096bea4374aaca67faf862e50a,sentry-sample_rate=0.01,sentry-sampled=false",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
        "sec-ch-ua-arch": "\"arm\"",
        "sec-ch-ua-bitness": "\"64\"",
        "sec-ch-ua-full-version": "\"138.0.7204.184\"",
        "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"138.0.7204.184\", \"Google Chrome\";v=\"138.0.7204.184\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-ch-ua-platform-version": "\"15.5.0\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sentry-trace": "327626096bea4374aaca67faf862e50a-b6c23760667a3a70-0",
        "Referer": "https://gmgn.ai/sol/address/3fFt9FLwcDEu4tCoVy7gk96By1XTwNntEo58NqhrKRjk"
    }

def holdings(wallet_address):
    try:
        response = requests.get(c.get_url_holding(wallet_address),headers=get_header(), impersonate="chrome124")
        response.raise_for_status()
        if not response.content:
            print(f"{wallet_address}响应内容为空")
            return None
        data = response.json()
        trades = data['data']['list']   
        if not trades:
            print(f"{wallet_address}没有持仓数据")
            return None
        return trades
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for address {wallet_address}: {http_err}")
        return None  # 返回 None 表示出现错误
    except ValueError as json_err:
        print(f"JSON decode error for address {wallet_address}: {json_err}")
        return None  # 返回 None 表示出现错误
    except Exception as err:
        print(f"An error occurred for address {wallet_address}: {err}")
        return False  # 返回 None 表示出现错误
        
def sol_balance(wallet_address):
    try:
        response = requests.get(c.get_url_balance(wallet_address),headers=get_header(), impersonate="chrome124")
        response.raise_for_status()
        data = response.json()
        if data.get("code") == 0:
            return float(data["data"].get("sol_balance", "0"))
        else:
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

def pump_addresses(url):
    
    try:
        response = requests.get(url,headers=get_header(), impersonate= "chrome124")
        time.sleep(3)
        response.raise_for_status()
        data = response.json()  # 解析JSON响应
        
        if data.get("code") == 0:  # 检查返回的代码是否为0（成功）
            high_market_cap_addresses = [item['address'] for item in data['data']['rank']]           
            return high_market_cap_addresses
        else:
            print(f"Error in response: {data.get('msg')}")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return []
    except Exception as err:
        print(f"Error occurred: {err}")
        return []

def top_traders(pump_token):
    """获取所有 top traders 的 address"""
    try:
        response = requests.get(c.get_url_traders(pump_token),headers=get_header(), impersonate="chrome124")
        time.sleep(3)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析JSON响应
        
        if data.get("code") == 0:  # 检查返回的代码是否为0（成功）
            addresses = [trader['address'] for trader in data['data']['list']]
            return addresses
        else:
            print(f"Error in response: {data.get('msg')}")
            return []
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return []
    except Exception as err:
        print(f"Error occurred: {err}")
        return []

def top_holders(pump_token):
    try:
        response = requests.get(c.get_url_holders(pump_token),headers=get_header(), impersonate="chrome124")
        response.raise_for_status()  # 检查请求是否成功
        time.sleep(3)
        data = response.json()  # 将响应内容解析为 JSON 格式
        
        if data.get("code") == 0:  # 检查返回的代码是否为0（成功）
            addresses = [holder['address'] for holder in data['data']['list']]
            return addresses
        else:
            print(f"Error in response: {data.get('msg')}")
            return []
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return []
    except Exception as err:
        print(f"Error occurred: {err}")
        return []

if __name__ == "__main__":
    pump_addresses_list = pump_addresses(c.url_24h)
    print(f"Pump addresses: {pump_addresses_list[0]}")
    pump_token = '2rcag4mFqDeozcdn9gCtKAX87jCnwqGy31fRjg3upump'
    top_traders_list = top_traders(pump_token)
    print(f"Top traders: {top_traders_list[0]}")
    top_holders_list = top_holders(pump_token)
    print(f"Top holders: {top_holders_list[0]}")
    wallet_addr = top_traders_list[0]
    bal = sol_balance(wallet_addr)
    print(f"Sol balance for {wallet_addr}: {bal}")
