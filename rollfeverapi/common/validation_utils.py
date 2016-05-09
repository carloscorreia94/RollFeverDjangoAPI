
def check_args(dict,args):
    for key in args:
        if key not in dict.keys():
            return False
    return True

def output_success(type,data=None):
    return {'status':'success','type':type,'data': data}


def output_error(type,data=None):
    return {'status':'error','type':type,'data': data}