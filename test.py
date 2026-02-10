from pubsub import pub

# 1. 定义消息接收函数 (订阅者)
def listener_data1(message, data):
    print(f"1 收到消息: {message}, 数据: {data}")

def listener_data2(message, data):
    print(f"2 收到消息: {message}, 数据: {data}")
# 2. 订阅主题 (主题名为 'data_topic')
pub.subscribe(listener_data1, 'data_topic')
pub.subscribe(listener_data2, 'data_topic')

# 3. 发布消息 (发布者)
# 'data_topic' 为主题，后面的参数会被传递给订阅者函数
pub.sendMessage('data_topic', message="Hello", data=123)
