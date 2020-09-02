from abc import abstractmethod

from checkov.common.checks.base_check import BaseCheck
from checkov.common.multi_signature import multi_signature
from checkov.serverless.registry import sls_registry


class BaseFunctionCheck(BaseCheck):
    def __init__(self, name, id, categories, supported_entities):
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_entities,
                         block_type="serverless")
        self.supported_entities = supported_entities
        sls_registry.register(self)

    def scan_entity_conf(self, conf, entity_type):
        return self.scan_function_conf(conf, entity_type)

    @abstractmethod
    @multi_signature()
    def scan_function_conf(self, conf, entity_type):
        raise NotImplementedError()

    @classmethod
    @scan_function_conf.add_signature(args=["self", "conf"])
    def _scan_function_conf_self_conf(cls, wrapped):
        def wrapper(self, conf, entity_type=None):
            # keep default argument for entity_type so old code, that doesn't set it, will work.
            return wrapped(self, conf)

        return wrapper
