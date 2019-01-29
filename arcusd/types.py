from enum import Enum


class OperationStatus(Enum):
    none = 'none'
    success = 'success'
    failed = 'failed'


class OperationType(Enum):
    query = 'query'
    payment = 'payment'
    topup = 'topup'


class ServiceProvider(Enum):
    cable_izzi = 6900
    cable_megacable = 1821
    electricity_cfe = 35
    topup_att = 13599
    topup_movistar = 13597
    topup_telcel = 13603
    invoice_att = 2901
    invoice_movistar = 5985
    invoice_telcel = 2931
    internet_telmex = 37
    internet_axtel = 1781
    internet_axtel_barcode = 36
    satellite_tv_sky = 40
