"""
Biology and bioinformatics-oriented data cleaning functions.
"""

import pandas as pd
import pandas_flavor as pf

from .utils import deprecated_alias, import_message

try:
    from Bio import SeqIO
except ImportError:
    import_message(
        "biology", "biopython", "conda install -c conda-forge biopython"
    )


@pf.register_dataframe_method
@deprecated_alias(col_name="column_name")
def join_fasta(
    df: pd.DataFrame, filename: str, id_col: str, column_name
) -> pd.DataFrame:
    """
    Convenience method to join in a FASTA file as a column.

    This allows us to add the string sequence of a FASTA file as a new column
    of data in the dataframe.

    This method only attaches the string representation of the SeqRecord.Seq
    object from Biopython. Does not attach the full SeqRecord. Alphabet is
    also not stored, under the assumption that the data scientist has domain
    knowledge of what kind of sequence is being read in (nucleotide vs. amino
    acid.)

    This method mutates the original DataFrame.

    For more advanced functions, please use phylopandas.

    :param df: A pandas DataFrame.
    :param filename: Path to the FASTA file.
    :param id_col: The column in the DataFrame that houses sequence IDs.
    :param column_name: The name of the new column.
    """
    seqrecords = {
        x.id: x.seq.__str__() for x in SeqIO.parse(filename, "fasta")
    }
    seq_col = [seqrecords[i] for i in df[id_col]]
    df[column_name] = seq_col
    return df
