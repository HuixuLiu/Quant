import websocket
import json
from datetime import datetime
import threading
import time

# ⚠️ 设置币种和阈值
SYMBOL = "btcusdt"
PRICE_THRESHOLD = 70000  # 例如超过70000报警
VOLUME_THRESHOLD = 500   # 例如一分钟成交量大于500报警

class BTCMonitor:
    def __init__(self):
        self.ws = None
        self.running = False
        
    def on_message(self, ws, message):
        data = json.loads(message)
        kline = data['k']
        price = float(kline['c'])      # 当前价格（收盘价）
        volume = float(kline['v'])     # 当前K线的成交量
        ts = datetime.fromtimestamp(kline['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{ts}] Price: {price:.2f}, Volume: {volume:.2f}")
        
        if price > PRICE_THRESHOLD or volume > VOLUME_THRESHOLD:
            self.send_alert(price, volume)
    
    def on_open(self, ws):
        print("✅ WebSocket连接已建立")
        payload = {
            "method": "SUBSCRIBE",
            "params": [f"{SYMBOL}@kline_1m"],
            "id": 1
        }
        ws.send(json.dumps(payload))
    
    def on_close(self, ws, close_status_code, close_msg):
        print("❌ WebSocket连接已关闭")
    
    def on_error(self, ws, error):
        print(f"❌ WebSocket错误: {error}")
    
    def send_alert(self, price, volume):
        # 这里先打印，后面接 Telegram、邮件、钉钉都可以
        print(f"🚨 报警：价格={price}, 成交量={volume}")
    
    def start(self):
        """启动监控"""
        self.running = True
        url = f"wss://stream.binance.com:9443/ws/{SYMBOL}@kline_1m"
        self.ws = websocket.WebSocketApp(url,
                                        on_open=self.on_open,
                                        on_message=self.on_message,
                                        on_close=self.on_close,
                                        on_error=self.on_error)
        
        print("🚀 开始监控BTC价格...")
        print("💡 要停止监控，请运行 monitor.stop()")
        self.ws.run_forever()
    
    def stop(self):
        """停止监控"""
        self.running = False
        if self.ws:
            self.ws.close()
        print("⏹️ 监控已停止")

# 使用方法：
# 1. 创建监控实例

# 2. 在一个新的 cell 中启动监控（这会开始无限循环）
# monitor.start()

# 3. 在另一个 cell 中停止监控
# monitor.stop()

print("监控器已准备就绪！")
print("运行 monitor.start() 开始监控")
print("运行 monitor.stop() 停止监控")


if __name__ == "__main__":
monitor = BTCMonitor()
monitor.start()