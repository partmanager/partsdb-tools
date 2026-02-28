from ..packaging.PackagingBase import PackagingBase
from ..packaging.from_dict import packaging_from_dict


class OrderNumber:
    def __init__(self, order_number: str, packaging: PackagingBase):
        self.order_number: str = order_number
        self.production_status = None
        self.alias: str | None = None
        self.SKU: str | None = None
        self.EAN13 = None
        self._12NC = None
        self.packaging: PackagingBase = packaging

    def to_dict(self):
        result = {}
        if self.production_status:
            result['status'] = self.production_status
        if self.alias:
            result['alias'] = self.alias
        if self.SKU:
            result['SKU'] = self.SKU
        if self.EAN13:
            result['EAN13'] = self.EAN13
        if self._12NC:
            result['12NC'] = self._12NC
        if self.packaging:
            result.update(self.packaging.to_dict())
        return result

def order_number_from_dict(order_number: str, order_dict: dict):
    order = OrderNumber(order_number, None)
    consumed_keys = set()
    if 'status' in order_dict:
        order.production_status = order_dict['status']
        consumed_keys.update('status')
    if 'alias' in order_dict:
        order.alias = order_dict['alias']
        consumed_keys.update('alias')
    if 'SKU' in order_dict:
        order.SKU = order_dict['SKU']
        consumed_keys.update('SKU')
    if 'EAN13' in order_dict:
        order.EAN13 = order_dict['EAN13']
        consumed_keys.update('EAN13')
    if '12NC' in order_dict:
        order._12NC = order_dict['12NC']
        consumed_keys.update('12NC')

    order.packaging = packaging_from_dict(order_dict)
    return order, consumed_keys