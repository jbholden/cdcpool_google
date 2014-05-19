class APIException(Exception):
    def __init__(self,http_code,errmsg):
        self.http_code = http_code
        self.errmsg = errmsg

    def __str__(self):
        return "%d: %s" % (self.http_code,self.errmsg)
