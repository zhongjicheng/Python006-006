作业三：请用自己的语言描述如下问题：

在你目前的工作场景中，哪个业务适合使用 rabbitmq？ 引入 rabbitmq 主要解决什么问题?（非相关工作可以以设计淘宝购物和结账功能为例来描述）
如何避免消息重复投递或重复消费？
交换机 fanout、direct、topic 有什么区别？
架构中引入消息队列是否利大于弊？你认为消息队列有哪些缺点？

作业 3 提示：
- （1）服务间异步通信
- （2）顺序消费
- （3）定时任务
- （4）流量削峰
- （5）解耦
- （6）利用消息队列将高并发访问变为串行操作
- （7）异步下单
- （8）消息队列持久化