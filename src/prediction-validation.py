import collections
import sys


INPUT_ACTUAL_PATH = './input/actual.txt'
INPUT_PREDICTED_PATH = './input/predicted.txt'
INPUT_WINDOW_PATH = './input/window.txt'
OUTPUT_COMPARISON_PATH = './output/comparison.txt'


class HourStats(object):

    def __init__(self, total_errs, count):
        self.total_errs = total_errs
        self.count = count

def GetStockPricesInHour(data, index, hour):
    stock_to_price = {}
    while index < len(data):
        d = data[index].strip()
        if not d:
            index += 1
            continue

        h, name, price = d.split('|')
        if int(h) == hour:
            stock_to_price[name] = float(price)
            index += 1
            continue
        break
    return stock_to_price, index


with open(INPUT_WINDOW_PATH, 'r') as window_file:
    window = int(window_file.read().strip())

with open(INPUT_ACTUAL_PATH, 'r') as actual_file:
    actual = actual_file.readlines()

with open(INPUT_PREDICTED_PATH, 'r') as predicted_file:
    predicted = predicted_file.readlines()

sliding_window_stats = collections.deque()
output = []
stock_to_price = {}
i = j = 0
n = 1
total = 0
count = 0

while i < len(actual):
    actual_prices, i = GetStockPricesInHour(actual, i, n)
    predicted_prices, j = GetStockPricesInHour(predicted, j, n)
    total_errs = 0
    cnt = 0

    for name, price in predicted_prices.items():
        if actual_prices[name]:
            total_errs += abs(price - actual_prices[name])
            cnt += 1

    if len(sliding_window_stats) == window:
        avg_err = round(total * 100 / count) / 100.0 if count != 0 else -1
	output.append(avg_err)
        stats = sliding_window_stats.popleft()
        total -= stats.total_errs
        count -= stats.count

    total += total_errs
    count += cnt
    sliding_window_stats.append(HourStats(total_errs, cnt))

    n += 1

avg_err = total / count if count != 0 else -1
output.append(avg_err)


with open(OUTPUT_COMPARISON_PATH, 'w') as comparison_file:
    for i, avg_err in enumerate(output):
        line = '%d|%d|' % (i + 1, i + window)
        if avg_err == -1:
            line += 'NA'
        else:
            line += '%.2f' % avg_err
        comparison_file.write(line + '\n')
