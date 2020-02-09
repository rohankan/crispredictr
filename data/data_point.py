from typing import List, NamedTuple

TempEditOutcome = NamedTuple(
    'TempEditOutcome', [
        ('indel_start', int),
        ('indel', int),
        ('num_reads', int)
    ]
)


class EditOutcome:
    """
    Class for one potential gene editing outcome.
    """
    @staticmethod
    def from_temp(temp: TempEditOutcome,
                  percentage: float) -> 'EditOutcome':
        """
        Create EditOutcome from TempEditOutcome.
        :param temp: Temporary edit outcome
        :param percentage: Percentage to add in
        :return: EditOutcome
        """
        return EditOutcome(temp.indel_start, temp.indel, temp.num_reads, percentage)

    def __init__(self,
                 indel_start: int,
                 indel: int,
                 num_reads: int,
                 percentage: float) -> None:
        """
        :param indel_start: Indel start point relative to cut site
        :param indel: Net indel
        :param num_reads: Counts of indel
        """
        self.indel_start: int = indel_start
        self.indel: int = indel
        self.num_reads: int = num_reads
        self.percentage: float = percentage

    def __repr__(self) -> str:
        return f'(istart: {self.indel_start}, indel: {self.indel}, ' \
               f'nreads: {self.num_reads}, %: {round(self.percentage * 100, 2)})'


class DataPoint:
    """
    Input/output data point for machine learning. Serialize / deserialize with pickle.
    """
    CSV_ATTRIBUTES: List[str] = ['name', 'file_name', 'guide_rna', 'pam_site', 'cut_site',
                                 'neighborhood', 'total_reads', 'events']
    CSV_HEADER: str = ','.join(x.capitalize() for x in CSV_ATTRIBUTES)

    def __init__(self,
                 name: str,
                 file_name: str,
                 guide_rna: str,
                 pam_site: str,
                 cut_site: int,
                 neighborhood: str,
                 total_reads: int,
                 events: List[TempEditOutcome]) -> None:
        """
        :param name: Sample name
        :param file_name: General file name from which sample came from
        :param guide_rna: Guide RNA sequence (in DNA bases)
        :param pam_site: PAM site (in DNA bases)
        :param cut_site: Cut site location relative to start of neighborhood
        :param neighborhood: DNA sequence neighborhood
        :param total_reads: Total number of NGS reads
        :param events: List of indel outcomes
        """
        self.name: str = name
        self.file_name: str = file_name
        self.guide_rna: str = guide_rna
        self.pam_site: str = pam_site
        self.cut_site: int = cut_site
        self.neighborhood: str = neighborhood
        self.total_reads: int = total_reads
        self.events: List[EditOutcome] = [EditOutcome.from_temp(x, x.num_reads / total_reads) for x in events]

    def __repr__(self) -> str:
        return f'<DataPoint\n\tname={self.name}\n\tseq={self.neighborhood}\n\t' \
               f'total_reads={self.total_reads}\n\t'  # events={[str(x) for x in self.events]}'

    def to_csv(self) -> str:
        return ','.join(str(self.__getattribute__(attr)) for attr in DataPoint.CSV_ATTRIBUTES)
