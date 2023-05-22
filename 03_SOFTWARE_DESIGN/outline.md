### 巨人的肩膀
- Pendo
  - 时间轴or日历板
- [monday](https://monday.com)
- [滴答清单](https://dida365.com/about/features)
- [csdn](https://blog.csdn.net/bishe401/article/details/128133054)
- [大学生趣味时间管理软件](https://max.book118.com/html/2017/1223/145656865.shtm)
- [一个需求分析与系统设计](https://issuu.com/dashdeep/docs/software__requirement_specification_task_scheduler)
### STEP ONE
- 场景描述与需求分析
  针对有较多任务安排的人群，常常需要对大量任务进行合理规划和管理，对于任务方便地插入与删除，明确地显示已完成与待办任务，智能规划辅助执行的顺序。
- 预期效果
  - 添加任务(内容、deadline/时间、四象限划分、执行周期、任务类型)
  - 任务临期提醒(根据当前日期与deadline的远近程度进行不同频繁程度的提醒)
  - 任务顺序的排列
      - 手动排序
      - 根据用户习惯排序
  - 完成任务

```puml
actor "Visitor" as v
actor "User" as u
u --|> v
left to right direction
rectangle 系统总览 {
    v --> (注册)
    (注册) ..> (填写个人信息): "<<include>>"
    (填写个人信息) ..> (填写习惯问卷): "<<include>>"
    (注册) <.. (注册失败): "<<extend>>"

    v --> (登录)
    (登录) <.. (忘记密码): "<<extend>>"

    u <-- (临期任务提醒)

    (临期任务提醒) <.. (用户习惯识别): "<<extend>>"

    u --> (任务管理)
    
    (任务管理) ..> (添加任务信息): "<<include>>"
    (任务管理) ..> (查看任务信息): "<<include>>"
    (任务管理) ..> (设置完成任务): "<<include>>"
    (任务管理) ..> (修改任务信息): "<<include>>"
    (任务管理) ..> (删除任务信息): "<<include>>"
    (任务管理) ..> (调整任务顺序): "<<include>>"

    (填写习惯问卷) ..> (用户习惯识别): "<<include>>"

    (调整任务顺序) ..> (智能调整): "<<include>>"
    (调整任务顺序) ..> (手动调整): "<<include>>"
    (手动调整) ..> (用户习惯识别): "<<include>>"
    (智能调整) <.. (用户习惯识别): "<<extend>>"

    u --> (数据统计)
  
}
```