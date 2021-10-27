import pandas as pd

# Global for now in case we want to use it in many places
TOP_SIZE = 5


def csv_to_df(csv_file: str) -> pd.DataFrame:
    """
    Converts CSV file to Pandas DataFrame to work with
    Here we can add import options to optimize if necessary
    """
    return pd.read_csv(csv_file)


def get_top_customers(vouchers_df: pd.DataFrame, top_size: int) -> None:
    """
    Sort out DataFrame to get customers who bought the most tickets
    with a given top size
    """
    top_df = vouchers_df.groupby("customer_id")
    top_df = top_df.size().reset_index(name="counts")
    top_df = top_df.sort_values("counts", ascending=False)

    print(f"Top {top_size} customers: [customer id, number of tickets]")
    index = 0
    for index in range(0, top_size):
        customer_id = top_df.iloc[index]["customer_id"]
        number_of_tickets = top_df.iloc[index]["counts"]
        print(f"{customer_id}, {number_of_tickets}")


def get_count_unused_barcodes(barcodes_df: pd.DataFrame) -> None:
    """
    Counts unused barcodes by checking barcodes with no order_id
    """
    unused_barcodes = barcodes_df.isnull().values.ravel().sum()
    print(f"Number of unused barcodes {unused_barcodes}")


def main():
    orders_df = csv_to_df("data/orders.csv")
    barcodes_df = csv_to_df("data/barcodes.csv")

    print("Number of orders rows", len(orders_df.index))
    print("Number of barcodes rows", len(barcodes_df.index))

    ## NOTE: This section acts as validation by removing duplicates and merging
    ## dataframes only with valid entries for now, it could be move in its own
    ## method for more granularity
    # DEDUPLICATE
    barcodes_df = barcodes_df.drop_duplicates(subset=["barcode"])
    print("Number of barcodes rows with dropped duplicates", len(barcodes_df.index))

    # MERGE
    vouchers_df = pd.merge(orders_df, barcodes_df, how="inner", on="order_id")
    vouchers_df = vouchers_df[["customer_id", "order_id", "barcode"]]

    # BONUSES
    get_top_customers(vouchers_df, TOP_SIZE)
    get_count_unused_barcodes(barcodes_df)

    grouped_df = vouchers_df.groupby(["customer_id", "order_id"])
    grouped_lists = grouped_df["barcode"].apply(list)
    grouped_lists = grouped_lists.reset_index()

    # Generates CSV file with vouchers following:
    # customer_id,order_id,[barcodes]
    grouped_lists.to_csv("vouchers.csv")


if __name__ == "__main__":
    main()
