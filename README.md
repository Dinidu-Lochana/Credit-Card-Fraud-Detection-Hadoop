# MapReduce: Credit Card Fraud Rate per Transaction Amount Range
## Dataset: Credit Card Fraud Detection (Kaggle)
## Course: EE7222/EC7204 Cloud Computing | University of Ruhuna

---

## Overview

This MapReduce job processes 284,807 credit card transactions to compute the
fraud rate within each transaction amount range. The goal is to identify which
amount brackets carry the highest risk of fraudulent activity.

For each amount bucket, the job outputs:
- Total number of transactions
- Number of fraud cases
- Number of normal cases
- Fraud rate (%)

---

## Dataset

- **File:** `creditcard.csv`
- **Rows:** 284,807 transactions
- **Source:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **Columns:** Time, V1–V28 (PCA features), Amount, Class
- **Class:** 0 = Normal, 1 = Fraud
- **Fraud cases:** 492 (0.17% of dataset)

### Amount Buckets

| Bucket | Range |
|--------|-------|
| 1_Bucket_$0-$10 | $0 to $9.99 |
| 2_Bucket_$10-$50 | $10 to $49.99 |
| 3_Bucket_$50-$100 | $50 to $99.99 |
| 4_Bucket_$100-$500 | $100 to $499.99 |
| 5_Bucket_$500-$1000 | $500 to $999.99 |
| 6_Bucket_$1000+ | $1000 and above |

---

## Prerequisites

- Python 3.x (for local test) / Python 2.7 (inside Hadoop Docker container)
- Docker Desktop with WSL2 backend
- `creditcard.csv` available locally

---

## Project Structure

```
.
├── mapper.py       # Hadoop Streaming mapper
├── reducer.py      # Hadoop Streaming reducer
├── creditcard.csv  # Input dataset
├── output/         # Output directory (created by Hadoop)
└── README.md
```

---

## Step 1: Test Locally (Before Running on Hadoop)

Always test locally first using Unix pipes:

```bash
# Make scripts executable
chmod +x mapper.py reducer.py

# Run locally
cat creditcard.csv | python3 mapper.py | sort | python3 reducer.py
```

Expected output:
```
1_Bucket_$0-$10     97314   249   97065   0.2559%
2_Bucket_$10-$50    92390    56   92334   0.0606%
3_Bucket_$50-$100   37718    57   37661   0.1511%
4_Bucket_$100-$500  47893    95   47798   0.1984%
5_Bucket_$500-$1000  6423    26    6397   0.4048%
6_Bucket_$1000+      3069     9    3060   0.2933%
```

---

## Step 2: Start the Hadoop Docker Container

Pull the official Apache Hadoop image and start a container with the project
folder mounted as a volume:

```bash
# Pull the image (one time only)
sudo docker pull apache/hadoop:3

# Start the container (run from the folder containing your files)
sudo docker run -it \
  --user root \
  -v "$(pwd)":/creditcard \
  --name hadoop \
  apache/hadoop:3 bash
```

Your local folder is now accessible inside the container at `/creditcard`.

---

## Step 3: Run the MapReduce Job on Hadoop

Inside the container, set HADOOP_HOME and run the Hadoop Streaming job using
local file paths (no HDFS setup required):

```bash
# Set Hadoop home
export HADOOP_HOME=/opt/hadoop

# Remove previous output if it exists
rm -rf /creditcard/output

# Run the MapReduce job
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input   /creditcard/creditcard.csv \
  -output  /creditcard/output \
  -mapper  "python /creditcard/mapper.py" \
  -reducer "python /creditcard/reducer.py"
```

---

## Step 4: View the Output

```bash
# View results
cat /creditcard/output/part-00000
```

Expected output:
```
1_Bucket_$0-$10     97314   249   97065   0.2559%
2_Bucket_$10-$50    92390    56   92334   0.0606%
3_Bucket_$50-$100   37718    57   37661   0.1511%
4_Bucket_$100-$500  47893    95   47798   0.1984%
5_Bucket_$500-$1000  6423    26    6397   0.4048%
6_Bucket_$1000+      3069     9    3060   0.2933%
```

---

## Output Format

Each output line is tab-separated:

| Column | Description |
|--------|-------------|
| amount_range | Transaction amount bucket |
| total_transactions | Total transactions in this bucket |
| fraud_count | Number of fraudulent transactions |
| normal_count | Number of normal transactions |
| fraud_rate | Fraud percentage in this bucket |

---

## Step 5: Clean Up (Optional)

```bash
# Remove output folder inside container
rm -rf /creditcard/output

# Exit and remove container
exit
sudo docker rm hadoop
```
