from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime
CWD = Path.cwd()


# imports data from a csv file and returns it as a list of dictionaries where each line from the csv other that the column headings is. Made generic in case it is needed elsewhere.
def import_csv(path):
    first = True
    cells = []
    data = []
    line = {}
    str = ""
    quotecount = 0
    quoteopen = False
    lastchar = ""
    try:
        file = open(path, 'r', encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    with file:
        while True:
            char = file.read(1)
            if not char:
                break
            if not quoteopen and char == ",":
                cells.append(str)
                str = ""
                quotecount = 0
            elif not quoteopen and char == "\n":
                cells.append(str)
                if first:
                    keys = cells
                    first = False
                else:
                    for i in range(len(keys)):
                        line[keys[i]] = cells[i]
                    data.append(line)
                line = {}
                cells = []
                str = ""
                quotecount = 0
            elif char == '"':
                quotecount += 1
                if quoteopen:
                    quoteopen = False
                elif quotecount > 1 and not quoteopen:
                    quoteopen = True
                if lastchar == '"':
                    str += char
            else:
                str += char
            lastchar = char
    return data

# Groups all lines of orders based on their Order ID
def group_orders(orders):
    orderKeys = []
    newOrders = {}
    newOrdersList = []
    neworder = {}
    # Go through each line of orders in orders then group the orders by Order ID. (This is a failsafe for if the data from the CSV is not sorted by ID)
    for order in orders:
        neworder = {}
        # check if the order ID exist, if so add the product from 
        if order["OrderID"] in orderKeys:
            newOrders[order["OrderID"]]['Products'].append({
                    'Product ID':order['Product ID'],
                    'Product Name':order['Product Name'],
                    'Category':order['Category'],
                    'Quantity':int(order['Quantity']),
                    'Price':float(order['Price']),
                    'Discount Applied':float(order['Discount Applied']),
                    'Total Price':float(order['Total Price'])
                    })
        else:
            neworder = {"OrderID":order["OrderID"],
                        "Date":order["Date"],
                        "Products":[{
                                'Product ID':order['Product ID'],
                                'Product Name':order['Product Name'],
                                'Category':order['Category'],
                                'Quantity':int(order['Quantity']),
                                'Price':float(order['Price']),
                                'Discount Applied':float(order['Discount Applied']),
                                'Total Price':float(order['Total Price'])
                                }
                            ]
                        }
            orderKeys.append(order["OrderID"])
            newOrders[order["OrderID"]] = neworder
    # add all orders to a list based on which ones appear first.
    for key in orderKeys:
        newOrdersList.append(newOrders[key])
    return newOrdersList   

def get_product_data(salesData):
    productsKeys = []
    newProducts = {}
    newProductList = []
    newProduct = {}
    # Group products by ID and add up their total cost and quantity
    for order in salesData:
        for product in order['Products']:
            if product["Product ID"] in productsKeys:
                newProducts[product['Product ID']]['Quantity'] += product['Quantity']
                newProducts[product['Product ID']]['Total Price'] += product['Total Price']
            else:
                newProduct = {
                    'Product ID':product['Product ID'],
                    'Product Name':product['Product Name'],
                    'Category':product['Category'],
                    'Quantity':product['Quantity'],
                    'Price':product['Price'],
                    'Total Price':product['Total Price']
                }
                productsKeys.append(product['Product ID'])
                newProducts[product['Product ID']] = newProduct
    # Put the products into a list based on the order they appear
    for key in productsKeys:
        newProductList.append(newProducts[key])
    return newProductList

def statistic_report(salesData):
    numOrders = len(salesData)
    totalRevenue = 0
    for order in salesData:
        for product in order["Products"]:
            totalRevenue += product['Total Price']
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    table = ax.table(cellText=[[str(round(totalRevenue, 2)), str(round(totalRevenue/numOrders, 2))]],colLabels=["Total Revenue", "Average Transaction"],loc='center', cellLoc='center')
    plt.show() 
    
def product_report(productData):
    products = merge_sort(productData, "Quantity")
    length = len(products)
    topfive = []
    botfive = []
    size = length
    if length > 4:
        size = 5  
    for i in range(size):
            # Name
            topfive.append([ products[length - 1 - i]["Product Name"], products[length - 1 - i]["Quantity"] ])
            botfive.append([ products[i]["Product Name"],  products[i]["Quantity"]])
        
            
    fig, axs =plt.subplots(2,1)
    axs[0].axis('tight')
    axs[0].axis('off')
    table = axs[0].table(cellText=topfive,colLabels=["Product Name", "Quantity Sold"],loc='center', cellLoc='center')
    axs[0].set_title("Top 5 Products")  
    
    axs[1].axis('tight')
    axs[1].axis('off')
    table = axs[1].table(cellText=botfive,colLabels=["Product Name", "Quantity Sold"],loc='center', cellLoc='center')
    axs[1].set_title("Bot 5 Products")

    plt.show() 
    

def correlation_report(productData):
    x = []
    y = []
    titles = []
    for product in productData:
        x.append(product['Price'])
        y.append(product['Quantity'])
        titles.append(product['Product Name'])
    plt.figure(figsize=(14, 6))
    plt.scatter(x, y,  edgecolors='black')
    plt.xlabel("Price")
    plt.ylabel("Quantity Sold")
    plt.title("Price to Quantity Scatter Plot")
    for i, label in enumerate(titles):
        plt.annotate(label, (x[i] -5, y[i] + 3))
        
    plt.show()
    
def probability_report(ordersbyDate, productID):
    timespan = datetime.strptime(ordersbyDate[-1]["Date"], "%Y-%m-%d") - datetime.strptime(ordersbyDate[0]["Date"], "%Y-%m-%d")
    timespan = timespan.days
    dateKeys = []
    soldDates = {}
    totalSold = 0
    numSales = 0
    name = ""
    for order in ordersbyDate:
        date = order["Date"]
        for product in order["Products"]:
            if product["Product ID"] == productID:
                if date in dateKeys:
                    soldDates[date] += product['Quantity']
                else:
                    soldDates[date] = product['Quantity']
                    dateKeys.append(date)
                if name == "":
                    name = product["Product Name"]
                numSales +=1
                totalSold += product['Quantity']
    numDaysSold = len(dateKeys)
    percentDaysSold = str(round(numDaysSold/timespan * 100, 2)) + "%"
    avgSoldPerDay = str(round(totalSold/timespan, 2))
    avgSoldPerDaySold = str(round(totalSold/numDaysSold, 2))
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    ax.set_title("Probability of Sale of " + name)
    table = ax.table(cellText=[[ percentDaysSold, avgSoldPerDay, avgSoldPerDaySold]],colLabels=[ " % Days Sold", "AVG Sales/Day", "Avg Sales/Day Sold"],loc='center', cellLoc='center')
    plt.show() 

def trend_report(ordersByDate):
    categorySales = {}
    categories = []
    dailySales = {}
    dates = []
    dailySalesVolume = []
    dailySalesRevenue = []
    catSalesVolume = []
    catSalesRevenue = []
    formatedDates = []
    sales = {}
    prevDate = None
    for order in ordersByDate:
        date = order["Date"]
        # whenever a new date is found.
        if date != prevDate and prevDate != None:
            dailySales[prevDate] = sales
            sales = {}
            dates.append(prevDate)
        for product in order["Products"]:
            category = product["Category"]
            if category not in categories:
                categorySales[category] = {"Quantity":product["Quantity"], "Total Price":product["Total Price"]}
                categories.append(category)
            else:
                categorySales[category]["Quantity"] += product["Quantity"]
                categorySales[category]["Total Price"] += product["Total Price"]
            if sales.get("Quantity") == None:
                sales["Quantity"] = product["Quantity"]
                sales["Total Price"] = product["Total Price"]
            else:
                sales["Quantity"] += product["Quantity"]
                sales["Total Price"] += product["Total Price"]
        prevDate = date
    dailySales[prevDate] = sales
    dates.append(date)
    for date in dates:
        dailySalesVolume.append(dailySales[date]["Quantity"])
        dailySalesRevenue.append(dailySales[date]["Total Price"])
        formatedDates.append(datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%m/%d"))
    for category in categories:
        catSalesVolume.append(categorySales[category]["Quantity"])
        catSalesRevenue.append(categorySales[category]["Total Price"])
    plt.figure(figsize=(14, 6))
    ax = plt.axes()
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.plot(formatedDates, dailySalesVolume)
    plt.xlabel("Date")
    plt.ylabel("Quantity Sold")
    plt.title("Volume of Sales over Time")
    plt.show()
    plt.figure(figsize=(14, 6))
    ax2 = plt.axes()
    ax2.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax2.plot(formatedDates, dailySalesRevenue)
    plt.xlabel("Date")
    plt.ylabel("Revenue ($)")
    plt.title("Revenue of Sales over Time")
    plt.show()
    ax3 = plt.axes()
    ax3.bar(categories, catSalesVolume)
    plt.xlabel("Category")
    plt.ylabel("Quantity Sold")
    plt.title("Volume of Sales by category")
    plt.show()
    ax4 = plt.axes()
    ax4.bar(categories, catSalesRevenue)
    plt.xlabel("Category")
    plt.ylabel("Revenue ($)")
    plt.title("Revenue by Category")
    plt.show()
    

def merge(left, right, key):
    
    # initialize the pointers and length variables
    leftlength = len(left)
    rightlength = len(right)
    i = 0
    j = 0
    
    # create a new list
    mergedlist = []
    
    # check if there was a key provided
    if key == None:
             # go put the smallest item from each list into the new list until all the items from one input list has been added.
        while i < leftlength and j < rightlength:
            if left[i] < right[j]:
                mergedlist.append(left[i])
                i+= 1
            else:
                mergedlist.append(right[j])
                j += 1
    else:
        # go put the smallest item from each list into the new list until all the items from one input list has been added.
        while i < leftlength and j < rightlength:
            if left[i][key] < right[j][key]:
                mergedlist.append(left[i])
                i+= 1
            else:
                mergedlist.append(right[j])
                j += 1
            
    # add the remaining items from each list.
    while i < leftlength:
        mergedlist.append(left[i])
        i+= 1
    while j < rightlength:
        mergedlist.append(right[j])
        j += 1
    return mergedlist

# Takes in an optional key parameter which is the key to the dictionary to use when sorting the list.
def merge_sort(list, key = None):
    # if length of list is 1 or less return the list.
    length = len(list)
    if length <= 1:
        return list
    
    # divide the lists into equal parts
    leftsize = length//2
    leftlist = []
    rightlist = []
    for i in range(length):
        if i < leftsize:
            leftlist.append(list[i])
        else:
            rightlist.append(list[i])
    
    # use recursion to divide the lists until they are 1 item or shorter.
    leftlist = merge_sort(leftlist, key)
    rightlist = merge_sort(rightlist, key)
    
    # merge and sort the lists and return the result
    return merge(leftlist, rightlist, key) 

def main():
    orders = group_orders(import_csv(CWD /"sales_data.csv"))
    products = get_product_data(orders)
    orders_by_date = merge_sort(orders, 'Date')
    statistic_report(orders)
    product_report(products)
    correlation_report(products)
    probability_report(orders_by_date, "P004")
    trend_report(orders_by_date)
main()