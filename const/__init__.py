# coding: UTF-8

BIDFORM_STATUS_CREATE=1
BIDFORM_STATUS_ESTABLISHMENT=2
BIDFORM_STATUS_APPROVED=3
BIDFORM_STATUS_SELECT_SUPPLIER=4
BIDFORM_STATUS_INVITE_BID=5
BIDFORM_STATUS_PROCESS_FOLLOW=6
BIDFORM_STATUS_CHECK_STORE=7
BIDFORM_STATUS_COMPLETE=8
BIDFORM_STATUS_STOP=-1

BIDFORM_STATUS_CHOICES=(

    (BIDFORM_STATUS_CREATE,u"标单创建"),
    (BIDFORM_STATUS_ESTABLISHMENT,u"标单编制"),
    (BIDFORM_STATUS_APPROVED,u"标单审批"),
    (BIDFORM_STATUS_SELECT_SUPPLIER,u"供应商选择"),
    (BIDFORM_STATUS_INVITE_BID,u"招标"),
    (BIDFORM_STATUS_PROCESS_FOLLOW,u"过程跟踪"),
    (BIDFORM_STATUS_CHECK_STORE,u"检查入库"),
    (BIDFORM_STATUS_COMPLETE,u"标单完成"),
    (BIDFORM_STATUS_STOP,u"标单终止")
    
)

IDENTITYERROR = "登录帐号或密码有错误！"
