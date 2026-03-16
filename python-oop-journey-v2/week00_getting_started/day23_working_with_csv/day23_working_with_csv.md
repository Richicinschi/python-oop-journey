# Day 23: Working with CSV

## Learning Objectives

By the end of this day, you will be able to:

1. Read CSV files using the `csv` module
2. Write data to CSV files
3. Work with CSV headers (DictReader/DictWriter)
4. Handle different CSV dialects and delimiters
5. Process CSV data as lists and dictionaries

---

## Key Concepts

### 1. Reading CSV Files

```python
import csv

# Basic reading with reader
with open('data.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)  # Each row is a list
```

### 2. Writing CSV Files

```python
import csv

# Basic writing with writer
data = [['Name', 'Age'], ['Alice', '30'], ['Bob', '25']]

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
```

### 3. DictReader - Access by Column Name

```python
import csv

# CSV with header row
with open('data.csv', 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['Name'])  # Access by column name
        print(row['Age'])
```

### 4. DictWriter - Write with Headers

```python
import csv

fieldnames = ['Name', 'Age', 'City']
data = [
    {'Name': 'Alice', 'Age': '30', 'City': 'NYC'},
    {'Name': 'Bob', 'Age': '25', 'City': 'LA'}
]

with open('output.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

### 5. Custom Delimiters

```python
import csv

# Tab-separated values (TSV)
with open('data.tsv', 'r', newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        print(row)
```

---

## Common Mistakes

### 1. Forgetting `newline=''`

```python
# Bad - can cause blank lines on Windows
with open('data.csv', 'w') as file:
    writer = csv.writer(file)

# Good - always use newline=''
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
```

### 2. Modifying List During Iteration

```python
# The row is a list that gets reused
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)  # Convert to list first!
```

### 3. Not Handling Missing Fields

```python
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Use .get() for optional fields
        phone = row.get('Phone', 'N/A')
```

---

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01. read_csv_rows | Basic CSV reading with csv.reader |
| 02. write_csv_rows | Basic CSV writing with csv.writer |
| 03. read_csv_dict | Using DictReader for header access |
| 04. write_csv_dict | Using DictWriter with headers |
| 05. count_csv_rows | Counting rows, skipping headers |

---

## Quick Reference

```python
import csv

# Read all rows
with open('file.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Read as dictionaries
with open('file.csv', 'r', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['column'])

# Write rows
with open('file.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['a', 'b', 'c'])
    writer.writerows(data)

# Write dictionaries
with open('file.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['a', 'b'])
    writer.writeheader()
    writer.writerows(dicts)
```

## Connection to Project

CSV export is a bonus feature for your Todo List - users can export tasks to spreadsheet apps:

```python
import csv

def export_to_csv(tasks: list[dict], filename: str = "tasks.csv") -> None:
    """Export tasks to CSV for use in spreadsheet apps."""
    if not tasks:
        return
    
    fieldnames = tasks[0].keys()  # Get columns from first task
    
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)

# Export completed tasks only
completed = [t for t in tasks if t["completed"]]
export_to_csv(completed, "completed_tasks.csv")
```

---

## Next Steps

After completing today's exercises:
1. Practice with real CSV datasets
2. Explore handling large CSV files efficiently
3. Consider learning pandas for advanced data manipulation
