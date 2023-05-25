def process_data():
    progress = 0
    
    # 進行一些初始化工作...
    print("test")
    while progress < 100:
        # 執行處理步驟...
        
        # 更新進度
        progress += 10
        
        # 產生進度值
        yield progress
    
    # 完成處理工作，返回最終結果
    result = "處理結果"
    yield (result, "1111")

# 使用生成器函式
generator = process_data()

# 逐步獲取進度值
for value in generator:
    print(value)

result = value
print( result )
# 獲取最終結果
