from Policy import *


class TestPolicy:
    def testPolicy01(self):
        policy = Policy()
        prefix = "BNBUSDT"
        coinKind = "BNB"
        policy.policy_01(1617467400, 1618367400, prefix, 1)
        assert (policy.totalMoney[coinKind] == 1206.1725999999987), "policy_01有误"

    def testPolicy02(self):
        policy = Policy()
        prefix = "BNBUSDT"
        coinKind = "BNB"
        policy.policy_02(1617467400, 1618367400, prefix, 1)
        assert (policy.totalMoney[coinKind] == 1193.1141999999973), "policy_02有误"

