class FBPoolVerbose:

    def __init__(self,quiet=None):
        self.quiet = True if quiet == None else quiet

    def start(self,operation):
        if self.quiet:
            return
        print ""
        print operation

    def done(self,operation):
        if self.quiet:
            return
        print "%s done." % (operation)
        print ""

    def update(self,message):
        if self.quiet:
            return
        print " : %s" % (message)
