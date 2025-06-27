import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_category, get_amount, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE= "finance_data.csv"
    COLUMNS=["date", "amount", "category", "description"]
    FORMAT="%d-%m-%Y"
    
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
           df= pd.DataFrame(columns=cls.COLUMNS)
           df.to_csv(cls.CSV_FILE, index=False)
                
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry={
            "date":date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer= csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("entry added successfully")
    @classmethod
    def delete_transaction(cls):
        df = pd.read_csv(cls.CSV_FILE)
        if df.empty:
            print("No transactions to delete.")
            return

        # Show transactions with index
        df.index.name = "Index"
        print("\nAll Transactions:")
        temp_df = df.reset_index(drop=True)
        print(temp_df.to_string(index=True))

# Use temp_df.iloc[idx] instead of df.iloc[idx]

        try:
            idx = int(input("Enter the index of the transaction to delete: "))
            if idx < 0 or idx >= len(df):
                print("Invalid index.")
                return
        except ValueError:
            print("Invalid input. Enter a number.")
            return

        confirm = input(f"Are you sure you want to delete this transaction? (y/n):\n{df.iloc[idx].to_string()}\n> ").lower()
        if confirm == "y":
            df = df.drop(index=idx)
            df.to_csv(cls.CSV_FILE, index=False)
            print("Transaction deleted successfully.")
        else:
            print("Deletion canceled.")
   
    @classmethod
    def get_transaction(cls, start_date,end_date):
        df= pd.read_csv(cls.CSV_FILE)
        
       
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date=datetime.strptime(start_date,CSV.FORMAT)
        end_date=datetime.strptime(end_date,CSV.FORMAT)
        
        mask=(df["date"]>=start_date)& (df["date"]<=end_date)
        filtered_df= df.loc[mask]
        
        if filtered_df.empty:
            print("no transaction found in the given date range")
        else:
            print(f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False,formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
            
            total_income= filtered_df[filtered_df["category"]=="Income"] ["amount"].sum()
            total_expense= filtered_df[filtered_df["category"]=="Expense"] ["amount"].sum() 
            print("\nSummary")
            print(f"total income : ${total_income:.2f}")
            print(f"Total expense: ${total_expense:.2f}")
            print(f"Net savings: ${(total_expense - total_income):.2f}")
        
        return filtered_df 
        
def add():
    CSV.initialize_csv()
    date=get_date("enter the date of the transaction or enter today's date (dd-mm-yy): ",allow_default=True)
    amount= get_amount()
    category=get_category()
    description=get_description()
    CSV.add_entry(date,amount,category,description)
  
def plot_transaction(df):
    df.set_index('date', inplace=True)
    
    income_df= df[df["category"]=="Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df= df[df["category"]=="Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="b")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time", fontsize=18, fontweight='bold', color='navy')
    plt.legend()
    plt.grid("True", linestyle=':', color='gray', alpha=0.7)
    plt.show()
    
def main():
   

    while True:
        print("\n1:Add a new transaction\n2. delete a transaction \n3.view transaction and summary within a date range\n4:exit")
        choice=input("enter your choice(1-4): ")
        
        if choice=="1":
            add()
        elif choice=="2":
            CSV.delete_transaction()
        elif choice=="3":
            start_date= get_date("enter the start date(dd-mm-yyyy):")
            end_date= get_date("enter the end date(dd-mm-yyyy):")
            df =CSV.get_transaction(start_date,end_date)
            if input("Do you want to see anplot?(y/n):  ").lower()=="y":
                plot_transaction(df)
                
        elif choice=="4":
            print("exiting")
            break
        else:
            print("invalid choice. enter 1,2,3")
if __name__ == "__main__":
    main()
    