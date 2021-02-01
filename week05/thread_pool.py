from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED
import time


def get_html(times):
    time.sleep(times)
    # print(f'get page {times} success')
    return times


# 单个线程提交
# executor = ThreadPoolExecutor(max_workers=2)
# task1 = executor.submit(get_html, (3))
# task2 = executor.submit(get_html, (2))
# print(task1.done())
# time.sleep(4)
# print(task1.done())
# print(task1.result())

# 批量线程提交(谁先完成，就先yeld谁)
# executor = ThreadPoolExecutor(max_workers=2)
# urls = [3, 2, 4]
# all_task = [executor.submit(get_html, (url)) for url in urls]
# for future in as_completed(all_task):
#     data = future.result()
#     print(f"get {data} page success")
# wait(all_task, return_when=FIRST_COMPLETED) # 当第一个线程完成时往下进行，默认是等待所有线程完成才往下进场

# 批量线程通过map提交(map里面把future.result()也给执行了)
executor = ThreadPoolExecutor(max_workers=2)
urls = [3, 2, 4]
for data in executor.map(get_html, urls):   # 把urls的每一个值传给 get_html 去执行，且安urls的顺序返回值
    print(f"get {data} page success")
