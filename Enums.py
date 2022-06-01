from enum import Enum

class Filter(Enum):
    Mass = 1
    Intensity = 2
    RetentionTime = 3
    NumberDetections = 4
    Annotations = 5
    Probability = 6
    Sort = 7
    SortTimeSeries = 8

class Plot(Enum):
    Peak = 1
    DerivativesAll = 2
    DerivativesLog = 3
    IntensityPatternAll = 4
    IntensityPatternTrend = 5
    FragmentationConsensus = 6
    FragmentationSample = 7
