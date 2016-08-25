from SimpleXMLRPCServer import SimpleXMLRPCServer
from security_util import expose, requires_user_privilege, requires_authentication_only, \
    requires_admin_privilege, is_exposed, is_authorized
from xen_api import XenAPI


class XenAPIExposer:
    """ This class exposes the actual xen_api with a remote RPC interface """

    def __init__(self):
        self.prefix = 'xenapi'

    def _dispatch(self, method, params):
        """ This method receives all the calls to the xen_api. Perfo """

        # check if method starts with correct prefix
        if not method.startswith(self.prefix + "."):
            raise Exception('method "%s" is not supported' % method)

        method_name = method.partition('.')[2]
        func = getattr(self, method_name)

        if not is_exposed(func):
            raise Exception('method "%s" is not supported' % method)

        is_authorized(func, params[0], params[1])

        return func(*params)

    @expose
    @requires_authentication_only
    def start_vm(self, user, passwd, vm_name, student_id, course_id):
        vm_name = student_id + '_' + course_id + '_' + vm_name
        return XenAPI().start_vm(vm_name)

    @expose
    @requires_authentication_only
    def stop_vm(self, user, passwd, vm_name, student_id, course_id):
        vm_name = student_id + '_' + course_id + '_' + vm_name
        XenAPI().stop_vm(vm_name)

    @expose
    @requires_authentication_only
    def list_all_vms(self, user, passwd):
        return XenAPI().list_all_vms()

    @expose
    @requires_authentication_only
    def list_vm(self, user, passwd, vm_name):
        return XenAPI().list_vm(vm_name)

    @expose
    @requires_authentication_only
    def register_vm(self, user, passwd, vm_name, student_id, course_id):
        XenAPI().register_vm(vm_name, student_id, course_id)

    @expose
    @requires_authentication_only
    def unregister_vm(self, user, passwd, vm_name, student_id, course_id):
        vm_name = student_id + '_' + course_id + '_' + vm_name
        XenAPI().unregister_vm(vm_name)

server = SimpleXMLRPCServer(('128.238.77.10', 8000), logRequests=True, allow_none=True)
server.register_instance(XenAPIExposer())

try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'
