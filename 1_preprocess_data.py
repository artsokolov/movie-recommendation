import polars as pl

def decompress_data(source: str, save_to: str, debug: bool = False) -> pl.DataFrame:
    """
    Decompress the gzipped TSV file and load it into a Polars DataFrame.
    """
    df = pl.read_csv(
        source=source,
        separator="\t",
        null_values=["\\N"],
        quote_char=None,
    )

    if debug:
        # Print the first few rows of the DataFrame for debugging
        print(df.head(5))
        print()

    if save_to:
        # Save the DataFrame to a Parquet file
        df.write_parquet(save_to)
        print(f"Data saved to {save_to}")

    return df

def load_data(source: str, debug: bool = False) -> pl.DataFrame:
    """
    Load the Parquet file into a Polars DataFrame.
    """
    # Load the Parquet file into a Polars DataFrame
    df = pl.read_parquet(source)

    if debug:
        # Print the first few rows of the DataFrame for debugging
        print(df.head(5))
        print()

    return df

def extract_data(df: pl.DataFrame, save_to: str, debug: bool = False) -> pl.DataFrame:
    """
    Extract  columns tconst, primaryTitle, originalTitle from the DataFrame where titleType is 'movie' and startYear is later than 2000.
    """

    # Select specific tconst, primaryTitle, originalTitle where titleType is 'movie', dont include titleType
    df = df.filter(
        (pl.col("titleType") == "movie") & 
        (pl.col("startYear") > 2000)
    ).select(
        pl.col("tconst"),
        pl.col("primaryTitle"),
        pl.col("originalTitle")
    )

    if debug:
        # Print the first few rows of the extracted DataFrame for debugging
        print(df.head(5))
        print()

    if save_to:
        # Save the extracted DataFrame to a Parquet file
        df.write_parquet(save_to)
        print(f"Data saved to {save_to}")

        # Save the DataFrame to a CSV file
        df.write_csv(save_to.replace(".parquet", ".csv"))
        print(f"Data saved to {save_to.replace('.parquet', '.csv')}")

    return df

def print_dataframe_info(df: pl.DataFrame):
    """
    Print information about the DataFrame.
    """
    print(f"Shape of the DataFrame: {df.shape}")
    print(f"Columns: {df.columns}")
    print(f"Number of rows: {df.height}")
    print(f"Number of columns: {df.width}")

    print(df.head(5))
    print()

    # df2 is the rows that primaryTitle and originalTitle are not the same
    df2 = df.filter(pl.col("primaryTitle") != pl.col("originalTitle"))
    print(f"Number of rows where primaryTitle != originalTitle: {df2.height}")
    print(df2.head(5))
    print()

if __name__ == "__main__":
    decompress_data(source="raw_data/title_basics.tsv.gz", save_to="raw_data/title_basics.parquet", debug=True)
    df = load_data(source="raw_data/title_basics.parquet", debug=True)
    df = extract_data(df, save_to="data/title_basics_extracted.parquet", debug=True)
    print_dataframe_info(df)
    