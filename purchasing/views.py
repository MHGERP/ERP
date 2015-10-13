# coding: UTF-8
from django.shortcuts import render
from django.db.models import Q
from purchasing.models import *
from const import *
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
def bidTrackingViews(request):
    """
    Liu Ye
    """
    bid_id = 444
    bid = BidForm.objects.get(bid_id = bid_id)
    qualityPriceCardForm = QualityPriceCardForm()
    bidApplyForm = BidApplyForm()
    bidCommentForm = BidCommentForm()
    bidComments = BidComment.objects.filter(Q(bid = bid))
    bidForm = BidFormStatus.objects.filter(Q(main_status = BIDFORM_STATUS_INVITE_BID)).order_by("part_status")
    bid_status = []
    for status in bidForm:
        bid_dict = {}
        bid_dict["name"] = status
        bid_dict["class"] = "btn-success"
        bid_status.append(bid_dict)

    context = {"bid_status": bid_status,
               "qualityPriceCardForm": qualityPriceCardForm,
               "bidApplyForm": bidApplyForm,
               "bidCommentForm": bidCommentForm,
               "bidComments": bidComments,
             }
    return render(request, "purchasing/bid_track.html", context)

@csrf.csrf_protect
def arrivalInspectionViews(request):
    if request.method == "POST":
        bid_id = request.POST["bidform_search"]
        print bid_id
        bidFormSet = BidForm.objects.filter(bid_id = bid_id)
    else:
        bidFormSet = BidForm.objects.filter(bid_status__part_status = BIDFORM_PART_STATUS_CHECK) 
    
    context = {
        "bidFormSet":bidFormSet,
    }
    return render(request,"purchasing/purchasing_arrival.html",context)

def arrivalCheckViews(request,bid):
    cargo_set = ArrivalInspection.objects.filter(bidform__bid_id = bid)
    is_exist = PurchasingEntry.objects.filter(bidform__bid_id = bid).count() > 0
    context = {
        "cargo_set":cargo_set,
        "bid":bid,
        "is_exist":is_exist,
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
    if request.method == "POST":
        receipts_code = request.POST["subapply_search"]
        subapply_set = MaterialSubApply.objects.filter(receipts_code = receipts_code)
    else:
        subapply_set = MaterialSubApply.objects.filter(is_submit = True) 
    context = {
        "subapply_set":subapply_set,
    }
    return render(request,"purchasing/subapply_home.html",context)

@csrf.csrf_protect
def subApplyViews(request,sid = None):
    is_show = False
    subapply_obj = MaterialSubApply.objects.get(id = sid)
    if request.method == "POST":
        subapply_form = SubApplyForm(request.POST,instance = subapply_obj)
        if subapply_form.is_valid():
            subapply_form.save()
            subapply_obj.is_submit = True
            subapply_obj.save()
            return HttpResponseRedirect("/purchasing/subApplyHome/")
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
    is_show = True
    subapply_obj = MaterialSubApply.objects.get(id = sid)
    if request.method == "POST":
        subapply_form = SubApplyInspectForm(request.POST,instance = subapply_obj)
        if subapply_form.is_valid():
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

    """
    mode: 0 view, 1 add
    mid : materielexecute id
    """
def materielExecuteDetailViews(request, choice, *mid):
    if choice == "0":
        materielexecute_id = mid[0]
        materielexecute = MaterielExecute.objects.get(pk = materielexecute_id)
        materiel_choice = materielexecute.materiel_choice
        
        if materiel_choice == MAIN_MATERIEL:
            current_materiel_choice = MATERIEL_CHOICE[0][1]
            materielexecute_detail = MainMaterielExecuteDetail.objects.get(materiel_execute__id = materielexecute_id)
        else:
            current_materiel_choice = MATERIEL_CHOICE[1][1]
            materielexecute_detail = SupportMaterielExecuteDetail.objects.get(materiel_execute__id = materielexecute_id)
        materielexecute_detail_set = [materielexecute_detail]
        context = {
            "materielexecute_detail_set" : materielexecute_detail_set,
            "choice" : materiel_choice,
            "MAIN_MATERIEL" : MAIN_MATERIEL,
            "current_materiel_choice" : current_materiel_choice,
            "current_document_number" : materielexecute.document_number
        }
        return render(request, "purchasing/materielexecute/materielexecute_detail_view.html", context)
    else:
        #default MAIN_MATERIEL
        choice_form = MaterielChoiceForm()
        detailForm = MainMaterielExecuteDetailForm()
        materielexecute_detail_set = MainMaterielExecuteDetail.objects.all()
        context = {
            "materielexecute_detail_set" : materielexecute_detail_set,
            "choice" : MAIN_MATERIEL,
            "MAIN_MATERIEL" : MAIN_MATERIEL,
            "current_materiel_choice" : MATERIEL_CHOICE[0][1],
            "materielChoice_form" : choice_form,
            "MainMaterielExecuteDetailForm" : detailForm
        }
        return render(request, "purchasing/materielexecute/materielexecute_detail_add.html", context)

