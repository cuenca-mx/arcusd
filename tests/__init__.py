import logging

from arcusd.exc import UnknownServiceProvider

logging.basicConfig()

vcr_log = logging.getLogger('vcr')
vcr_log.setLevel(logging.DEBUG)


def mock_get_arcus_mapping(service_provider_code):
    if service_provider_code == 'cable_izzi':
        return 6900
    elif service_provider_code == 'cable_megacable':
        return 1821
    elif service_provider_code == 'electricity_cfe':
        return 35
    elif service_provider_code == 'topup_att':
        return 13599
    elif service_provider_code == 'topup_movistar':
        return 13597
    elif service_provider_code == 'topup_telcel':
        return 13603
    elif service_provider_code == 'invoice_att':
        return 2901
    elif service_provider_code == 'invoice_movistar':
        return 5985
    elif service_provider_code == 'invoice_telcel':
        return 2931
    elif service_provider_code == 'internet_telmex':
        return 37
    elif service_provider_code == 'internet_axtel':
        return 1781
    elif service_provider_code == 'internet_axtel_barcode':
        return 36
    elif service_provider_code == 'satellite_tv_sky':
        return 40
    else:
        raise UnknownServiceProvider()
