#!/usr/bin/env python
# coding=utf-8

from dajax.core import Dajax
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from const.models import WorkOrder,Materiel
from production.models import *
from purchasing.models import *
from production.forms import *
from techdata.models import Processing, CirculationRoute
from django.db import connection
from django.db.models import Q,Sum
from storage.utils import get_weld_filter
from const.forms import WorkOrderForm
from production.forms import *
from django.contrib.auth.models import User
from users.models import UserInfo
from storage.models import *
from const import *
from production.utility import get_applycard_code, ApplyCardModelCheckDICT

def getQ(con):
    query_set = Q()
    for k,v in con.items():
         if v:
             if k.endswith("isnull"):
                 v = int(v)
             query_set.add(Q(**{k: v}), Q.AND)
    return query_set

@dajaxice_register
def getFileList(request, form):
    """
    Lei
    """
    sub_work_order_form = SubWorkOrderForm(deserialize_form(form))
    if sub_work_order_form.is_valid():
        syn_size_file_list_status = SynthesizeFileListStatus.objects.filter(getQ(sub_work_order_form.cleaned_data))
    syn_size_file_list = []
    for item in syn_size_file_list_status:
        syn_size_file_list.append([(status, getattr(item,status)) for status in SYNSIZE_FILE_LIST_STATUS])
    context = {
        "syn_size_file_list":zip(syn_size_file_list_status, syn_size_file_list),
    }
    html = render_to_string("production/synthesize_detail_filelist.html",context)
    return html

@dajaxice_register
def changeFileList(request, status, workorder_id, is_check):
    """
    Lei
    """
    syn_size_file_status = SynthesizeFileListStatus.objects.get(sub_order = workorder_id)
    setattr(syn_size_file_status,status,is_check)
    syn_size_file_status.save()
    return 

@dajaxice_register
def getHourSearch(request, form):
    """
    Lei
    """
    hour_message_search_form = HourMessageSearchForm(deserialize_form(form))
    if hour_message_search_form.is_valid():
        process_detail_list  = ProcessDetail.objects.filter(getQ(hour_message_search_form.cleaned_data))
    else:
        print hour_message_search_form.errors
    context = {
            "process_detail_list":process_detail_list
        }

    html = render_to_string("production/man_hour_message_list.html",context)
    return html

@dajaxice_register
def getHourSummarize(request, form):
    """
    Lei
    """
    hour_summarize_form = HourSummarizeForm(deserialize_form(form))
    if hour_summarize_form.is_valid():
        select = {'month': connection.ops.date_trunc_sql('month', 'complete_process_date')}
        process_detail_list  = ProcessDetail.objects.exclude(complete_process_date = None).filter(getQ(hour_summarize_form.cleaned_data))\
        .extra(select=select).values('month','sub_materiel_belong__sub_order','sub_materiel_belong__sub_order__name', 'productionworkgroup', 'productionworkgroup__name').annotate(Sum('work_hour'))
    else:
        print hour_message_search_form.errors
    context = {
        "process_detail_list":process_detail_list
    }
    html = render_to_string("production/widgets/man_hour_table.html",context)
    return html

@dajaxice_register
def getSummarizeTicket(request, work_order_id, groupNumId, date):
    """
    Lei
    """
    year,month = date.split("-")
    process_detail_list = ProcessDetail.objects.filter(Q(sub_materiel_belong__sub_order__id=work_order_id)&Q(productionworkgroup=groupNumId)&Q(complete_process_date__year=year)&Q(complete_process_date__month=month)).order_by('complete_process_date')
    work_order = process_detail_list[0].sub_materiel_belong.sub_order.name
    group_num = process_detail_list[0].productionworkgroup.name
    context = {
        "work_order":work_order,
        "group_num":group_num,
        "process_detail_list":process_detail_list
    }
    html = render_to_string("production/man_hour_summarize_table.html",context)
    return html

@dajaxice_register
def getPartTicket(request, work_order_id, groupNumId, date):
    """
    Lei
    """
    year,month = date.split("-")
    process_detail_list = list(ProcessDetail.objects.filter(Q(sub_materiel_belong__sub_order__id=work_order_id)&Q(productionworkgroup=groupNumId)&Q(complete_process_date__year=year)&Q(complete_process_date__month=month)).order_by('sub_materiel_belong'))
    work_order = process_detail_list[0].sub_materiel_belong.sub_order.name
    group_num = process_detail_list[0].productionworkgroup.name
    process_detail_list.extend([ProcessDetail()] * ((4-len(process_detail_list))%4))
    context = {
        "work_order":work_order,
        "group_num":group_num,
        "process_detail_list":process_detail_list
    }
    html = render_to_string("production/man_hour_part_ticket.html",context)
    return html


@dajaxice_register
def workorderSearch(request, form):
    """
    kad
    """
    search_form = WorkOrderProductionSearchForm(deserialize_form(form))
    if search_form.is_valid():
        workorder_set  = WorkOrder.objects.filter(getQ(search_form.cleaned_data))
    html = render_to_string("production/widgets/production_plan_select_table.html",{"workorder_set":workorder_set})
    data = {
        "html":html,
    }
    return simplejson.dumps(data)

@dajaxice_register
def workorderAdd(request, checkList):
    """
    kad
    """
    for i in checkList:
        wo_obj = WorkOrder.objects.get(order_index = i)
        obj = ProductionPlan(order = wo_obj)
        obj.save()
    prodplan_set = ProductionPlan.objects.all()
    html = render_to_string("production/widgets/production_plan_table.html", {"prodplan_set":prodplan_set})
    data = {
        "html":html,
    }
    return simplejson.dumps(data)

@dajaxice_register
def prodplanDelete(request, planid):
    """
    kad
    """
    try:
        prodplan_obj = ProductionPlan.objects.get(plan_id = planid)
        prodplan_obj.delete()
        flag = True
    except Exception,e:
        print e
        flag = False
    data = {
        "flag":flag,
    }
    return simplejson.dumps(data)

@dajaxice_register
def getProductPlanForm(request, planid):
    prodPlanForm = ProdPlanForm(instance = ProductionPlan.objects.get(plan_id = planid))
    return simplejson.dumps(prodPlanForm.as_p())
    
@dajaxice_register
def prodplanUpdate(request, form, planid):
    """
    kad
    """
    prodplan_obj = ProductionPlan.objects.get(plan_id = planid)
    prodplan_form = ProdPlanForm(deserialize_form(form), instance=prodplan_obj)
    if prodplan_form.is_valid():
        prodplan_form.save()
        message = u"修改成功"
        flag = True
    else:
        message = u"修改失败"
        flag = False
    prodplan_set = ProductionPlan.objects.all()
    html = render_to_string("production/widgets/production_plan_table.html", {"prodplan_set":prodplan_set})

    data ={
        "html":html,
        "message":message,
        "flag":flag,
    }
    return simplejson.dumps(data)

@dajaxice_register
def prodplanSearch(request, form):
    """
    kad
    """
    search_form = ProductionPlanSearchForm(deserialize_form(form))
    if search_form.is_valid():
        prodplan_set  = ProductionPlan.objects.filter(getQ(search_form.cleaned_data))
        html = render_to_string("production/widgets/production_plan_table.html",{"prodplan_set":prodplan_set})
    else:
        print search_form.errors
    data = {
        "html":html,
    }
    return simplejson.dumps(data)

@dajaxice_register
def taskAllocationSearch(request, form):
    """
    bin
    """
    form = TaskAllocationForm(deserialize_form(form))
    items_list = {}
    if form.is_valid():
        conditions = form.cleaned_data
        items_list = ProcessDetail.objects.exclude(plan_startdate = None).filter(complete_process_date = None).filter(getQ(conditions)).order_by('-productionworkgroup');
        for item in items_list:
            item.groups = ProductionWorkGroup.objects.filter(processname = item.processname);
    context = {
        "items_list":items_list,
        "taskallocationform":form,
    }
    html = render_to_string("production/table/task_allocation_table.html",context)
    return simplejson.dumps({"html":html})

@dajaxice_register
def taskConfirmSearch(request, form):
    """
    bin
    """
    form = TaskConfirmForm(deserialize_form(form))
    items_list = {}
    if form.is_valid():
        conditions = form.cleaned_data
        items_list = ProcessDetail.objects.exclude(productionworkgroup = None).filter(getQ(conditions)).order_by('complete_process_date');
    context = {
        "items_list":items_list,
        "taskallocationform":form,
    }
    html = render_to_string("production/table/task_confirm_table.html",context)
    return simplejson.dumps({"html":html})

@dajaxice_register
def taskPlanSearch(request, form):
    """
    bin
    """
    form = TaskPlanForm(deserialize_form(form))
    items_list = {}
    if form.is_valid():
        conditions = form.cleaned_data
        items_list = ProcessDetail.objects.filter(productionworkgroup = None).filter(getQ(conditions)).order_by('sub_materiel_belong').order_by('-plan_startdate');
    context = {
        "items_list":items_list,
        "taskplanform":form,
    }
    html = render_to_string("production/table/task_plan_table.html",context)
    return simplejson.dumps({"html":html})

@dajaxice_register
def taskPlanSubmit(request, form, mid, startdate, enddate):
    """
    bin
    """
    item = ProcessDetail.objects.get(id = mid)
    item.plan_startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    item.plan_enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    item.save()
    return taskPlanSearch(request, form)


@dajaxice_register
def taskPlanChange(request, mid):
    """
    bin
    """
    item = ProcessDetail.objects.get(id = mid)
    context = {
        "item":item,
    }
    html = render_to_string("production/table/task_plantime_table.html",context)
    return simplejson.dumps({"html":html})
    
@dajaxice_register
def taskAllocationRemove(request, form, mid):
    """
    bin
    """
    item = ProcessDetail.objects.get(id = mid)
    item.productionworkgroup = None
    item.save()
    return taskAllocationSearch(request, form)
   
@dajaxice_register
def taskAllocationSubmit(request, form, mid, groupid):
    """
    bin
    """
    item = ProcessDetail.objects.get(id = mid)
    group = ProductionWorkGroup.objects.get(id = groupid)
    item.productionworkgroup = group
    item.save()
    return taskAllocationSearch(request, form)
      
@dajaxice_register
def taskConfirmFinish(request, form, mid):
    """
    bin
    """
    item = ProcessDetail.objects.get(id = mid)
    import datetime
    item.complete_process_date = datetime.datetime.today();
    print datetime.datetime.today()
    item.save()
    return taskConfirmSearch(request, form)

@dajaxice_register
def taskConfirmView(request,mid):
    """
    bin
    """
    item = ProcessDetail.objects.get(id = mid)
    context = {
        "item":item,
    }
    html = render_to_string("production/table/task_view_table.html",context)
    return simplejson.dumps({"html":html})

@dajaxice_register
def taskCheck(request, mid, check_content):
    item = ProcessDetail.objects.get(id = mid)
    item.check_content = check_content
    item.check_date = datetime.datetime.today()
    item.check_user = request.user
    item.save()
    context = {
        "item":item,
    }
    html = render_to_string("production/table/task_view_table.html",context)
    return simplejson.dumps({"html":html})
    
@dajaxice_register
def ledgerTimeChange(request, mid):
    """
    bin
    """
    item = SubMateriel.objects.get(id = mid)
    form = MaterialPlantimeChangeForm(instance = item)
    return simplejson.dumps(form.as_p())

@dajaxice_register
def materialPlantimeChange(request, mid, date):
    """
    bin
    """
    materielObj= SubMateriel.objects.get(id = mid)
    complete_plandate = datetime.datetime.strptime(date, '%Y-%m-%d')
    materielObj.complete_plandate = complete_plandate
    materielObj.save()
    materielObj.processDetailObj = list(ProcessDetail.objects.filter(sub_materiel_belong = materielObj).order_by('process_id'))
    materielObj.processDetailObj.extend([ProcessDetail()] * (12-len(materielObj.processDetailObj)))
    html = render_to_string("production/widgets/weld_part_order_info_table.html",{"materielObj":materielObj})
    return simplejson.dumps({ "html" : html})

@dajaxice_register
def ledgerSearch(request, form):
    search_form = LedgerSearchForm(deserialize_form(form))
    if search_form.is_valid():
        materiel_list  = SubMateriel.objects.filter(getQ(search_form.cleaned_data))
        html = render_to_string("production/widgets/designBOM_table_list.html",{"BOM":materiel_list})
    else:
        print search_form.errors
    return simplejson.dumps({ "html" : html})

@dajaxice_register
def weldPartOrderInfo(request, iid):
    """
    Lei
    """
    materielObj = SubMateriel.objects.get(id=iid)
    materielObj.processDetailObj = list(ProcessDetail.objects.filter(sub_materiel_belong = materielObj).order_by('process_id'))
    materielObj.processDetailObj.extend([ProcessDetail()] * (12-len(materielObj.processDetailObj)))
    html = render_to_string("production/widgets/weld_part_order_info_table.html",{"materielObj":materielObj})
    return simplejson.dumps({ "html" : html})

@dajaxice_register
def getProductionUser(request, form):
    """
    Lei
    """
    production_user_search_form = ProductionUserSearchForm(deserialize_form(form))
    if production_user_search_form.is_valid():
        production_user_list  = ProductionUser.objects.filter(getQ(production_user_search_form.cleaned_data))
    html = render_to_string("production/widgets/production_user_table.html",{"production_user_list":production_user_list})
    return html

@dajaxice_register
def getUser(request, form):
    """
    Lei
    """
    user_choose_form = UserChooseForm(deserialize_form(form))
    if user_choose_form.is_valid():
        user_list = UserInfo.objects.filter(getQ(user_choose_form.cleaned_data)).order_by("productionuser")
    html = render_to_string("production/widgets/user_table.html",{"user_list":user_list})
    return html

@dajaxice_register
def prodUserModify(request, produserid):
    """
    Lei
    """
    productionUserForm = ProductionUserForm(instance = ProductionUser.objects.get(id = produserid))
    return productionUserForm.as_p()

@dajaxice_register
def saveProdUserModify(request, form, produserid):
    prod_user_obj = ProductionUser.objects.get(id = produserid)
    prod_user_form = ProductionUserForm(deserialize_form(form),instance = prod_user_obj)
    if prod_user_form.is_valid():
        prod_user_form.save()
        message = u"修改成功"
    else:
        message = u"修改失败"
    return message

@dajaxice_register
def prodUserDelete(request, uid):
    """
    Lei
    """
    produser_obj = ProductionUser.objects.get(id = uid)
    produser_obj.delete()
    return uid

@dajaxice_register
def addProdUser(request, checkUserList):
    """
    Lei
    """
    for username in checkUserList:
        userInfor_obj = UserInfo.objects.get(user__username = username)
        prod_user_obj = ProductionUser()
        prod_user_obj.production_user_id = userInfor_obj
        prod_user_obj.save()
    return

@dajaxice_register
def applyCardSearch(request, form):
    search_form = ApplyCardForm(deserialize_form(form))
    if search_form.is_valid():
        applyCards = []
        for applyCardModel in [SteelMaterialApplyCard, AuxiliaryToolApplyCard, OutsideApplyCard, WeldingMaterialApplyCard]:
            materiel_list  = applyCards.extend(list(applyCardModel.objects.filter(getQ(search_form.cleaned_data))))
        html = render_to_string("production/table/materiel_use_table.html",{"applyCards":applyCards})
    else:
        print search_form.errors
    return simplejson.dumps({ "html" : html})

@dajaxice_register
def materialuseSearch(request, form):
    search_form = MaterielCopyForm(deserialize_form(form))
    if search_form.is_valid():
        materiel_list  = MaterielCopy.objects.filter(getQ(search_form.cleaned_data))
        print materiel_list.count()
        html = render_to_string("production/table/materiel_use_select_table.html",{"items":materiel_list})
    else:
        print search_form.errors
        return simplejson.dumps({ "html" : html})

ApplyCardModelDICT = {
    SteelMaterialApplyCard:"G",
    AuxiliaryToolApplyCard:"F",
    OutsideApplyCard:"W",
    WeldingMaterialApplyCard:"H",
}

def createSteelMaterialApplyCard(request, materielCopys):
    steelMaterialApplyCard = SteelMaterialApplyCard(applycard_code=get_applycard_code(SteelMaterialApplyCard),)
    steelMaterialApplyCard.save()
    for item in materielCopys:
        applyCardItem = SteelMaterialApplyCardItems(apply_card = steelMaterialApplyCard,
                                                    material_mark=item.material.name,
                                                    material_code=item.quality_number,
                                                    count=item.count,
                                                    work_order = item.sub_workorder,
                                                    specification = item.specification,
        )
        applyCardItem.save()
        return [steelMaterialApplyCard.applycard_code]


def createOutsideApplyCard(request, materielCopys):
    outsideApplyCard = OutsideApplyCard(applycard_code=get_applycard_code(OutsideApplyCard),
                                        work_order=materielCopys[0].sub_workorder,)
    outsideApplyCard.save()
    print outsideApplyCard 
    for item in materielCopys:
        applyCardItem = OutsideApplyCardItems(apply_card = outsideApplyCard,
                                              schematic_index=item.schematic_index,
                                              specification=item.name,
                                              material_mark=item.material.name,
                                              material_code=item.quality_number,
                                              unit=item.unit,
                                              count=item.count,
        )
        applyCardItem.save()
    return [outsideApplyCard.applycard_code]


def createWeldingMaterialApplyCard(request, materielCopys):
    applycard_codes = []
    for item in materielCopys:
        applyCard = WeldingMaterialApplyCard(applycard_code=get_applycard_code(WeldingMaterialApplyCard),
                                             work_order = item.sub_workorder,
                                             material_code=item.quality_number,
                                             material_mark=item.material.name,
                                             specification=item.specification,
                                             apply_count=item.count,)
        applyCard.save()
        applycard_codes.append(applyCard.applycard_code)
    return applycard_codes 


@dajaxice_register
def createApplyCard(request, form, iids):
    search_form = ApplyCardTypeForm(deserialize_form(form))
    if search_form.is_valid():
        materielCopys = MaterielCopy.objects.filter(Q(id__in=iids))
        applytype = search_form.cleaned_data["applytype"]
        if applytype == "H":
            applycodes = createWeldingMaterialApplyCard(request, materielCopys)
        elif applytype == "G":
            applycodes = createSteelMaterialApplyCard(request, materielCopys)
        elif applytype == "W":
            applycodes = createOutsideApplyCard(request, materielCopys)
    return simplejson.dumps(",".join(applycodes))

html_href = {"G":"steel",
             "W":"outside",
             "H":"weld",
             "F":"auxiliarytool",
    
}

@dajaxice_register
def getApplyCardDetail(request, aid):
    context={}
    context["apply_card"]=ApplyCardModelCheckDICT[aid[0]].objects.get(applycard_code=aid)
    if aid[0]=="G":
        ApplyCardItemsModel = SteelMaterialApplyCardItems
    elif aid[0]=="W":
        ApplyCardItemsModel = OutsideApplyCardItems
    if aid[0] in ["W", "G"]:
        context["items"]=ApplyCardItemsModel.objects.filter(apply_card=context["apply_card"])
    html = render_to_string("storage/wordhtml/%sapplycard.html" % (html_href[aid[0]]), context)
    return simplejson.dumps(html)
