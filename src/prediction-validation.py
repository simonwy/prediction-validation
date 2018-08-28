import collections
import sys

INPUT_ACTUAL_PATH = './input/actual.txt'
INPUT_PREDICTED_PATH = './input/predicted.txt'
INPUT_WINDOW_PATH = './input/window.txt'
OUTPUT_COMPARISON_PATH = './output/comparison.txt'



# Define Object class for per HourStats (including calculated error_sum and error_count)
class HourStats(object):
    def __init__(self, error_sum, error_count):
        self.error_sum = error_sum
        self.error_count = error_count



# Define GetPricesAtHour, return stock_price array and its index
def GetPricesAtHour(source, index, hour):
    stock_price = {}
    while index < len(source):
        item = source[index].strip()
        if not item: # to deal with edge case of NULL item
            index += 1
            continue
	    
        hr, name, price = item.split('|')
        if int(hr) == hour:
            stock_price[name] = float(price)
            index += 1
            continue
        break # quit function earlier in case the interested hour completed
    return stock_price, index



with open(INPUT_WINDOW_PATH, 'r') as window_file:
    window = int(window_file.read().strip())

with open(INPUT_ACTUAL_PATH, 'r') as actual_file:
    sourceActual = actual_file.readlines()

with open(INPUT_PREDICTED_PATH, 'r') as predicted_file:
    sourcePredicted = predicted_file.readlines()



# Using sliding_window to calculate the errors by a given window size
# use a deque to implement the sliding_window for better efficiency
sliding_window_stats = collections.deque()
output = []
stock_price = {}
actIdx = preIdx = 0
hr = 1	# starting hour
total = 0
count = 0


while actIdx < len(sourceActual):
    actual_prices, actIdx = GetPricesAtHour(sourceActual, actIdx, hr)
    predicted_prices, preIdx = GetPricesAtHour(sourcePredicted, preIdx, hr)
    total_errs = 0
    cnt = 0

    # calculate each matching error's sum and maitain its count
    for name, price in predicted_prices.items():
        if actual_prices[name]:
            total_errs += abs(price - actual_prices[name])
            cnt += 1
    
    # use a sliding_window to maintain and update the calculated errors in given window
    if len(sliding_window_stats) == window:
        #avg_err = round(total / count, 2) if count != 0 else -1
        avg_err = total / float(count) if count != 0 else -1
	output.append(avg_err)
        stats = sliding_window_stats.popleft()
        total -= stats.error_sum
        count -= stats.error_count

    total += total_errs
    count += cnt
    sliding_window_stats.append(HourStats(total_errs, cnt))

    hr += 1


avg_err = total / float(count)  if count != 0 else -1
output.append(avg_err)


with open(OUTPUT_COMPARISON_PATH, 'w') as comparison_file:
    for i, avg_err in enumerate(output):
        line = '%d|%d|' % (i + 1, i + window)
        if avg_err == -1:
            line += 'NA'
        else:
            #line += str(round(avg_err * 100 / 100.0, 2))
            #line += '%.2f' % avg_err
            line += '{:0.2f}'.format(avg_err)
        comparison_file.write(line + '\n')
