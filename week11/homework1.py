import threading
from queue import Queue

"""
作业一：
由 Dijkstra 提出并解决的哲学家就餐问题是典型的同步问题。该问题描述的是五个哲学家共用一张圆桌，分别坐在五张椅子上，在圆桌上有五个盘子和五个叉子，
他们的生活方式是交替的进行思考和进餐，思考时不能用餐，用餐时不能思考。平时，一个哲学家进行思考，饥饿时便试图用餐，
只有在他同时拿到他的盘子左右两边的两个叉子时才能进餐。进餐完毕后，他会放下叉子继续思考（关于哲学家就餐问题更详细的描述，
请参考本节的 PDF 附件，里面有维基百科中的具体描述）。
请写出代码来解决如上的哲学家就餐问题，要求代码返回“当每个哲学家分别需要进食 n 次”时这五位哲学家具体的行为记录（具体需要记录哪些行为，请参考下面的代码）。

# 示例代码
import threading
class DiningPhilosophers:
   def __init__(self):
   pass
# philosopher 哲学家的编号。
# pickLeftFork 和 pickRightFork 表示拿起左边或右边的叉子。
# eat 表示吃面。
# putLeftFork 和 putRightFork 表示放下左边或右边的叉子。
   def wantsToEat(self,
      philosopher,
      pickLeftFork(),
      pickRightFork(),
      eat(),
      putLeftFork(),
      putRightFork())
测试用例：
输入：n = 1 （1<=n<=60，n 表示每个哲学家需要进餐的次数。）
预期输出：
[[4,2,1],[4,1,1],[0,1,1],[2,2,1],[2,1,1],[2,0,3],[2,1,2],[2,2,2],[4,0,3],[4,1,2],[0,2,1],[4,2,2],[3,2,1],[3,1,1],[0,0,3],[0,1,2],[0,2,2],[1,2,1],[1,1,1],[3,0,3],[3,1,2],[3,2,2],[1,0,3],[1,1,2],[1,2,2]]
解释:
输出列表中的每一个子列表描述了某个哲学家的具体行为，它的格式如下：
output[i] = [a, b, c] (3 个整数)
a 哲学家编号。
b 指定叉子：{1 : 左边, 2 : 右边}.
c 指定行为：{1 : 拿起, 2 : 放下, 3 : 吃面}。
如 [4,2,1] 表示 4 号哲学家拿起了右边的叉子。所有自列表组合起来，就完整描述了“当每个哲学家分别需要进食 n 次”时这五位哲学家具体的行为记录。

代码思路：
1，总共有5个叉子，一个哲学家进食需要两个叉子，也就是一次只能同时有两个哲学家进食，再加一个哲学家会引起线程阻塞问题
2，把5个叉子放进queue，控制每个迭代最多同时2个哲学家同时进食，一个循环为所有哲学家进食一次，把哲学家进食行为放入queue中保存
"""


class DiningPhilosophers(threading.Thread):
    def __init__(self, philosopher, fork_queue, behavior_queue):
        super().__init__()
        self.lock = threading.Lock()
        self.philosopher = philosopher
        self.queue = fork_queue
        self.behavior_queue = behavior_queue
        self.exp_eat_time = 0
        self.has_fork = {"左边": 0, "右边": 0, "吃面": 0}
        self.left_fork = ""
        self.right_fork = ""

    def run(self):
        while True:
            if self.has_fork["左边"] == 0 and self.has_fork["吃面"] == 0:
                self.pick(self.pick_left_fork)
                self.has_fork["左边"] = 1
            elif self.has_fork["右边"] == 0 and self.has_fork["吃面"] == 0:
                self.pick(self.pick_right_fork)
                self.has_fork["右边"] = 1
            elif self.has_fork["吃面"] == 0:
                self.eat()
                self.has_fork["吃面"] = 1
            elif self.has_fork["左边"] == 1:
                self.put(self.put_left_fork, self.left_fork)
                self.has_fork["左边"] = 0
            elif self.has_fork["右边"] == 1:
                self.put(self.put_right_fork, self.right_fork)
                self.has_fork["右边"] = 0
            else:
                self.has_fork["左边"] = 0
                self.has_fork["右边"] = 0
                self.has_fork["吃面"] = 0
                break

    @classmethod
    def get_fork(cls, side):
        return {"左边": 1, "右边": 2}[side]

    @classmethod
    def get_behavior(cls, behavior):
        return {"拿起": 1, "放下": 2, "吃面": 3}[behavior]

    def pick(self, pick_fork):
        behavior = []
        behavior.append(self.philosopher)
        behavior.append(self.get_fork(pick_fork()))
        behavior.append(self.get_behavior("拿起"))
        self.behavior_queue.put(behavior)

    def pick_left_fork(self):
        self.lock.acquire()
        while True:
            if self.queue.qsize() >= 2:
                try:
                    self.left_fork = self.queue.get(False)
                    print(f"{self.philosopher} had pick the left fork{self.left_fork}.\n")
                    break
                except Exception as e:
                    print(f"fork queue is empty[{e}], pls continue")
        self.lock.release()

        return "左边"

    def pick_right_fork(self):
        self.lock.acquire()
        while True:
            if self.queue.qsize() >= 2:
                try:
                    self.right_fork = self.queue.get(False)
                    print(f"{self.philosopher} had pick the right fork{self.right_fork}.\n")
                    break
                except Exception as e:
                    print(f"fork queue is empty[{e}], pls continue")
        self.lock.release()

        return "右边"

    def put(self, put_fork, fork):
        action, side = put_fork(fork)
        behavior = []
        behavior.append(self.philosopher)
        behavior.append(self.get_fork(side))
        behavior.append(self.get_behavior(action))
        self.behavior_queue.put(behavior)

    def put_left_fork(self, fork):
        print(f"{self.philosopher} is putting the left fork{fork}.\n")
        self.queue.put(fork)
        return "放下", "左边"

    def put_right_fork(self, fork):
        print(f"{self.philosopher} is putting the right fork{fork}.\n")
        self.queue.put(fork)
        return "放下", "右边"

    def eat(self):
        print(f"{self.philosopher} is eating noodles.\n")
        behavior = []
        behavior.append(self.philosopher)
        behavior.append(0)
        behavior.append(self.get_behavior("吃面"))
        self.behavior_queue.put(behavior)
        self.exp_eat_time += 1


if __name__ == "__main__":
    # 初始化叉子队列（5个叉子）
    fork_queue = Queue(5)
    for i in range(5):
        fork_queue.put(i)

    # 多线程执行哲学家进食行为
    behavior_queue = Queue()
    eat_time = 3  # 进食次数
    for _ in range(eat_time):
        philosopher_threads = []
        philosopher_name_list = ['philosopher_1', 'philosopher_2', 'philosopher_3', 'philosopher_4', 'philosopher_5']
        for name in philosopher_name_list:
            thread = DiningPhilosophers(name, fork_queue, behavior_queue)
            philosopher_threads.append(thread)

        # 启动前两个线程，并等待其结束
        [t.start() for t in philosopher_threads[:2]]
        # 等待前两个线程结束
        [t.join() for t in philosopher_threads[:2]]

        # 启动中间两个线程，并等待其结束
        [t.start() for t in philosopher_threads[2:4]]
        [t.join() for t in philosopher_threads[2:4]]

        # 启动最后一个线程
        philosopher_threads[-1].start()
        philosopher_threads[-1].join()

    # 展示哲学家行为数据
    behavior_list = []
    while not behavior_queue.empty():
        behavior_list.append(behavior_queue.get(False))
    print(f"{behavior_list}")
