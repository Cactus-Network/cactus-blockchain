from cactus.util.ints import uint32, uint64

# 1 Cactus coin = 1,000,000,000,000 = 1 trillion mojo.
_mojo_per_cactus = 1000000000000
_blocks_per_year = 1681920  # 32 * 6 * 24 * 365


def calculate_pool_reward(height: uint32) -> uint64:
    """
    Returns the pool reward at a certain block height. The pool earns 7/8 of the reward in each block. If the farmer
    is solo farming, they act as the pool, and therefore earn the entire block reward.
    These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously.
    """

    return uint64(int(0))

    """
    if height == 0:
        return uint64(int((7 / 8) * 210000 * _mojo_per_cactus))
    elif height < 3 * _blocks_per_year:
        return uint64(int((7 / 8) * 2 * _mojo_per_cactus))
    elif height < 6 * _blocks_per_year:
        return uint64(int((7 / 8) * 1 * _mojo_per_cactus))
    elif height < 9 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.5 * _mojo_per_cactus))
    elif height < 12 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.25 * _mojo_per_cactus))
    else:
        return uint64(int((7 / 8) * 0.125 * _mojo_per_cactus))
    """

def calculate_base_farmer_reward(height: uint32) -> uint64:
    """
    Returns the base farmer reward at a certain block height.
    The base fee reward is 1/8 of total block reward

    Returns the coinbase reward at a certain block height. These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously.
    """
    if height == 0:
        return uint64(210000 * _mojo_per_cactus)
    elif height < 3 * _blocks_per_year:
        return uint64(2 * _mojo_per_cactus)
    elif height < 6 * _blocks_per_year:
        return uint64(1 * _mojo_per_cactus)
    elif height < 9 * _blocks_per_year:
        return uint64(0.5 * _mojo_per_cactus)
    elif height < 12 * _blocks_per_year:
        return uint64(0.25 * _mojo_per_cactus)
    else:
        return uint64(0.125 * _mojo_per_cactus)
