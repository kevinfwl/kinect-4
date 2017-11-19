from requests import get, post, put

RUN = 201
TRN = 202
INV = 203
WIN = 204

IP = 'http://4afdc283.ngrok.io'
#IP = 'http://localhost:5000'

def pretty(arr):
    print('')
    for row in arr:
        pr = ''
        for x in row:
            if x == 1:
                pr += 'X, '
            elif x == 0:
                pr += '-, '
            elif x == -1:
                pr += 'O, '
        print('[' + pr + ']')

def doTurn(num):
    query = IP + '/board/' + str(num-1)
    human = post(query, data={'data': 0})
    if human.status_code == RUN:
        pretty(human.json())
    elif human.status_code == TRN:
        print('not your turn')
    elif human.status_code == INV:
        print('invalid move')
        return 'inv'
    elif human.status_code == WIN:
        pretty(human.json())
        print('you won')
        return 'win'
    
    ai = post(IP + '/board/9', data={'data': 0})
    if ai.status_code == RUN:
        pretty(ai.json())
    elif ai.status_code == TRN:
        print('not its turn')
    elif ai.status_code == WIN:
        try:
            print(ai.json())
        except:
            print(ai.text)
        print('pc won')
        return 'win'
    return ''

def play(control, human_moves):
    put(IP + '/game')
    pretty(get(IP + '/board/1', data={'data':0}).json())
    move_count = 0
    while True:
        if control:
            num = int(input('\nSelect row (1-7): '))
            if doTurn(num) == 'win': break
        else:
            if move_count < len(human_moves):
                num = human_moves[move_count]
                print('\nSelect row (1-7): ' + str(num))
                if doTurn(num) == 'win': break
                move_count += 1
            else:
                control = True

lose = [1, 1, 7, 7, 2, 6]
lose2 = [4, 4, 1, 3, 5, 2, 6, 6, 2, 2, 6, 5, 7]
play(False, lose)