# coding=utf-8

TASK_ALLOCATION_STATUS_CHOICES = (
 (-1,u"任务分配状态"),
 (0,u"未分配"),
 (1,u"已分配"),
)

TASK_CONFIRM_STATUS_CHOICES = (
  (-1,u"任务完成状态"),
  (0,u"未完成"),
  (1,u"已完成"),
)


PRODUCTION_=40

BIDFORM_STATUS_CHOICES=(
    (BIDFORM_STATUS_CREATE,u"标单生成"),
    (BIDFORM_STATUS_SELECT_SUPPLIER,u"供应商选择"),
    (BIDFORM_STATUS_INVITE_BID,u"招标"),
    (BIDFORM_STATUS_PROCESS_FOLLOW,u"过程跟踪"),
    (BIDFORM_STATUS_CHECK_STORE,u"检查入库"),
    (BIDFORM_STATUS_COMPLETE,u"标单完成"),
    (BIDFORM_STATUS_STOP,u"标单终止")
)
