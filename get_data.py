import json
from curl_cffi import requests
import time
from datetime import datetime, timedelta
import os

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

def sol_balance(wallet_address):
    url = f"https://gmgn.ai/defi/quotation/v1/smartmoney/sol/walletNew/{wallet_address}"

    try:
        response = requests.get(url,headers=get_header(), impersonate="chrome124")
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
    url = f'https://gmgn.ai/vas/api/v1/token_traders/sol/{pump_token}?device_id=da3364a3-2401-4a0f-a831-5482badd4a9b&fp_did=4e26fa883280531007b76beddc66924b&client_id=gmgn_web_20250921-4228-b63b95b&from_app=gmgn&app_ver=20250921-4228-b63b95b&tz_name=Asia%2FShanghai&tz_offset=28800&app_lang=zh-CN&os=web&limit=100&orderby=profit&direction=desc'
    
    try:
        response = requests.get(url,headers=get_header(), impersonate="chrome124")
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
    url = f'https://gmgn.ai/vas/api/v1/token_holders/sol/{pump_token}?device_id=da3364a3-2401-4a0f-a831-5482badd4a9b&fp_did=4e26fa883280531007b76beddc66924b&client_id=gmgn_web_20250921-4228-b63b95b&from_app=gmgn&app_ver=20250921-4228-b63b95b&tz_name=Asia%2FShanghai&tz_offset=28800&app_lang=zh-CN&os=web&limit=100&cost=20&orderby=amount_percentage&direction=desc'
    
    try:
        response = requests.get(url,headers=get_header(), impersonate="chrome124")
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
    wallet_addr= ''
    url = 'https://gmgn.ai/api/v1/rank/sol/swaps/24h?device_id=3e417959-0b07-4169-881d-2e2beb11791f&fp_did=2e0207aac1641053e8c014ed0945c9d0&client_id=gmgn_web_20260306-11434-42d387e&from_app=gmgn&app_ver=20260306-11434-42d387e&tz_name=Asia%2FShanghai&tz_offset=28800&app_lang=zh-CN&os=web&worker=0&orderby=creation_timestamp&direction=desc&filters[]=renounced&filters[]=frozen'
    pump_token = 'AxeAwYdjkBGwSZtKyA9eAWoAyqGE9bj575fLYqF85qxJ'
    #bal = sol_balance(wallet_addr)
    #print(f"Sol balance for {wallet_addr}: {bal}")
    pump_addresses_list = pump_addresses(url)
    print(f"Pump addresses: {pump_addresses_list[0]}")
    #top_traders_list = top_traders(pump_token)
    #print(f"Top traders: {top_traders_list[0]}")
    #top_holders_list = top_holders(pump_token)
    #print(f"Top holders: {top_holders_list[0]}")
