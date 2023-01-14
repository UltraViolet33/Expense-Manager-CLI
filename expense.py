import csv
import datetime
from tabulate import tabulate
import calendar

DEBUG = False
if DEBUG:
    FILE_PATH = './debug/expenses.csv'
else:
    FILE_PATH = "expenses.csv"


class Expense():

    TYPES = [
        "Food", "Clothes", "Restaurant", "Books", "Others", "Washing", "Bus"
    ]

    def __init__(self, amount, kind):
        self.amount = amount
        self.kind = kind
        self.date = datetime.date.today()
        self.save_expense()
        self.debug = True

    def __str__(self):
        return f"amount: {self.amount}, kind: {self.kind}, date: {self.date}"

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, kind):
        self._kind = kind

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @classmethod
    def get(cls):
        while True:
            try:
                amount = float(input("Amount: "))
                print(amount)
                kind = input("Kind: ")
                if kind not in Expense.TYPES:
                    raise (ValueError)
                return cls(amount, kind)
            except ValueError:
                print(
                    f"For amount: a positive integer \n For the type: {Expense.TYPES}"
                )

    @classmethod
    def see_total_expenses_amount(self):
        expenses = self.get_expenses_from_file(self)
        total_amount = 0
        for item in expenses:
            total_amount += float(item["amount"])

        return total_amount

    @classmethod
    def read_all_expenses(self):
        all_expenses = self.get_expenses_from_file(self)
        print(tabulate(all_expenses, headers="keys", tablefmt="grid"))

    @classmethod
    def read_single_expense(self, id_expense):
        expense = self.get_single_expense(id_expense)
        list_single_expense = [expense]
        print(tabulate(list_single_expense, headers="keys", tablefmt="grid"))
        return expense

    @classmethod
    def get_single_expense(self, id_expense):
        expense = {}
        id_expense = str(id_expense)
        all_expenses = self.get_expenses_from_file(self)
        for item in all_expenses:
            if item['id'] == id_expense:
                expense = item
        return expense

    @classmethod
    def delete_expense(self, id_expense):
        id_expense = str(id_expense)
        all_expenses = self.get_expenses_from_file(self)
        for item in all_expenses:
            if item['id'] == id_expense:
                all_expenses.remove(item)
        self.write_expense_to_file(all_expenses)

    def save_expense(self):
        expense = self.to_dict()
        self.save_expenses_to_file(expense)

    def to_dict(self):
        return {"kind": self.kind, "amount": self.amount, "date": self.date}

    def get_expenses_from_file(self):
        all_expenses = []
        with open(FILE_PATH, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                all_expenses.append(row)

        return all_expenses

    @classmethod
    def write_expense_to_file(self, expenses):
        header = ["id", "kind", "amount", "date"]

        with open(FILE_PATH, "w") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(expenses)

    def save_expenses_to_file(self, expense):
        all_expenses = self.get_expenses_from_file()
        if len(all_expenses) == 0:
            id = 1
        else:
            id = int(all_expenses[len(all_expenses) - 1]['id']) + 1

        expense['id'] = id
        all_expenses.append(expense)
        self.write_expense_to_file(all_expenses)

    @classmethod
    def read_total_per_months(self):
        total_per_months = self.get_total_per_months()
        print(tabulate(total_per_months, headers="keys", tablefmt="grid"))

    @classmethod
    def get_total_per_months(self):
        all_expenses = self.get_expenses_from_file(self)
        months = {}
        for item in all_expenses:
            item['date'] = datetime.datetime.strptime(item['date'], '%Y-%m-%d')
            month = item['date'].month
            if month not in months:
                months[month] = 0

        for month in months:
            for item in all_expenses:
                month_expense = item['date'].month
                if month_expense == month:
                    months[month] += float(item['amount'])

        final_months_amount = []
        for item in months:
            month_str = calendar.month_name[item]
            single_month = {}
            single_month["month"] = month_str
            single_month["amount"] = (months[item])
            final_months_amount.append(single_month)

        return final_months_amount

    @classmethod
    def read_average_expenses_per_month(self):
        expenses_per_month = self.get_total_per_months()
        total = 0
        total_months = len(expenses_per_month)

        for item in expenses_per_month:
            total += float(item["amount"])

        average_per_month = total / total_months
        average_per_month = round(average_per_month, 2)

        print(f"Average expenses by month: {average_per_month} €")

    @classmethod
    def read_details_per_months(self):
        all_expenses = self.get_expenses_from_file(self)
        months = []
        for item in all_expenses:
            item['date'] = datetime.datetime.strptime(item['date'], '%Y-%m-%d')
            month = item['date'].month
            month = calendar.month_name[month]
            if month not in months:
                month_details = {}
                month_details['month'] = month
                month_details['types'] = []
                months.append(month)

        final_months = []

        for month in months:
            month_details = {}
            month_details['month'] = month
            month_details['types'] = {}
            for type in Expense.TYPES:
                month_details['types'][type] = 0
            final_months.append(month_details)

        for expense in all_expenses:

            month = expense['date'].month
            month = calendar.month_name[month]

            for item in final_months:
                if month == item['month']:
                    for type in item["types"]:
                        if type == expense['kind']:
                            item["types"][type] += float(expense['amount'])

        previous_month = 0
        for month in final_months:
            print("Month: ", month["month"])
            total = 0
            for type in Expense.TYPES:
                total += month["types"][type]
            types = [month['types']]
            print(f"Total expenses: {total} € ")
            diff = total - previous_month
            if diff > 0:
                print(f"Diff previous month : + {diff} ")
            elif diff < 0:
                print(f"Diff previous month : {diff} ")
            else:
                print("No diff")
            previous_month = total

            print(tabulate(types, headers="keys", tablefmt="grid"))
