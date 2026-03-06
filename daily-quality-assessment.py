import math
from datetime import datetime


def parse_time_input(time_str):
    """
    解析用户输入的时间字符串
    格式: "xx-xx-xx" (时-分-秒) 或 "xx-xx" (分-秒)
    返回: 小时数 (float)
    """
    parts = time_str.split("-")
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return hours + minutes / 60 + seconds / 3600
    elif len(parts) == 2:
        minutes = int(parts[0])
        seconds = int(parts[1])
        return minutes / 60 + seconds / 3600
    else:
        raise ValueError("时间格式错误，请使用 xx-xx-xx 或 xx-xx 格式")


def calculate_daily_score(actual_times):
    """
    输入字典格式: {'学习': 6, '工作': 4, '睡眠': 6.5, '其他': 4, '娱乐': 1, '游戏': 1.5, 'L站': 1}
    输出: 0~100 的浮点数
    """
    # 1. 定义标准时间 (从图片识别得出)
    standards = {
        "学习": 2.0,
        "工作": 8.0,
        "睡眠": 6.5,
        "其他": 4.0,
        "娱乐": 1.0,
        "游戏": 1.5,
        "L站": 1.0,
    }

    # 2. 定义权重 (根据价值排序设定)
    weights = {
        "学习": 8.0,
        "工作": 7.0,
        "睡眠": 1.0,
        "其他": -0.2,
        "娱乐": -1.0,
        "游戏": -1.0,
        "L站": -2.0,
    }

    # 3. 计算加权偏移总量 V
    v = 0
    for category, s_time in standards.items():
        x_time = actual_times.get(category, 0)
        v += weights[category] * (x_time - s_time)

    # 4. 映射到 0-100 (Sigmoid)
    # k 控制敏感度，0.15 是经过测试较平衡的值
    k = 0.15
    score = 100 / (1 + math.exp(-k * v))

    return round(score, 2)


# --- 交互输入 ---
categories = ["学习", "工作", "睡眠", "其他", "娱乐", "游戏", "L站"]

print("请输入今日七类时间(格式: xx-xx-xx 或 xx-xx, 时-分-秒或分-秒):")
print("示例: 3-21-12 表示 3小时21分钟12秒, 24-53 表示 24分钟53秒")
print("-" * 50)

actual_times = {}
for category in categories:
    while True:
        user_input = input(f"{category}: ").strip()
        try:
            actual_times[category] = parse_time_input(user_input)
            break
        except ValueError as e:
            print(f"输入错误: {e}，请重新输入")

# --- 计算并输出结果 ---
score = calculate_daily_score(actual_times)
today = datetime.now().strftime("%Y-%m-%d")

print("-" * 50)
print(f"今天是 {today}, 得分是 {score}")

# --- 写入文件 ---
with open("value.txt", "a", encoding="utf-8") as f:
    f.write(f"{today},{score}\n")
