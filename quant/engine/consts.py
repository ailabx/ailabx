from enum import Enum
class EventType(Enum):
    onstart = 0
    onbar = 1,
    onfinished = 2,
    onmessage = 3,

class ShowTypes(Enum):
    alloc_funds_cash_equally = 20,

    pick_symbol_fixed = 30, #指定symbols


    benchmark_self = 10,
    benchmark_spy = 11


benchmark_types = {
    ShowTypes.benchmark_self:'买入并持有自身',
    ShowTypes.benchmark_spy:'买入并持用标普'
}

pick_symbol_types = {
    ShowTypes.pick_symbol_fixed:'指定股票池'
}

alloc_funds_types = {
    ShowTypes.alloc_funds_cash_equally:'可用资金平均分配'
}

def get_type_by_text(types,text):
    if text in types.values():
        for k,v in types.items():
            if v == text:
                return k
    return None