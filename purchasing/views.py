# coding: UTF-8
from django.shortcuts import render
from django.db.models import Q
from purchasing.models import *
from const import *
from purchasing import *
from const.forms import InventoryTypeForm
from django.http import HttpResponseRedirect
from const.models import WorkOrder, InventoryType, BidFormStatus
from purchasing.forms import *
from datetime import datetime
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q

from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json
from django.db import transaction

from users.decorators import authority_required
from users import *

def purchasingFollowingViews(request):
    """
    chousan1989
    """
    bidform_processing=BidForm.objects.filter(bid_status__main_status__gte=BIDFORM_STATUS_SELECT_SUPPLIER,bid_status__main_status__lte=BIDFORM_STATUS_CHECK_STORE)

    context={
        "bidform":bidform_processing,
        "BIDFORM_STATUS_SELECT_SUPPLIER":BIDFORM_STATUS_SELECT_SUPPLIER,
        "BIDFORM_STATUS_INVITE_BID":BIDFORM_STATUS_INVITE_BID,
        "BIDFORM_STATUS_PROCESS_FOLLOW":BIDFORM_STATUS_PROCESS_FOLLOW,
        "BIDFORM_STATUS_CHECK_STORE":BIDFORM_STATUS_CHECK_STORE 
    }

    return render(request,"purchasing/purchasing_following.html",context)

def bidformApproveViews(request):
    bidform=BidForm.objects.filter(bid_status__part_status=BIDFORM_PART_STATUS_APPROVED)
    return render(request,"purchasing/bidform_approve.html",{"bidform":bidform})

def bidformApproveIDViews(request,bid):
    bidform=BidForm.objects.get(pk=bid)
    bidcommentform=BidCommentForm()
    context={
        "bidform":bidform,
        "bidcommentform":bidcommentform
    }
    return render(request,"purchasing/bidform_approve_id.html",context)

@authority_required(PENDING_ORDER)
def pendingOrderViews(request):
    """
    JunHU
    summary: view function of pendingorder page
    params: NULL
    return: NULL
    """
    return render(request, "purchasing/pending_order.html")

def selectSupplierViews(request,bid):
    suppliers=Supplier.objects.all()
    bidform=BidForm.objects.get(pk=bid)
    for item in suppliers:
        if SupplierSelect.objects.filter(supplier=item,bidform=bidform).count()>0:
            item.selected=1
        else:
            item.selected=0
    context={
        "suppliers":suppliers,
        "bidform":bidform
    }
    return render(request,"purchasing/select_supplier.html",context)

def materialSummarizeViews(request):
    """
    wanglei-0707
    summary: view function of meterialSummarize page
    params: NULL
    return: NULL
    """
    inventoryTypeForm = InventoryTypeForm()
    context = {"inventoryTypeForm": inventoryTypeForm}
    return render(request, "purchasing/material_summarize.html", context)


def supplierManagementViews(request):
    file_upload_error=0
    if request.method=="POST":
        if request.FILES['supplier_file'].size>10*1024*1024:
            file_upload_error=2
        else:
            supplier_id=request.POST['supplier_id']
            supplier=Supplier.objects.get(pk=supplier_id)
            file=SupplierFile()
            file.project=supplier
            file.file_obj=request.FILES['supplier_file']
            file.file_size=str(int(request.FILES['supplier_file'].size)/1000)+"kb"
            file.name=request.FILES['supplier_file'].name
            file.upload_time= datetime.now()
            file.save()
            file_upload_error=1
    suppliers=Supplier.objects.all()
    supplier_form=SupplierForm()
    context={
        "suppliers":suppliers,
        "supplier_form":supplier_form,
        "file_upload_error":file_upload_error
    }
    return render(request,"purchasing/supplier/supplier_management.html",context)

@csrf.csrf_protect
def bidTrackingViews(request, bid_id):
    """
    Liu Ye
    """
    bidform = BidForm.objects.get(id = bid_id)
    qualityPriceCardForm = QualityPriceCardForm()
    try:
        bid_apply = bidApply.objects.get(bid = bidform)
        bidApplyForm = BidApplyForm(instance = bid_apply)
    except:
        bidApplyForm = BidApplyForm()
    #quality_price_card = qualityPriceCard.objects.filter(bid = bidform)

    bidCommentForm = BidCommentForm()
    bidComments = BidComment.objects.filter(Q(bid = bidform))
    bidFormStatuss = BidFormStatus.objects.filter(Q(main_status = BIDFORM_STATUS_INVITE_BID)).order_by("part_status")

    btn_cnt = 2 if bidform.bid_status.part_status < BIDFORM_PART_STATUS_INVITE_BID_APPLY else 0
    btn_color = ["btn-success", "btn-warning", ""]
    bid_status = []
    for status in bidFormStatuss:
        btn_cnt += 1 if status == bidform.bid_status else 0
        bid_dict = {}
        bid_dict["name"] = status
        bid_dict["class"] = btn_color[btn_cnt]
        bid_status.append(bid_dict)
        btn_cnt += 1 if status == bidform.bid_status else 0

    context = {"bid_status": bid_status,
               "qualityPriceCardForm": qualityPriceCardForm,
               "bidApplyForm": bidApplyForm,
               "bidCommentForm": bidCommentForm,
               "bidComments": bidComments,
               "bidform": bidform,
               "BIDFORM_PART_STATUS_INVITE_BID_APPLY": BIDFORM_PART_STATUS_INVITE_BID_APPLY,
               "BIDFORM_PART_STATUS_INVITE_BID_WINBIDNOTICE_AOORIVED": BIDFORM_PART_STATUS_INVITE_BID_WINBIDNOTICE_AOORIVED,
             }
    return render(request, "purchasing/bid_track.html", context)

def contractFinanceViews(request):
    bidforms = BidForm.objects.all()
    context = {
        "bidForms":bidforms,
        "CONTRACT_ADD_AMOUNT": CONTRACT_ADD_AMOUNT,
        "CONTRACT_DETAIL": CONTRACT_DETAIL,
    }
    return render(request,"purchasing/contract_finance.html",context)

@csrf.csrf_protect
def arrivalInspectionViews(request):
    if request.method == "POST":
        bid_id = request.POST["bidform_search"]
        bidFormSet = BidForm.objects.filter(bid_id = bid_id)
    else:
        bidFormSet = BidForm.objects.filter(bid_status__part_status = BIDFORM_PART_STATUS_STORE)    
    context = {
        "bidFormSet":bidFormSet,
        "BIDFORM_PART_STATUS_STORE":BIDFORM_PART_STATUS_STORE,
    }
    return render(request,"purchasing/purchasing_arrival.html",context)

def arrivalCheckViews(request,bid):
    cargo_set = ArrivalInspection.objects.filter(bidform__bid_id = bid)
    is_show = BidForm.objects.filter(bid_id = bid , bid_status__part_status = BIDFORM_PART_STATUS_CHECK).count() > 0
    context = {
        "cargo_set":cargo_set,
        "bid":bid,
        "is_show":is_show,
    }
    return render(request,"purchasing/purchasing_arrivalcheck.html",context)

def inventoryTableViews(request):
    order_index = request.GET.get("order_index")
    tableid = request.GET.get("tableid")
    order = WorkOrder.objects.get(order_index = order_index)
    inventoryType = InventoryType.objects.get(id = tableid)
    context = {"order": order,
               "inventoryType": inventoryType,
    }
    return render(request, "purchasing/inventory_table_base.html", context)

def materialEntryViews(request,bid):
    try:
        purchasingentry = PurchasingEntry.objects.get(bidform__bid_id = bid)
        entry_set = PurchasingEntryItems.objects.filter(purchasingentry = purchasingentry)
        entry_form = EntryForm(instance = purchasingentry)
    except Exception,e:
        print e
    context = {
        "pur_entry":purchasingentry,
        "entry_set":entry_set,
        "entry_form":entry_form,
    }
    return render(request,"purchasing/purchasing_materialentry.html",context)

def subApplyHomeViews(request):
    is_show = True
    if request.method == "POST":
        receipts_code = request.POST["subapply_search"]
        subapply_set = MaterialSubApply.objects.filter(receipts_code = receipts_code)
    else:
        subapply_set = MaterialSubApply.objects.filter(is_submit = True) 
    context = {
        "subapply_set":subapply_set,
        "is_show":is_show,
    }
    return render(request,"purchasing/subapply_home.html",context)

@csrf.csrf_protect
def subApplyViews(request,sid = None):
    subapply_obj = MaterialSubApply.objects.get(id = sid)
    is_show = not subapply_obj.is_submit
    if request.method == "POST":
        subapply_form = SubApplyForm(request.POST,instance = subapply_obj)
        if subapply_form.is_valid():
            if is_show:
                subapply_form.save()
                subapply_obj.is_submit = True
                subapply_obj.save()
            return HttpResponseRedirect("/purchasing/subApplyHome/")
        else:
            print subapply_form.errors
    else:
        subapply_form = SubApplyForm(instance = subapply_obj)
    sub_set = MaterialSubApplyItems.objects.filter(sub_apply__id = sid)
    subitem_form = SubApplyItemForm()
    context = {
        "subapply_form":subapply_form,
        "is_show":is_show,
        "sub_set":sub_set,
        "subitem_form":subitem_form,
        "subapply":subapply_obj,
    }
    return render(request,"purchasing/subapplication.html",context)

@csrf.csrf_protect
def subApplyReviewViews(request,sid = None):
    subapply_obj = MaterialSubApply.objects.get(id = sid)
    is_show = subapply_obj.is_submit and subapply_obj.is_approval == REVIEW_COMMENTS_CHOICE_WAIT 
    if request.method == "POST":
        subapply_form = SubApplyInspectForm(request.POST,instance = subapply_obj)
        if subapply_form.is_valid():
            if is_show:
                subapply_form.save()
                subapply_obj.is_submit = True
                subapply_obj.save()
            return HttpResponseRedirect("/purchasing/subApplyHome/")
    else:
        subapply_form = SubApplyInspectForm(instance = subapply_obj)
    sub_set = MaterialSubApplyItems.objects.filter(sub_apply__id = sid)
    subitem_form = SubApplyItemForm()
    context = {
        "subapply_form":subapply_form,
        "is_show":is_show,
        "sub_set":sub_set,
        "subitem_form":subitem_form,
        "subapply":subapply_obj,
    }
    return render(request,"purchasing/subapplication.html",context)

def orderFormManageViews(request):
    """
    JunHU
    """
    form = OrderFormStatusForm()
    context = {
        "form": form,
        }
    return render(request, "purchasing/order_form_manage.html", context)

def orderFormViews(request):
    """
    JunHu
    """
    index = request.GET.get("index")
    order_form = OrderForm.objects.get(order_id = index)
    context = {
        "order_form": order_form,
    }
    return render(request, "purchasing/order_form.html", context)

def processFollowingViews(request,bid):
    bidform=BidForm.objects.get(pk=bid)
    process_following_info=ProcessFollowingInfo.objects.filter(bidform=bidform)
    process_following_form=ProcessFollowingForm(initial={
        'bidform':bidform,
        'following_date':datetime.today(),
        'executor':request.user
    })
    context={
        "bidform":bidform,
        "process_following_info":process_following_info,
        "process_following_form":process_following_form
    }
    return render(request,"purchasing/process_following.html",context)

def materielExecuteViews(request):
    materielexecute_set = MaterielExecute.objects.all()
    context = {
        "materielexecute_set":materielexecute_set,
    }
    return render(request, "purchasing/materielexecute/materielexecute_management.html", context)

def processFollowAdd(request):
    if request.is_ajax():
        status=0
        form_html=""
        form=ProcessFollowingForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        else:
            form_html=render_to_string("purchasing/process_following/process_following_form.html",{"process_following_form":form})
            status=1
        return HttpResponse(json.dumps({'status':status,"form_html":form_html}),content_type="application/json")

    
def materielExecuteDetailViews(request, choice, *mid):
    """
    mxl
    summary : click into add or view html
    params : choice : main or support detail
             mid : option param, the materielexecute id
    """
    if choice == "0":
        materielexecute_id = mid[0]
        materielexecute = MaterielExecute.objects.get(pk = materielexecute_id)
        materiel_choice = materielexecute.materiel_choice
        
        materielexecute_detail_set = MaterielExecuteDetail.objects.filter(materiel_execute = materielexecute)
        # materielexecute_detail_set = [materielexecute_detail]
        executeForm = MaterielExecuteForm(instance = materielexecute)
        context = {
            "materielexecute_detail_set" : materielexecute_detail_set,
            "choice" : materiel_choice,
            "MAIN_MATERIEL" : MAIN_MATERIEL,
            "executeForm" : executeForm
        }
        return render(request, "purchasing/materielexecute/materielexecute_detail_view.html", context)
    else:
        #default MAIN_MATERIEL
        #detailForm = MainMaterielExecuteDetailForm()
        # materielexecute_detail_set = MainMaterielExecuteDetail.objects.all()
        materiel_choice=MAIN_MATERIEL
        try:
            materielexecute_id = mid[0]
            materielexecute = MaterielExecute.objects.get(pk = materielexecute_id)
            materiel_choice = materielexecute.materiel_choice
            executeForm = MaterielExecuteForm(instance = materielexecute)
            materielexecute_detail_set = MaterielExecuteDetail.objects.filter(materiel_execute = materielexecute)

            

        except:
            executeForm = MaterielExecuteForm()
            materiel_choice=MAIN_MATERIEL
            materielexecute_detail_set=None
            
        if materiel_choice==MAIN_MATERIEL:
            type=1
        else:
            type=2
        materiels=MaterielExecuteDetail.objects.filter(materiel__inventory_type__id=type,materiel_execute__isnull=True)
        context = {
            "materielexecute_detail_set" : materielexecute_detail_set,
            "choice" : materiel_choice,
            "MAIN_MATERIEL" : MAIN_MATERIEL,
            "MaterielExecuteForm" : executeForm,
            "materiels":materiels
           # "MainMaterielExecuteDetailForm" : detailForm
        }
        return render(request, "purchasing/materielexecute/materielexecute_detail_add.html", context)

def statusChangeViews(request):
    bid_set = BidForm.objects.all()
    if request.method == "POST":
        bid_id = request.POST["bidform_search"]
        bid_set = BidForm.objects.filter(bid_id = bid_id)
    context = {
        "bid_set":bid_set,
    }
    return render(request,"purchasing/status_change/home.html",context)

def statusChangeHistoryViews(request,bid):
    statuschange_set = StatusChange.objects.filter(bidform__bid_id = bid).order_by("change_time")
    
    for obj in statuschange_set:
        try: 
            obj.reason = obj.statuschangereason
            print obj.change_time
            print obj.reason
        except Exception,e:
            pass
    context = {
        "his_set":statuschange_set,
        "bid":bid,
    }
    return render(request,"purchasing/status_change/statushistory.html",context)

@transaction.commit_manually
def statusChangeApplyViews(request,bid):
    bidform = BidForm.objects.get(bid_id = bid)
    if request.method == "POST":
        statuschangeform = StatusChangeApplyForm(request.POST,bidform = bidform)
        if statuschangeform.is_valid():
            statuschange_obj = statuschangeform.save(commit = False)
            statuschange_obj.bidform = bidform
            statuschange_obj.change_user = request.user
            statuschange_obj.normal_change = False
            statuschange_obj.original_status = bidform.bid_status
            try:
                bidform.bid_status = statuschange_obj.new_status
                bidform.save()
                statuschange_obj.save()
                reason = statuschangeform.cleaned_data["reason"]
                changereason = StatusChangeReason(status_change = statuschange_obj ,reason = reason)
                changereason.save()
                transaction.commit()
                return HttpResponseRedirect('/purchasing/statusChangeHome')
            except Exception,e:
                transaction.rollback()
                print e
        else:
            print statuschangeform.errors
    else:
        statuschangeform = StatusChangeApplyForm(bidform=bidform)   
    
    context = {
        'chform':statuschangeform,
    }
    revl = render(request,"purchasing/status_change/statuschangeapply.html",context)
    transaction.commit()
    return revl

    
