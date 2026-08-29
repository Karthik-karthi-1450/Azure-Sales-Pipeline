import pandas as pd
import os

# ============================================================
# 1. READ SOURCE DATA
# ============================================================

df = pd.read_csv("Data/sales.csv")

source_count = len(df)

print("Source row count:", source_count)


# ============================================================
# 2. CONVERT DATA TYPES
# ============================================================

df["order_id"] = pd.to_numeric(
    df["order_id"],
    errors="coerce"
)

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

df["quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)

df["unit_price"] = pd.to_numeric(
    df["unit_price"],
    errors="coerce"
)


# ============================================================
# 3. REMOVE DUPLICATES
# ============================================================

duplicate_count = df.duplicated().sum()

df = df.drop_duplicates()

print("Duplicate records:", duplicate_count)


# ============================================================
# 4. IDENTIFY DATA QUALITY ISSUES
# ============================================================

missing_quantity = df["quantity"].isna()

negative_quantity = df["quantity"] < 0

invalid_price = df["unit_price"] <= 0

missing_order_id = df["order_id"].isna()

invalid_order_date = df["order_date"].isna()

missing_customer = df["customer_id"].isna()


# ============================================================
# 5. CREATE REJECTED DATA
# ============================================================

rejected_data = df[
    missing_quantity
    | negative_quantity
    | invalid_price
    | missing_order_id
    | invalid_order_date
    | missing_customer
].copy()


# ============================================================
# 6. ADD REJECTION REASON ONLY TO REJECTED DATA
# ============================================================

rejected_data["rejection_reason"] = ""

rejected_data.loc[
    rejected_data["quantity"].isna(),
    "rejection_reason"
] = "MISSING_QUANTITY"

rejected_data.loc[
    rejected_data["quantity"] < 0,
    "rejection_reason"
] = "NEGATIVE_QUANTITY"

rejected_data.loc[
    rejected_data["unit_price"] <= 0,
    "rejection_reason"
] = "INVALID_UNIT_PRICE"

rejected_data.loc[
    rejected_data["order_id"].isna(),
    "rejection_reason"
] = "MISSING_ORDER_ID"

rejected_data.loc[
    rejected_data["order_date"].isna(),
    "rejection_reason"
] = "INVALID_ORDER_DATE"

rejected_data.loc[
    rejected_data["customer_id"].isna(),
    "rejection_reason"
] = "MISSING_CUSTOMER_ID"


# ============================================================
# 7. CREATE CLEAN DATA
# ============================================================

clean_df = df[
    ~(
        missing_quantity
        | negative_quantity
        | invalid_price
        | missing_order_id
        | invalid_order_date
        | missing_customer
    )
].copy()


# ============================================================
# 8. CALCULATE REVENUE
# ============================================================

clean_df["revenue"] = (
    clean_df["quantity"]
    * clean_df["unit_price"]
)


# ============================================================
# 9. CREATE OUTPUT FOLDERS
# ============================================================

os.makedirs(
    "Data/Processed",
    exist_ok=True
)

os.makedirs(
    "Data/Quarantine",
    exist_ok=True
)


# ============================================================
# 10. SAVE CLEAN DATA
# ============================================================

clean_df.to_csv(
    "Data/Processed/clean_sales.csv",
    index=False
)


# ============================================================
# 11. SAVE REJECTED DATA
# ============================================================

rejected_data.to_csv(
    "Data/Quarantine/rejected_sales.csv",
    index=False
)


# ============================================================
# 12. DATA QUALITY REPORT
# ============================================================

clean_count = len(clean_df)

rejected_count = len(rejected_data)

print("\n====================================")
print("DATA QUALITY REPORT")
print("====================================")

print("Source records:", source_count)

print("Duplicate records:", duplicate_count)

print(
    "Records after deduplication:",
    len(df)
)

print("Clean records:", clean_count)

print("Rejected records:", rejected_count)

print("\nRejection reasons:")

print(
    "Missing quantity:",
    missing_quantity.sum()
)

print(
    "Negative quantity:",
    negative_quantity.sum()
)

print(
    "Invalid unit price:",
    invalid_price.sum()
)

print(
    "Missing order ID:",
    missing_order_id.sum()
)

print(
    "Invalid order date:",
    invalid_order_date.sum()
)

print(
    "Missing customer ID:",
    missing_customer.sum()
)

print("\n====================================")
print("PIPELINE COMPLETED")
print("====================================")

print(
    "Clean data:",
    "Data/Processed/clean_sales.csv"
)

print(
    "Rejected data:",
    "Data/Quarantine/rejected_sales.csv"
)