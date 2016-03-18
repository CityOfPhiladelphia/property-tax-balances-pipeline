# Property Tax Data Pipeline

Remove `NULL` bytes from the mainframe-generated file and run this script using:
```bash
cat OPEN_DATA_FILE.txt | tr -d '\0' | python main.py
```
