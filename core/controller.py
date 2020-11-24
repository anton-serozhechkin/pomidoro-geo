customer_address_parameters = ['lon', 'lat']
#def _check_params_exists(params):

def _check_adress_param_exists(params):
    for item in customer_address_parameters:
        if item in params and bool(params[item]):
            print('yes')
        else:
            print('no')

