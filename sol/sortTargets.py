import MN_API as mn
import sys
from datetime import datetime, timedelta

# Telegram Bot 配置（可提取到配置文件或环境变量中）
BOT_TOKEN = "YOUR_BOT_TOKEN"  # 请替换为您的 Bot Token
CHAT_ID = -1002604809472

def parse_file(filename):
    wallet_dict = {}

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # 分割 wallet 和括号内容
                parts = line.split(' ', 1)
                if len(parts) < 2:
                    continue

                wallet = parts[0]
                content = parts[1].strip('()')

                values = [v.strip() for v in content.split(',')]
                if len(values) != 3:
                    continue

                try:
                    count_total = int(values[0])
                    count_five = int(values[1])
                    one_rate = float(values[2])  # 确保将胜率解析为浮点数
                except ValueError as e:
                    print(f"数据解析错误：{values} - {e}")
                    continue

                # 只保留第一次出现的钱包地址
                if wallet not in wallet_dict:
                    wallet_dict[wallet] = (count_total, count_five, one_rate)

        return wallet_dict

    except FileNotFoundError:
        print(f"错误：文件 {filename} 未找到。")
        return None
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None


def main(filename=None):
    if filename is None:
        current_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        filename = f"{current_date}_15.txt"

    print(f"正在处理文件：{filename}")

    wallet_dict = parse_file(filename)
    if wallet_dict is None:
        return

    # 按 one_rate 从高到低排序
    sorted_wallets = sorted(
        wallet_dict.items(),
        key=lambda item: item[1][2],  # 按 one_rate 排序
        reverse=True
    )

    # 构建输出内容
    output_lines = [f"{wallet} ({data[0]}, {data[1]}, {data[2]})" 
                    for wallet, data in sorted_wallets]
    output_url = [f"https://gmgn.ai/sol/address/{wallet}" 
                    for wallet, data in sorted_wallets]
    url_filename = filename.replace('_15.txt', '_url.txt')
    # 写入文件
    mn.write_file(filename, output_lines)
    mn.write_file(url_filename, output_url)

    # 可选：发送到 Telegram（取消注释即可启用）
    # for line in output_lines:
    #     mn.send_message_via_telegram(BOT_TOKEN, CHAT_ID, line)
    #     time.sleep(2)

if __name__ == "__main__":
    # 检查是否传入了文件名参数
    if len(sys.argv) > 1:
        file_to_process = sys.argv[1]
    else:
        file_to_process = None

    main(file_to_process)
