# HW5 — Sales Data Cleaning and Analysis

**Student name:** Toshboev Utkirbek Uktam Ugli 
**Student ID:** 23012866  
**Course:** Web-Based Systems

## How to run

1. Put `hw5.ipynb` and `sales_data.csv` in the same folder.
2. Open the folder in Jupyter Notebook or VS Code with a Python kernel.
3. Ensure Pandas and Matplotlib are installed: `pip install pandas matplotlib notebook`.
4. Select **Kernel → Restart & Run All**. Verify all seven steps finish without errors.
5. Save the notebook with its cell outputs. Step ④ saves `sales_clean.csv`.

## Steps ①–④ — Cleaning decisions and evidence

| Check | Action | Before | After | Reason |
|---|---|---|---|---|
| Read and parse dates | Load CSV; parse 3 date columns | 1,030 rows, 14 columns | Same | Dates must support subtraction and comparisons. |
| Missing age, satisfaction and arrival dates | Leave missing values unchanged | 51 / 30 / 5 missing | Same | There is no reliable basis for inventing values; imputation could distort analysis. |
| Exact duplicates | Drop duplicates | 1,030 rows | 1,004 rows | 26 duplicated records should not be counted twice. |
| Quantity > 100 | Restore quantity as `total_sales / unit_price` | 22 suspicious quantities; maximum 990 | Corrected 22; maximum 99; 0 sales mismatches | The amount/price ratio gives the original whole-number quantity. |
| Arrival earlier than shipment | Flag `date_error`, do not change the dates | 149 errors before duplicate removal | 147 flagged rows | The data cannot establish which date is wrong. |
| Save result | Export `sales_clean.csv` | 14 columns | 1,004 rows × 15 columns | Add `date_error` without changing source CSV. |

## Step ⑤ — Typical delivery duration

Among **852** records with valid nonmissing, nonreversed dates, the mean is **22.05 days**, while the median is **2 days**; **47** orders fall in a separate 364–370-day cluster.  
This near-one-year cluster looks suspicious, but the true dates cannot be verified. I retain it in `sales_clean.csv` and exclude it only from the typical-duration estimate, yielding **mean 1.93 days and median 2 days** across 805 orders.

## Step ⑥ — Satisfaction versus returns

The return rate is **7.59%** at satisfaction 1, **11.96%** at 2, and **6.93%** at 5.  
There is **no consistent monotonic pattern**: satisfaction 2 has the highest return rate (11.96%), rather than satisfaction 1.

## Step ⑦ — Why the leading sales category ranks first

**Furniture (가구)** leads with **28.43억 원** in total sales, ahead of **Food (식품)** at **25.13억 원**.  
Their order counts (**213 vs 210**) and average unit prices (**₩257,323 vs ₩255,233**) are similar, while Furniture has a higher **average quantity (51.04 vs 47.31)**. Average quantity shows the largest relative difference among these three factors versus the runner-up, helping explain the sales gap.

## Submitted files

- `hw5.ipynb` (executed and saved with charts/tables)
- `sales_data.csv` (original input)
- `sales_clean.csv` (Step ④ output)
- `README.md` (this document)
