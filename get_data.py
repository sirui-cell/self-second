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

def pump_addresses(url=url_24h):
    
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
