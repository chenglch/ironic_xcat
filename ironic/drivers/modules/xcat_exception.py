"""xCAT baremtal exceptions.
"""

from oslo.config import cfg
import six

from ironic.openstack.common.gettextutils import _
from ironic.openstack.common import log as logging
from ironic.common.exception import IronicException
LOG = logging.getLogger(__name__)

class xCATCmdFailure(IronicException):
    message = _("xcat call failed: %(cmd)s %(node)s %(args)s.")

class xCATDeploymentFailure(IronicException):
    message = _("xCAT node deployment failed for node %(node)s:%(error)s")