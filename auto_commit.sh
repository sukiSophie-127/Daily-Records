#!/bin/bash

# 获取当前日期（格式：YY-M-D）
current_date=$(date +%y-%m-%d)

# 计算前一天的日期
previous_date=$(date -d "yesterday" +%y-%m-%d)

# 执行git命令
git add .
git commit -m "$previous_date"
git push origin main

echo "提交完成！日期: $previous_date"