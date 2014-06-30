class FBPoolError:

    @classmethod
    def exit_with_error(operation,fbapi_exception,additional_message=None):
        FBPoolError.__print_error(operation,fbapi_exception,additional_message)
        sys.exit(1)

    @classmethod
    def error_no_exit(operation,fbapi_exception,additional_message=None):
        FBPoolError.__print_error(operation,fbapi_exception,additional_message)

    @classmethod
    def load_error(name,fbapi_exception):
        operation = "loading %s" % (name)
        additional_message = "Database data may be in invalid state."
        FBPoolError.exit_with_error(operation,fbapi_exception,additional_message)

    @classmethod
    def __print_error(operation,fbapi_exception,additional_message=None):
        print "**ERROR** Encountered error when %s" % (operation)
        print "---------------------------------------------"
        print "FBAPIException: code=%d, msg=%s" % (fbapi_exception.http_code,fbapi_exception.errmsg)

        if additional_message:
            print additional_message

        print ""
