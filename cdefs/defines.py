import sys

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    if sys.version_info >= (3, 0) :
        forward_dict = dict((key, value) for key, value in enums.items())
        reverse_dict = dict((value, key) for key, value in enums.items())
    else:
        forward_dict = dict((key, value) for key, value in enums.iteritems())
        reverse_dict = dict((value, key) for key, value in enums.iteritems())
    enums['forward'] = forward_dict
    enums['reverse'] = reverse_dict
    return type('Enum', (), enums)


MarketEvent_t = enum('Invalid', 'OneMinuteBar')

TradingStatus_t = enum('Invalid', 'PreOpen', 'Trading', 'PostClose')

TradeType_t = enum('Invalid', 'Buy', 'Sell')

OrderType_t = enum('Invalid', 'Limit', 'Market', 'FOK')

ExecAlgoType_t = enum('Invalid', 'Direct', 'MeanRev', 'Momentum')


def get_algo_from_str(algo_str):
    if algo_str == 'Direct':
        return ExecAlgoType_t.Direct
    elif algo_str == 'MeanRev':
        return ExecAlgoType_t.MeanRev
    elif algo_str == 'Momentum':
        return ExecAlgoType_t.Momentum
    else:
        return ExecAlgoType_t.Invalid
