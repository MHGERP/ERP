# coding: UTF-8
from const.models import *
from purchasing.models import *

bidapply = bidApply()

#bidapply.implement_class = ImplementClassChoices.objects.get(category = 1)
bidapply.bid = BidForm.objects.get(id = 6)
bidapply.apply_company = models.CharField(null=True, max_length=40, verbose_name=u"申请单位")
bidapply.demand_company = "1"
bidapply.work_order = BidFormStatus.objects.get(id=10)
bidapply.bid_project = "1"
bidapply.bid_date = "1990-12-05"
bidapply.special_model = "1"
bidapply.core_part = "1"

bidapply.save()
