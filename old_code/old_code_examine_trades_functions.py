#import  libraries
from datetime import date
import pandas as pd


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

                print(f'Buy {symbol} on {date}, Quantity: {quantity}, Avg Price: ${avg_price}, Current Avg Price: {cur_avg_price}, Total: ${total}')
                print('\n')

        #if sell
        if orders.loc[i, 'side'] == 'sell':

            #if 'symbol_avgprice' in trading_dict, gain = (df avg_price - trading_dict avg_price) * df quantity, update trading dict quantity
            if symbol+'_avgprice' in trading_dict:
                #print 'symbol sell on date # shares at price'

                # print(orders.loc[i, 'symbol'] + ' sell on ' + orders.loc[i, 'date'].strftime('%Y-%m-%d')
                #   + ', ' + str(orders.loc[i, 'quantity']) + ' shares' + ' at $' + str(orders.loc[i, 'average_price']) + ', current avg price: $' + str(round(trading_dict[symbol+'_avgprice'],2)) + ', total: $' + str(round(orders.loc[i, 'total'],2)))

                cur_avg_price = round(trading_dict[symbol+'_avgprice'],2)

                print(f'Sell {symbol} on {date}, Quantity: {quantity}, Avg Price: ${avg_price}, Current Avg Price: {cur_avg_price}, Total: ${total}')

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

                # print('Free/Acquired Stock Gain:', round(gain,2))
                print(f'Free/Acquired Stock Gain: ${gain}')
                print('\n')

    # trades_df = pd.DataFrame(trades).fillna('')

    # display(trades_df)

    if crypto == 'yes':
        total_cryptogain = round(total_stockgain,2)
        total_cryptoloss = round(total_stockloss,2)

        print()
        # print('total gain: $' + str(round(total_cryptogain, 2)))
        print(f'Total Gain: ${total_cryptogain}')
        # print('total loss: $' + str(round(total_cryptoloss, 2)))
        print(f'Total Loss: ${total_cryptoloss}')

    elif crypto == 'no':
        total_stockgain = round(total_stockgain, 2)
        total_stockloss = round(total_stockloss, 2)
        print()
        # print('total gain: $' + str(round(total_stockgain,2)))
        print(f'Total Gain: ${total_stockgain}')
        # print('total loss: $' + str(round(total_stockloss,2)))
        print(f'Total Loss: ${total_stockloss}')

    # return trades_df


def get_total_gain_loss(orders, crypto = 'no'):

    trading_dict = {}
    total_stockgain = 0
    total_stockloss = 0

    #loop through df
    for i in range(len(orders)):
        #store symbol variable
        symbol = orders.loc[i, 'symbol']

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

        #if sell
        if orders.loc[i, 'side'] == 'sell':

            #if 'symbol_avgprice' in trading_dict, gain = (df avg_price - trading_dict avg_price) * df quantity, update trading dict quantity
            if symbol+'_avgprice' in trading_dict:
                #print 'symbol sell on date # shares at price'
                gain = (orders.loc[i, 'average_price'] - trading_dict[symbol+'_avgprice']) * orders.loc[i, 'quantity']
                if gain >= 0:
                    total_stockgain += gain
                else:
                    total_stockloss += gain

                trading_dict[symbol+'_quantity'] -= orders.loc[i, 'quantity']

                #if holding position = 0, then pop symbol avgprice and symbol quantity
                if trading_dict[symbol+'_quantity'] == 0:
                    trading_dict.pop(symbol+'_avgprice')
                    trading_dict.pop(symbol+'_quantity')

            else:
                gain = orders.loc[i, 'average_price'] * orders.loc[i, 'quantity']
                total_stockgain += gain


    if crypto == 'yes':
        total_cryptogain = round(total_stockgain,2)
        total_cryptoloss = round(total_stockloss,2)
        return total_cryptogain, total_cryptoloss

    elif crypto == 'no':
        total_stockgain = round(total_stockgain, 2)
        total_stockloss = round(total_stockloss, 2)
        return total_stockgain, total_stockloss



###Options#########################################################################################################################################
def examine_optiontrades(orders, printbuy = 'yes'):
    total_optionsgain = 0
    total_optionsloss = 0
    trading_dict = {}
    symbol_strike_exp_type_list = []
    losses = []
    gains = []

    #loop through df
    for i in range(len(orders)):

        symbol = orders.loc[i, 'chain_symbol']
        exp = orders.loc[i, 'expiration_date']
        strike = orders.loc[i, 'strike_price']
        option_type = orders.loc[i, 'option_type']
        quantity = orders.loc[i, 'processed_quantity']
        order_date = orders.loc[i, 'order_created_at'].strftime('%Y-%m-%d')
        avg_price = orders.loc[i, 'price']
        total = round(avg_price * quantity * 100,2)

        symb_exp_strike_type = f'{symbol} {exp} {strike} {option_type}'

        #if buy
        if orders.loc[i, 'side'] == 'buy':
            if symb_exp_strike_type not in symbol_strike_exp_type_list:
                symbol_strike_exp_type_list.append(symb_exp_strike_type)

            #if 'chain_symbol_avgprice' in trading_dict, get cur_total, then new total after buying, update holding quantity, update avgprice
            if symb_exp_strike_type+'_avgprice' in trading_dict:
                cur_total = trading_dict[symb_exp_strike_type+'_quantity']*trading_dict[symb_exp_strike_type+'_avgprice']
                new_total = cur_total + quantity * avg_price
                trading_dict[symb_exp_strike_type+'_quantity'] += quantity
                trading_dict[symb_exp_strike_type+'_avgprice'] = new_total/trading_dict[symb_exp_strike_type+'_quantity']

            #else add chain_symbol_avgprice = buy price in df and chain_symbol_quantity = bought quantity
            else:
                trading_dict[symb_exp_strike_type+'_avgprice'] = avg_price
                trading_dict[symb_exp_strike_type+'_quantity'] = quantity


            cur_avg_price = round(trading_dict[symb_exp_strike_type+'_avgprice'],2)

            if printbuy == 'yes':
                #print 'chain_symbol buy on date # shares at price'
                # print(symbol, exp, ' expiration', orders.loc[i, 'strike_price'], ' buy on ' + orders.loc[i, 'order_created_at'].strftime('%Y-%m-%d') + ', ' + str(orders.loc[i, 'processed_quantity']) + ' contracts' + ' at $' + str(orders.loc[i, 'price'])
                # + ', current avg price: $' + str(round(trading_dict[symb_exp_strike_type+'_avgprice'],2)))

                print(f'Buy {symbol}, Expiration: {exp}, Strike: {strike} on {order_date}, Quantity: {quantity} contracts, Avg Price: ${avg_price}, Current Avg Price: ${cur_avg_price}, Total: ${total}')
                print()

        #if sell
        if orders.loc[i, 'side'] == 'sell':

            #if 'chain_symbol_avgprice' in trading_dict, gain = (df avg_price - trading_dict avg_price) * df quantity, update trading dict quantity
            if symb_exp_strike_type+'_avgprice' in trading_dict:
                #print 'chain_symbol sell on date # shares at price'

                cur_avg_price = round(trading_dict[symb_exp_strike_type+'_avgprice'],2)

                # print(symbol, exp, ' expiration', orders.loc[i, 'strike_price'], ' sell on ' + orders.loc[i, 'order_created_at'].strftime('%Y-%m-%d') + ', ' + str(orders.loc[i, 'processed_quantity']) + ' contracts' + ' at $' + str(orders.loc[i, 'price'])
                # + ', current avg price: $' + str(round(trading_dict[symb_exp_strike_type+'_avgprice'],2)))

                print(f'Sell {symbol}, Expiration: {exp}, Strike: {strike} on {order_date}, Quantity: {quantity} contracts, Avg Price: ${avg_price}, Current Avg Price: ${cur_avg_price}, Total: ${total}')

                gain = round((orders.loc[i, 'price'] - trading_dict[symb_exp_strike_type+'_avgprice']) * orders.loc[i, 'processed_quantity']*100,2)
                perc_gain = round((orders.loc[i, 'price'] - trading_dict[symb_exp_strike_type+'_avgprice'])/trading_dict[symb_exp_strike_type+'_avgprice']*100,2)

                if gain >= 0:
                    total_optionsgain += gain
                    # print('Gain:', round(gain,2), ', % Gain:', str(round((orders.loc[i, 'price'] - trading_dict[symb_exp_strike_type+'_avgprice'])/trading_dict[symb_exp_strike_type+'_avgprice']*100,2)) + '%')

                    print(f'Gain: ${gain}, % Gain: {perc_gain}%')
                    print()
                    gains.append([symbol, exp, strike, gain, str(round((orders.loc[i, 'price'] - trading_dict[symb_exp_strike_type+'_avgprice'])/trading_dict[symb_exp_strike_type+'_avgprice']*100,2)) + '%'])
                else:
                    total_optionsloss += gain
                    # print('Gain:', round(gain,2), ', % Gain:', str(round((orders.loc[i, 'price'] - trading_dict[symb_exp_strike_type+'_avgprice'])/trading_dict[symb_exp_strike_type+'_avgprice']*100,2)) + '%', 'LOSS')

                    print(f'Gain: ${gain}, % Gain: {perc_gain}%, LOSS')
                    print()
                    losses.append([symbol, exp, strike, gain, str(round((orders.loc[i, 'price'] - trading_dict[symb_exp_strike_type+'_avgprice'])/trading_dict[symb_exp_strike_type+'_avgprice']*100,2)) + '%'])

                trading_dict[symb_exp_strike_type+'_quantity'] -= orders.loc[i, 'processed_quantity']

                #if holding position = 0, then pop chain_symbol avgprice and chain_symbol quantity

                if trading_dict[symb_exp_strike_type+'_quantity'] == 0:
                    trading_dict.pop(symb_exp_strike_type+'_avgprice')
                    trading_dict.pop(symb_exp_strike_type+'_quantity')
                    symbol_strike_exp_type_list.remove(symb_exp_strike_type)
    print()

    #getting expired orders, adding to losses
    for i in range(len(orders)):

        symbol = orders.loc[i, 'chain_symbol']
        exp = orders.loc[i, 'expiration_date']
        strike = orders.loc[i, 'strike_price']
        option_type = orders.loc[i, 'option_type']
        quantity = orders.loc[i, 'processed_quantity']
        order_date = orders.loc[i, 'order_created_at'].strftime('%Y-%m-%d')
        avg_price = orders.loc[i, 'price']
        total = round(avg_price * quantity * 100,2)


        symb_exp_strike_type = f'{symbol} {exp} {strike} {option_type}'

        if symb_exp_strike_type in symbol_strike_exp_type_list and exp < date.today():
            # print('Expired: ', symbol, exp, strike, option_type, '$', orders.loc[i, 'processed_quantity']*orders.loc[i, 'price']*100)
            print(f'Expired: {symbol} Expiration: {exp}, Strike: {strike}, Option Type: {option_type}, Quantity: {quantity}, Avg Price: ${avg_price} Total: ${total}')
            losses.append([symbol, exp, strike, total*-1, '-100%'])
            total_optionsloss -= total



    print()

    total_optionsgain = round(total_optionsgain,2)
    total_optionsloss = round(total_optionsloss,2)
    print(f'Total Options Gain: ${total_optionsgain}')
    print(f'Total Options Loss: ${total_optionsloss}')


    gains_df = pd.DataFrame(gains, columns = ['Symbol', 'Expiration', 'Strike', 'Gain', '% Gain'])
    losses_df = pd.DataFrame(losses, columns = ['Symbol', 'Expiration', 'Strike', 'Gain', '% Gain'])


    gains_df['Expiration'] = gains_df['Expiration'].astype(str).str.replace(' 00:00:00', '')
    losses_df['Expiration'] = losses_df['Expiration'].astype(str).str.replace(' 00:00:00', '')
    gains_df['Gain'] = gains_df['Gain'].astype('float64')
    losses_df['Gain'] = losses_df['Gain'].astype('float64')

    print()
    print('Top Option Gainers:')
    display(gains_df.sort_values('Gain', ascending=False).reset_index(drop=True))

    print()
    print('Top Option Losers:')
    display(losses_df.sort_values('Gain').reset_index(drop=True))




def get_options_total_gain_loss(orders):

    total_optionsgain = 0
    total_optionsloss = 0
    trading_dict = {}
    symbol_strike_exp_type_list = []

    #loop through df
    for i in range(len(orders)):

        symbol = orders.loc[i, 'chain_symbol']
        exp = orders.loc[i, 'expiration_date']
        strike = orders.loc[i, 'strike_price']
        option_type = orders.loc[i, 'option_type']
        quantity = orders.loc[i, 'processed_quantity']
        order_date = orders.loc[i, 'order_created_at'].strftime('%Y-%m-%d')
        avg_price = orders.loc[i, 'price']
        total = round(avg_price * quantity * 100,2)

        symb_exp_strike_type = f'{symbol} {exp} {strike} {option_type}'

        #if buy
        if orders.loc[i, 'side'] == 'buy':
            if symb_exp_strike_type not in symbol_strike_exp_type_list:
                symbol_strike_exp_type_list.append(symb_exp_strike_type)

            #if 'chain_symbol_avgprice' in trading_dict, get cur_total, then new total after buying, update holding quantity, update avgprice
            if symb_exp_strike_type+'_avgprice' in trading_dict:
                cur_total = trading_dict[symb_exp_strike_type+'_quantity']*trading_dict[symb_exp_strike_type+'_avgprice']
                new_total = cur_total + quantity * avg_price
                trading_dict[symb_exp_strike_type+'_quantity'] += quantity
                trading_dict[symb_exp_strike_type+'_avgprice'] = new_total/trading_dict[symb_exp_strike_type+'_quantity']

            #else add chain_symbol_avgprice = buy price in df and chain_symbol_quantity = bought quantity
            else:
                trading_dict[symb_exp_strike_type+'_avgprice'] = avg_price
                trading_dict[symb_exp_strike_type+'_quantity'] = quantity


        if orders.loc[i, 'side'] == 'sell':

            #if 'chain_symbol_avgprice' in trading_dict, gain = (df avg_price - trading_dict avg_price) * df quantity, update trading dict quantity
            if symb_exp_strike_type+'_avgprice' in trading_dict:

                gain = round((orders.loc[i, 'price'] - trading_dict[symb_exp_strike_type+'_avgprice']) * orders.loc[i, 'processed_quantity']*100,2)
                perc_gain = round((orders.loc[i, 'price'] - trading_dict[symb_exp_strike_type+'_avgprice'])/trading_dict[symb_exp_strike_type+'_avgprice']*100,2)

                if gain >= 0:
                    total_optionsgain += gain
                else:
                    total_optionsloss += gain

                trading_dict[symb_exp_strike_type+'_quantity'] -= orders.loc[i, 'processed_quantity']

                #if holding position = 0, then pop chain_symbol avgprice and chain_symbol quantity

                if trading_dict[symb_exp_strike_type+'_quantity'] == 0:
                    trading_dict.pop(symb_exp_strike_type+'_avgprice')
                    trading_dict.pop(symb_exp_strike_type+'_quantity')
                    symbol_strike_exp_type_list.remove(symb_exp_strike_type)

    #getting expired orders, adding to losses
    for i in range(len(orders)):

        symbol = orders.loc[i, 'chain_symbol']
        exp = orders.loc[i, 'expiration_date']
        strike = orders.loc[i, 'strike_price']
        option_type = orders.loc[i, 'option_type']
        quantity = orders.loc[i, 'processed_quantity']
        avg_price = orders.loc[i, 'price']
        total = round(avg_price * quantity * 100,2)


        symb_exp_strike_type = f'{symbol} {exp} {strike} {option_type}'

        if symb_exp_strike_type in symbol_strike_exp_type_list and exp < date.today():
            total_optionsloss -= total



    return round(total_optionsgain,2), round(total_optionsloss,2)
