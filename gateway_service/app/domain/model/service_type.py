# service_type.py
import os
from enum import Enum

class ServiceType(str, Enum):
    ACTLOG = "actlog"
    COMPANY = "company"
    DSDGEN = "dsdgen"
    USER = "user"
    XBRLGEN = "xbrlgen"

SERVICE_URLS = {
    ServiceType.ACTLOG: os.getenv("ACTLOG_SERVICE_URL"),
    ServiceType.COMPANY: os.getenv("COMPANY_SERVICE_URL"),
    ServiceType.DSDGEN: os.getenv("DSDGEN_SERVICE_URL"),
    ServiceType.USER: os.getenv("USER_SERVICE_URL"),
    ServiceType.XBRLGEN: os.getenv("XBRLGEN_SERVICE_URL"),
}
