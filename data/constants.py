from processing import sequence_to_one_hots, sequence_to_ordinals


MIN_INDEL = -30
MAX_INDEL = +5


INDEL_RANGE = list(range(MIN_INDEL, MAX_INDEL+1))


SEQUENCE_MAPPER = sequence_to_ordinals
