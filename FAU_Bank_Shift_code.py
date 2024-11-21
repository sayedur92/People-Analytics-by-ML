import pandas as pd
from pulp import  *
week = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat"]

df = pd.read_csv("fau_bank_shifts.csv",encoding="latin",index_col=0)

df = df.fillna(0).map(lambda x: 1 if x == "X" else x)
avg_customer_num_columns = []
avg_customer_num_columns.append(f'Avg_Customer_Number')
# create a matrix to show which shift each time window is associated with
shifts = df.drop(index=["Wage rate per 4h shift (EUR)"], columns=avg_customer_num_columns).values
# number of shifts
shift_num = shifts.shape[1]

# number of time windows
time_windows = shifts.shape[0]

# number of customers measured per time window
avg_customer_num = df[avg_customer_num_columns].values

# wage rate per shift
wages_per_shift = df.loc["Wage rate per 4h shift (EUR)", :].values.astype(int)

# service level
service_level = 0.125
# Decision variable, find the optimal number of workers for each time slot of each day
num_workers_indexes = []
for day_of_week in range(0,6):
  for shift_index in range(shift_num):
    num_workers_indexes.append(f'{day_of_week}_{shift_index}')
num_workers = LpVariable.dicts("num_workers", num_workers_indexes, lowBound=0, cat="Integer")
print(num_workers)
# Create problem
# Minimize number of workers/costs paid for employees each day
prob = LpProblem("scheduling_workers", LpMinimize)
for day_of_week in range(0,6):
  prob += lpSum([wages_per_shift[j] * num_workers[f'{day_of_week}_{j}'] for j in range(shift_num)])
#print(avg_customer_num)
for day_of_week in range(0, 1):
  for t in range(time_windows):
    print(avg_customer_num[t][day_of_week])
    prob += lpSum([shifts[t, j] * num_workers[f'{day_of_week}_{j}'] for j in range(shift_num)]) >= avg_customer_num[t][day_of_week] * service_level
prob.solve()
print("Status:", LpStatus[prob.status])
for index in num_workers:
  index_parts = index.split('_')
  shift = index_parts[1]
  print(
    f"The number of workers needed for shift {shift} is {int(num_workers[(index)].value())} workers"
  )
