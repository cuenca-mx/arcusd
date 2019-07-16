import sys

sys.path.append('/arcusd')

from arcusd.data_access.providers_mapping import add_mapping, \
    get_service_provider_code, get_biller_id

add_mapping('cable_izzi', 6900)
add_mapping('cable_megacable', 1821)
add_mapping('electricity_cfe', 35)
add_mapping('topup_att', 13599)
add_mapping('topup_movistar', 13597)
add_mapping('topup_telcel', 13603)
add_mapping('invoice_att', 2901)
add_mapping('invoice_movistar', 5985)
add_mapping('invoice_telcel', 2931)
add_mapping('internet_telmex', 37)
add_mapping('internet_axtel', 1781)
add_mapping('internet_axtel_barcode', 36)
add_mapping('satellite_tv_sky', 40)
print('lo hizo')
print(get_service_provider_code(6900))
print(get_biller_id('satellite_tv_sky'))
