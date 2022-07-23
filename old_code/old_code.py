
###Stocks#########################################################################################################################################
def examinetrades(orders, printbuy = 'yes', crypto = 'no'):

    trades = []
    trading_dict = {}
    total_stockgain = 0
    total_stockloss = 0

    #loop through df
    for i in range(len(orders)):
        #store symbol variable
        symbol = orders.loc[i, 'symbol']
        date = orders.loc[i, 'date'].strftime('%Y-%m-%d')
        quantity = orders.loc[i, 'quantity']
        avg_price = orders.loc[i, 'average_price']
        total = round(orders.loc[i, 'total'],2)

        #if buy
        if orders.loc[i, 'side'] == 'buy':

            #if 'symbol_avgprice' in trading_dict, get cur_total, then new total after buying, update holding quantity, update avgprice
            if symbol+'_avgprice' in trading_dict:
                cur_total = trading_dict[symbol+'_quantity']*trading_dict[symbol+'_avgprice']
                new_total = cur_total + orders.loc[i, 'quantity'] * orders.loc[i, 'average_price']
                trading_dict[symbol+'_quantity'] += orders.loc[i, 'quantity']
                trading_dict[symbol+'_avgprice'] = new_total/trading_dict[symbol+'_quantity']
            #else add symbol_avgprice = buy price in df and symbol_quantity = bought quantity
            else:
                trading_dict[symbol+'_avgprice'] = orders.loc[i, 'average_price']
                trading_dict[symbol+'_quantity'] = orders.loc[i, 'quantity']

            cur_avg_price = round(trading_dict[symbol+'_avgprice'],2)

            #print 'symbol buy on date # shares at price'
            if printbuy == 'yes':
                # trades.append({'Symbol': orders.loc[i, 'symbol'], 'Side': 'Buy', 'Date': orders.loc[i, 'date'].strftime('%Y-%m-%d'), 'Quantity': orders.loc[i, 'quantity'],
                #                 'Avg Buy/Sell Price': orders.loc[i, 'average_price'], 'Current Avg Price': round(trading_dict[symbol+'_avgprice'],2), 'Total': round(orders.loc[i, 'total'],2)})

                # print(orders.loc[i, 'symbol'] + ' buy on ' + orders.loc[i, 'date'].strftime('%Y-%m-%d') + ', '
                #       + str(orders.loc[i, 'quantity']) + ' shares' + ' at $' + str(orders.loc[i, 'average_price']) + ', total: $' + str(round(orders.loc[i, 'total'],2)) + ', current avg price: $' + str(round(trading_dict[symbol+'_avgprice'],2)))

                print(f'Buy {symbol} on {date}, Quantity: {quantity}, Avg Price: ${avg_price}, Current Avg Cost: {cur_avg_price}, Total: ${total}')
                print('\n')

        #if sell
        if orders.loc[i, 'side'] == 'sell':

            #if 'symbol_avgprice' in trading_dict, gain = (df avg_price - trading_dict avg_price) * df quantity, update trading dict quantity
            if symbol+'_avgprice' in trading_dict:
                #print 'symbol sell on date # shares at price'

                # print(orders.loc[i, 'symbol'] + ' sell on ' + orders.loc[i, 'date'].strftime('%Y-%m-%d')
                #   + ', ' + str(orders.loc[i, 'quantity']) + ' shares' + ' at $' + str(orders.loc[i, 'average_price']) + ', current avg price: $' + str(round(trading_dict[symbol+'_avgprice'],2)) + ', total: $' + str(round(orders.loc[i, 'total'],2)))

                cur_avg_price = round(trading_dict[symbol+'_avgprice'],2)

                print(f'Sell {symbol} on {date}, Quantity: {quantity}, Avg Price: ${avg_price}, Current Avg Cost: {cur_avg_price}, Total: ${total}')

                gain = round((orders.loc[i, 'average_price'] - trading_dict[symbol+'_avgprice']) * orders.loc[i, 'quantity'],2)
                perc_gain = round((orders.loc[i, 'average_price'] - trading_dict[symbol+'_avgprice'])/trading_dict[symbol+'_avgprice']*100,2)

                if gain >= 0:
                    total_stockgain += gain
                    # trades.append({'Symbol': orders.loc[i, 'symbol'], 'Side': 'Sell', 'Date': orders.loc[i, 'date'].strftime('%Y-%m-%d'), 'Quantity': orders.loc[i, 'quantity'], 'Avg Buy/Sell Price': orders.loc[i, 'average_price'],
                    # 'Current Avg Price': round(trading_dict[symbol+'_avgprice'],2), 'Total': round(orders.loc[i, 'total'],2), 'Gain': round(gain,2),
                    # '% Gain': str(round((orders.loc[i, 'average_price'] - trading_dict[symbol+'_avgprice'])/trading_dict[symbol+'_avgprice']*100,2))+'%', 'Gain\Loss': 'Gain',
                    # 'Net Gain/Loss': round(total_stockgain + total_stockloss,2)})



                    # print('Gain: $' + str(round(gain,2)), ', Perc Gain:', str(round((orders.loc[i, 'average_price'] - trading_dict[symbol+'_avgprice'])/trading_dict[symbol+'_avgprice']*100,2)) + '%')
                    print(f'Gain: ${gain}, % Gain: {perc_gain}%')

                else:
                    total_stockloss += gain
                    # trades.append({'Symbol': orders.loc[i, 'symbol'], 'Side': 'Sell', 'Date': orders.loc[i, 'date'].strftime('%Y-%m-%d'), 'Quantity': orders.loc[i, 'quantity'], 'Avg Buy/Sell Price': orders.loc[i, 'average_price'],
                    # 'Current Avg Price': round(trading_dict[symbol+'_avgprice'],2), 'Total': round(orders.loc[i, 'total'],2), 'Gain': round(gain,2),
                    # '% Gain': str(round((orders.loc[i, 'average_price'] - trading_dict[symbol+'_avgprice'])/trading_dict[symbol+'_avgprice']*100,2))+'%', 'Gain\Loss': 'LOSS',
                    # 'Net Gain/Loss': round(total_stockgain + total_stockloss,2)})
                    # print('Gain: $' + str(round(gain,2)), ', Perc Gain:', str(round((orders.loc[i, 'average_price'] - trading_dict[symbol+'_avgprice'])/trading_dict[symbol+'_avgprice']*100,2)) + '%', 'LOSS')

                    print(f'Gain: ${gain}, % Gain: {perc_gain}%, LOSS')

                trading_dict[symbol+'_quantity'] -= orders.loc[i, 'quantity']

                net_gain_loss = round(total_stockgain + total_stockloss,2)
                # print('Net gain/loss: $', round(total_stockgain + total_stockloss,2))
                print(f'Net Gain/Loss: ${net_gain_loss}')
                print('\n')


                #if holding position = 0, then pop symbol avgprice and symbol quantity
                if trading_dict[symbol+'_quantity'] == 0:
                    trading_dict.pop(symbol+'_avgprice')
                    trading_dict.pop(symbol+'_quantity')

            else:

                # print(orders.loc[i, 'symbol'] + ' sell on ' + orders.loc[i, 'date'].strftime('%Y-%m-%d')
                #   + ', ' + str(orders.loc[i, 'quantity']) + ' shares' + ' at $' + str(orders.loc[i, 'average_price']) + ', total: $' + str(round(orders.loc[i, 'total'],2)))

                print(f'Sell {symbol} on {date}, Quantity: {quantity}, Avg Price: ${avg_price}, Total: ${total}')

                gain = round(orders.loc[i, 'average_price'] * orders.loc[i, 'quantity'],2)
                total_stockgain += gain

                # trades.append({'Symbol': orders.loc[i, 'symbol'], 'Side': 'Sell', 'Date': orders.loc[i, 'date'].strftime('%Y-%m-%d'), 'Quantity': orders.loc[i, 'quantity'],
                #                 'Avg Buy/Sell Price': orders.loc[i, 'average_price'], 'Total': round(orders.loc[i, 'total'],2), 'Gain': round(gain,2), 'Free/Acquired Stock': 'Yes'})
                print(f'Free/Acquired Stock Gain: ${gain}')
                print('\n')

    # trades_df = pd.DataFrame(trades).fillna('')

    # display(trades_df)

    if crypto == 'yes':
        total_cryptogain = round(total_stockgain,2)
        total_cryptoloss = round(total_stockloss,2)

        print()
        print(f'Total Gain: ${total_cryptogain}')
        print(f'Total Loss: ${total_cryptoloss}')

    elif crypto == 'no':
        total_stockgain = round(total_stockgain, 2)
        total_stockloss = round(total_stockloss, 2)
        print()
        print(f'Total Gain: ${total_stockgain}')
        print(f'Total Loss: ${total_stockloss}')

    # return trades_df
