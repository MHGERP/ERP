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
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q

from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json
from django.db import transaction

from users.decorators import authority_required
from users import *
from storage.forms import EntryTypeForm
from storage.models import *
from datetime import datetime
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
    order_form=bidform.order_form
    context={
        "suppliers":suppliers,
        "bidform":bidform,
        "order_form":order_form,
        "items":MaterielCopy.objects.filter(materielformconnection__order_form=order_form)
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

    btn_cnt = 2 if bidform.bid_status.part_status < BIDFORM_PART_STATUS_INVITE_BID_APPLY_SELECT else 0
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
              # "BIDFORM_PART_STATUS_INVITE_BID_APPLY_SELECT": BIDFORM_PART_STATUS_INVITE_BID_APPLY_SELECT,
              # "BIDFORM_PART_STATUS_INVITE_BID_WINBIDNOTICE_AOORIVED": BIDFORM_PART_STATUS_INVITE_BID_WINBIDNOTICE_AOORIVED,
               "supplier_set":bidform.supplierselect_set.all()
             }
    """
    bidform = BidForm.objects.get(id = bid_id)
    bidFormStatuss = BidFormStatus.objects.filter(Q(main_status = BIDFORM_STATUS_INVITE_BID)).order_by("part_status")


    btn_cnt = 2 if bidform.bid_status.part_status < BIDFORM_PART_STATUS_INVITE_BID_APPLY_SELECT else 0
    btn_color = ["btn-success", "btn-warning", ""]
    bid_status = []
    for status in bidFormStatuss:
        btn_cnt += 1 if status == bidform.bid_status else 0
        bid_dict = {}
        bid_dict["name"] = status
        bid_dict["class"] = btn_color[btn_cnt]
        bid_status.append(bid_dict)
        btn_cnt += 1 if status == bidform.bid_status else 0
    try:
        bid_apply=bidform.bidapply     
        if bid_apply.status.status == BIDFORM_PART_STATUS_INVITE_BID_APPLY_FINISH:
            bid_apply_finish=True
        else:
            bid_apply_finish=False
    except:
        bid_apply_finish=False
    try:
        supplier_check=bidform.suppliercheck     
        if supplier_check.status.status == BIDFORM_PART_STATUS_INVITE_BID_APPLY_FINISH:
            supplier_check_finish=True
        else:
            supplier_check_finish=False
    except:
        supplier_check_finish=False
    try:
        quality_card=bidform.qualitypricecard     
        if quality_card.status.status == BIDFORM_PART_STATUS_INVITE_BID_APPLY_FINISH:
            quality_card_finish=True
        else:
            quality_card_finish=False
    except:
        quality_card_finish=False
    
    print quality_card_finish
    order_form=bidform.order_form

    try:
        bid_acception=bidform.bidacceptance
    except:
        bid_acception=BidAcceptance(bid=bidform)
        bid_acception.save()
    bid_acceptance_form=BidAcceptanceForm(instance=bid_acception,bidform=bidform)
    context={
        "bid_status":bid_status,
        "bidform":bidform,
        "bid_status_dic":BIDFORM_PART_STATUS_DICT,
        "order_form":order_form,
        "bid_apply_finish":bid_apply_finish,
        "supplier_check_finish":supplier_check_finish,
        "quality_card_finish":quality_card_finish,
        "bid_acceptance_form":bid_acceptance_form,
        "bid_acceptance":bid_acception,
        "items":MaterielCopy.objects.filter(materielformconnection__order_form=order_form)
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

def arrivalInspectionConfirmViews(request,entry_typeid,eid,steel_typeid):
    """
    Liu Guochao
    """
    entry = []
    items = []
    entry_typeid = int(entry_typeid)
    if entry_typeid == 1:
        message = weldMaterialEntryConfirm(request,eid,entry_typeid)
    elif entry_typeid == 2:
        message = steelMaterialEntryConfirm(request,eid,steel_typeid,entry_typeid)
    elif entry_typeid == 3:
        message = auxiliaryToolEntryConfirm(request,eid,entry_typeid)
    elif entry_typeid == 4:
        message = outsideEntryConfirm(request,eid,entry_typeid)
    return message
def weldMaterialEntryConfirm(request,eid,entry_typeid):
    entry = WeldMaterialEntry.objects.get(id = eid)
    items = WeldMaterialEntryItems.objects.filter(entry = entry)
    context = {
            "entry":entry,
            "entry_set":items,
            "entry_type":entry_typeid,
    }
    return render(request,"purchasing/widgets/purchasing_arrival_confirm_weld.html",context)
def steelMaterialEntryConfirm(request,eid,steel_typeid,entry_typeid):
    entry = SteelMaterialPurchasingEntry.objects.get(id = eid)
    entry.entry_code = entry.form_code
    steel_typeid = int(steel_typeid)
    if steel_typeid == 1:
        items = entry.barsteelmaterialpurchasingentry_set.all()
    elif steel_typeid == 0:
        items = entry.boardsteelmaterialpurchasingentry_set.all()
    context = {
            "entry":entry,
            "entry_set":items,
            "entry_type":entry_typeid,
    }
    print steel_typeid
    if steel_typeid:
        return render(request,"purchasing/widgets/purchasing_arrival_confirm_bar.html",context)
    else:
        return render(request,"purchasing/widgets/purchasing_arrival_confirm_board.html",context)
def auxiliaryToolEntryConfirm(request,eid,entry_typeid):
    entry = AuxiliaryToolEntryCardList.objects.get(id = eid)
    entry.entry_code = entry.index
    entry.entry_status = entry.status
    items = AuxiliaryToolEntryCard.objects.filter(card_list = entry)
    context = {
            "entry":entry,
            "sub_objects":items,
            "entry_type":entry_typeid,
    }
    return render(request,"purchasing/widgets/purchasing_arrival_confirm_auxi.html",context)
def outsideEntryConfirm(request,eid,entry_typeid):
    entry = OutsideStandardEntry.objects.get(id = eid)
    items = OutsideStandardItem.objects.filter(entry = entry)
    context = {
            "entry":entry,
            "entry_set":items,
            "entry_type":entry_typeid,
    }
    return render(request,"purchasing/widgets/purchasing_arrival_confirm_outside.html",context)

def inventoryTableViews(request):
    order_index = request.GET.get("order_index")
    tableid = request.GET.get("tableid")
    order = SubWorkOrder.objects.get(id = order_index)
    inventoryType = InventoryType.objects.get(name = tableid)
    context = {"order": order,
               "inventoryType": inventoryType,
    }
    return render(request, "purchasing/inventory_table_base.html", context)

def materialEntryViews(request,bid):
    context = {
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
    target=request.GET.get("target")
    order_form = OrderForm.objects.get(order_id = index)
    
    items=MaterielCopy.objects.filter(materielformconnection__order_form__order_id=index)
    print target
    context = {
        "order_form": order_form,
        "items":items,
        'target':target
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

    
def materielExecuteDetailViews(request, choice, source, *mid):
    """
    mxl
    summary : click into add or view html
    params : choice : view(0) or add(1) detail
             source : click source , from techdata or purchasing(use in view ,where choice = 1)
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
            "executeForm" : executeForm,
            "source" : source,
            "materielexecute":materielexecute
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
            tech_requirement=materielexecute.tech_requirement
            

        except:
            executeForm = MaterielExecuteForm()
            materiel_choice=MAIN_MATERIEL
            materielexecute_detail_set=None
            tech_requirement=""
            
        materiels=MaterielExecuteDetail.objects.filter(materiel__inventory_type__name=materiel_choice,materiel_execute__isnull=True)
        context = {
            "materielexecute_detail_set" : materielexecute_detail_set,
            "choice" : materiel_choice,
            "MAIN_MATERIEL" : MAIN_MATERIEL,
            "MaterielExecuteForm" : executeForm,
            "materiels":materiels,
            "source" : source,
            "tech_requirement":tech_requirement
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

@csrf.csrf_protect
def arrivalInspectionViews(request):
    """
    shen Lian
    """
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
    """
    shen Lian
    """
    cargo_set = ArrivalInspection.objects.filter(bidform__bid_id = bid,check_pass=False)
    is_show = BidForm.objects.filter(bid_id = bid , bid_status__part_status = BIDFORM_PART_STATUS_CHECK).count() > 0
    entrytypeform = EntryTypeForm()
    context = {
        "cargo_set":cargo_set,
        "bidform":BidForm.objects.get(bid_id=bid),
        "is_show":is_show,
        "entrytype":entrytypeform,
    }
    return render(request,"purchasing/purchasing_arrivalcheck.html",context)

def bidApplyFormViews(request,bid):
    bidform = BidForm.objects.get(bid_id = bid)
    try:
        bid_apply = bidform.bidapply
    except:
        status=CommentStatus.objects.get(status=BIDFORM_PART_STATUS_INVITE_BID_APPLY_FILL)
        bid_apply=bidApply(bid=bidform,status=status,work_order=bidform.order_form.work_order)
        bid_apply.save()
    bidApplyForm = BidApplyForm(instance=bid_apply)
    supplier_set=bidform.supplierselect_set.all()
    comment_dict={}
    for k in COMMENT_USER_DICT:
        comment=BidComment.objects.filter(bid=bidform,user_title=COMMENT_USER_DICT[k])
        if comment.count()>0:
            comment_dict[k]=comment[0]
    for item in supplier_set:
        item.form=BidApplySupplierForm(instance=item)

    context={
        "bid_apply":bid_apply,
        "bidApplyForm":bidApplyForm,
        "BidLogisticalForm":BidLogisticalForm,
        "supplier_set":supplier_set,
        "status_dic":BIDFORM_INVITE_BID_APPLY_DIC,
        "comment_user_dict":COMMENT_USER_DICT,
        "comment_dict":comment_dict
    }
    return render(request,"purchasing/bid_invite/bid_apply_page.html",context)

def SupplierCheckViews(request,bid):
    bidform = BidForm.objects.get(bid_id = bid)
    try:
        supplier_check = bidform.suppliercheck
    except:    
        status=CommentStatus.objects.get(status=BIDFORM_PART_STATUS_INVITE_BID_CHECK_FILL)
        supplier_check=SupplierCheck(bid=bidform,status=status)
        supplier_check.save()
    supplier_check_form=SupplierCheckForm(instance=supplier_check)
    supplier_set=bidform.supplierselect_set.all()
    comment_dict={}
    for k in COMMENT_USER_DICT:
        comment=BidComment.objects.filter(bid=bidform,user_title=COMMENT_USER_DICT[k])
        if comment.count()>0:
            comment_dict[k]=comment[0]

    for item in supplier_set:
        item.form=SupplierCheckSupplierForm(instance=item)
    context={
        "supplier_check":supplier_check,
        "supplier_check_form":supplier_check_form,
        "supplier_set":supplier_set,
        "status_dic":BIDFORM_INVITE_BID_SUPPLIER_DIC,
        "comment_user_dict":COMMENT_USER_DICT,
        "comment_dict":comment_dict
    }
    return render(request,"purchasing/bid_invite/supplier_check_page.html",context)

def QualityCardViews(request,bid):
    bidform = BidForm.objects.get(bid_id = bid)
    try:
        quality_card = bidform.qualitypricecard
    except:    
        status=CommentStatus.objects.get(status=BIDFORM_PART_STATUS_INVITE_BID_QUALITY_FILL)
        quality_card=qualityPriceCard(bid=bidform,status=status,work_order=bidform.order_form.work_order)
        quality_card.save()
    quality_card_form=QualityPriceCardForm(instance=quality_card)
    supplier_set=bidform.supplierselect_set.all()
    comment_dict={}
    for k in COMMENT_USER_DICT:
        comment=BidComment.objects.filter(bid=bidform,user_title=COMMENT_USER_DICT[k])
        if comment.count()>0:
            comment_dict[k]=comment[0]

    for item in supplier_set:
        item.form=QualityCardSupplierForm(instance=item)
    context={
        "quality_card":quality_card,
        "quality_card_form":quality_card_form,
        "supplier_set":supplier_set,
        "status_dic":BIDFORM_INVITE_BID_QUALITY_DIC,
        "comment_user_dict":COMMENT_USER_DICT,
        "comment_dict":comment_dict
    }
    return render(request,"purchasing/bid_invite/quality_card_page.html",context)

