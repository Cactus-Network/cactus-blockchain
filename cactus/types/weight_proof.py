from __future__ import annotations

from dataclasses import dataclass
from typing import List

import cactus_rs

from cactus.types.blockchain_format.reward_chain_block import RewardChainBlock
from cactus.types.end_of_slot_bundle import EndOfSubSlotBundle
from cactus.types.header_block import HeaderBlock
from cactus.util.streamable import Streamable, streamable

SubEpochData = cactus_rs.SubEpochData

# number of challenge blocks
# Average iters for challenge blocks
# |--A-R----R-------R--------R------R----R----------R-----R--R---|       Honest difficulty 1000
#           0.16

#  compute total reward chain blocks
# |----------------------------A---------------------------------|       Attackers chain 1000
#                            0.48
# total number of challenge blocks == total number of reward chain blocks


SubEpochChallengeSegment = cactus_rs.SubEpochChallengeSegment
SubEpochSegments = cactus_rs.SubEpochSegments
SubSlotData = cactus_rs.SubSlotData


@streamable
@dataclass(frozen=True)
# this is used only for serialization to database
class RecentChainData(Streamable):
    recent_chain_data: List[HeaderBlock]


@streamable
@dataclass(frozen=True)
class ProofBlockHeader(Streamable):
    finished_sub_slots: List[EndOfSubSlotBundle]
    reward_chain_block: RewardChainBlock


@streamable
@dataclass(frozen=True)
class WeightProof(Streamable):
    sub_epochs: List[SubEpochData]
    sub_epoch_segments: List[SubEpochChallengeSegment]  # sampled sub epoch
    recent_chain_data: List[HeaderBlock]
