#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from techdata.models  import *

RegisterClass = (
    CirculationRoute,
    CirculationName,
    ProcessReview,
    Processing,
    ProcessingName,
    WeldSeam,
    WeldSeamType,
    WeldPositionType,
    WeldMethod,
    NondestructiveInspection,
    WeldListPageMark,
    TransferCard,
    TransferCardMark,
    ProcessBOMPageMark,
    Program,
    HeatTreatmentTechCard,
    HeatTreatmentArrangement,
    HeatTreatmentMateriel,
    DesignBOMMark,
    TechPlan,
    WeldQuotaPageMark,
    ConnectOrientation,
    WeldCertification,
    ProcedureQualificationIndex,
    WeldJointTechDetail,
    OutPurchasedItem,
    WeldQuota,
    OutPurchasedMark,
    FirstFeedingItem,
    FirstFeedingMark,
    AuxiliaryItem,
    AuxiliaryMark,
    CooperantItem,
    CooperantMark,
    PrincipalItem,
    PrincipalMark,
    TransferCardProcess,
    WeldingProcessSpecification,
    WeldingWorkInstruction,
    WeldingWorkInstructionProcess,
    WeldingStep,
)

for item in RegisterClass:
    admin.site.register(item)
