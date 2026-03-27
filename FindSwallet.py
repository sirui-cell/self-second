import json
from curl_cffi import requests
import time
from datetime import datetime, timedelta
import os
import config as f
import getData as g
import handleFile as h

def ProfitIndicators(wallet_assets):
    # 数据验证
    if not isinstance(wallet_assets, list) or not wallet_assets:
        raise ValueError("wallet_assets 应为非空列表")

    total_assets = 0

    # 初始化指标计数
    high_profit_assets = 0
    winning_assets = 0
    quick_trades = 0
    low_cost_assets = 0

    # 获取当前时间戳
    current_time = int(time.time())
    seven_days_in_seconds = 7 * 24 * 60 * 60  # 7天的秒数

    for asset in wallet_assets:
        try:
            # 解析需要的字段
            total_profit_pnl = float(asset.get("total_profit_pnl", 0))
            history_bought_cost = float(asset.get("history_bought_cost", 0))
            history_bought_amount = float(asset.get("history_bought_amount", 1))  # 防止除以0
            start_holding_at = int(asset.get("start_holding_at", 0))
            end_holding_at = int(asset.get("end_holding_at", 0))

            # 检查资产是否在过去7天内购买
            if (current_time - start_holding_at) > seven_days_in_seconds:
                continue  # 跳过不在7天内购买的资产
            else:
                total_assets += 1

            # 高倍盈利资产
            if total_profit_pnl > 15:
                high_profit_assets += 1

            # 胜率高
            if total_profit_pnl > 0:
                winning_assets += 1

            # 快进快出
            if end_holding_at and (end_holding_at - start_holding_at) < 60:  # 小于3分钟
                quick_trades += 1

            # 资产单位成本价格低
            unit_cost_price = history_bought_cost / history_bought_amount
            if unit_cost_price < 0.0003:
                low_cost_assets += 1

        except (ValueError, TypeError) as e:
            print(f"数据处理错误: {e}，资产数据: {asset}")
            continue  # 跳过当前资产继续处理下一个

    # 计算各项指标
    has_high_profit = high_profit_assets > 0
    winning_ratio = (winning_assets / total_assets) > 0.5 if total_assets > 0 else False
    quick_trade_ratio = (quick_trades / total_assets) < 0.2 if total_assets > 0 else True
    low_cost_ratio = (low_cost_assets / total_assets) > 0.5 if total_assets > 0 else False

    # 检查所有指标是否满足
    if has_high_profit and winning_ratio and quick_trade_ratio and low_cost_ratio:
        return total_assets,high_profit_assets, winning_assets / total_assets
    return False

def isSmartWallet(address):
    url = f'https://gmgn.ai/pf/api/v1/wallet/sol/{address}/holdings?device_id=3e417959-0b07-4169-881d-2e2beb11791f&fp_did=2e0207aac1641053e8c014ed0945c9d0&client_id=gmgn_web_20260105-9509-b9c2d27&from_app=gmgn&app_ver=20260105-9509-b9c2d27&tz_name=Asia%2FShanghai&tz_offset=28800&app_lang=zh-CN&os=web&worker=0&limit=50&order_by=last_active_timestamp&direction=desc&hide_airdrop=true&hide_abnormal=false&hide_closed=false&sellout=true&showsmall=true&tx30d=true'

    try:
        bal = get_sol_balance(address)
        if bal == 0:
            #send_message_via_telegram(BOT_TOKEN, CHAT_ID, f"{address}bal 为 0,不满足\n")
            print(f"{address}bal 为 0,不满足")
            return False
            
        response = requests.get(url, headers=get_header(), impersonate="chrome124")
        response.raise_for_status()  # 检查请求是否成功
        time.sleep(1)  # 适当延迟，避免过度请求
        # 检查响应内容
        if not response.content:
            print(f"{address}响应内容为空")
            return False
        
        data=response.json()

        trades = data['data']['list']   
        if not trades:
            print(f"{address}没有持仓数据")
            return False
        
        all_count = len(trades)
        
        if all_count < 2:
            return False
        

        evaluate = ProfitIndicators(trades)
        return evaluate

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for address {address}: {http_err}")
        return None  # 返回 None 表示出现错误
    except ValueError as json_err:
        print(f"JSON decode error for address {address}: {json_err}")
        return None  # 返回 None 表示出现错误
    except Exception as err:
        print(f"An error occurred for address {address}: {err}")
        return False  # 返回 None 表示出现错误
      
def main():
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"{current_date}_15.txt"
    yesteday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesteday_filename = f"{yesteday_date}_15.txt"
    result_list = f.process_file(yesteday_filename) #读取昨天符合标准的wallets列表
    pump_file_path = "pump.txt"
    #begin 

    f.send_message_via_telegram(BOT_TOKEN, CHAT_ID, 'begin get wallets' + '\n')
    
    #获取满足市值的pump
    while True:
        pump_1h = g.pump_addresses(url_1h)
        pump_24h = g.pump_addresses(url_24h)
        merged_pump = list(set(pump_1h) | set(pump_24h))
        if len(merged_pump) > 0:
            break
        else:
            print('无法获取代币pump，等待15秒再试')
            time.sleep(1)
    for pump in merged_pump:
        while True:
            top_traders_wallets = g.top_traders(pump)
            if len(top_traders_wallets) > 0:
                break
            else:
                print('无法获取代币pump的traders钱包地址，请等待10秒后再试')
                time.sleep(1)
        while True:
            top_holders_wallets = g.top_holders(pump)
            if len(top_holders_wallets) > 0:
                break
            else:
                print('无法获取代币pump的holders钱包地址，请等待10秒后再试')
                time.sleep(1)
                            
        #获取当前pump中的最终wallets
        wallets = list(set(top_traders_wallets) | set(top_holders_wallets))
              
        #检查钱包是否符合设置的标准，符合就输出
        for wallet in wallets:
            if wallet not in result_list:
                i = 0
                while i < 3:
                    pnl = isSmartWallet(wallet)
                    if pnl is not None:
                        break
                    else:
                        print('无法获得指定钱包15天内的胜率情况，请等15秒后再试')
                        i = i+1
                        time.sleep(1)
                print(f'检查{wallet}是否符合标准：{pnl}')
                if pnl:
                    result_list.append(wallet)
                    result = f'{wallet} {pnl}'
                    result_tg = f'https://gmgn.ai/sol/address/{wallet}   {pnl}'
                    f.send_message_via_telegram(BOT_TOKEN, CHAT_ID, result_tg + '\n')
                    print(result)
                    with open(filename, 'a') as file:
                        file.write(result + '\n')
                time.sleep(1)
    f.send_message_via_telegram(BOT_TOKEN, CHAT_ID, 'all done！' + '\n')    
    
if __name__ == "__main__":
    main()
