# game/views.py
from django.shortcuts import render, redirect
from .models import Game, Player
import random

def home_view(request):
    return render(request, 'home.html')

def start_game_view(request):
    
    deck = create_deck()
    player_hand = deal_initial_cards(deck)
    dealer_hand = deal_initial_cards(deck)

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    
    player = Player.objects.create(name="Player 1")  
    game = Game.objects.create(
        player=player,
        player_hand=player_hand,
        dealer_hand=dealer_hand,
        deck=deck,
        dealer_score=dealer_score,
        player_score=player_score
    )

    # Store game details in session
    request.session['game_id'] = game.id

    context = {
        
        'game':game,
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
    }

    return render(request, 'game/game.html', context)

def create_deck():
    symbols = ['diamond', 'heart', 'club', 'spade']
    numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [(x, y) for x in numbers for y in symbols] * 5
    random.shuffle(deck)
    return deck

def deal_initial_cards(deck):
    hand = [deck.pop(0), deck.pop(0)]  
    return hand

def calculate_score(hand):
    game_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    result = 0
    aces = 0

    for card in hand:
        if card[0] == 'A':
            aces += 1
        result += game_dict[card[0]]

    while result > 21 and aces:
        result -= 10
        aces -= 1

    return result

from django.http import JsonResponse

def hit_view(request, game_id):

    game = Game.objects.get(id=game_id)

    if not game.is_active:
        return JsonResponse({'redirect': True, 'url': f'/result/{game.id}/'})

    deck = game.deck
    player_hand = game.player_hand

    new_card = deck.pop(0)
    player_hand.append(new_card)

    player_score = calculate_score(player_hand)

    game.player_hand = player_hand
    game.player_score = player_score
    game.deck = deck
    game.save()

    if player_score > 21:
        game.is_active = False
        game.save()
        return JsonResponse({'redirect': True, 'url': f'/result/{game.id}/'})

    return JsonResponse({
        'player_hand': player_hand,
        'player_score': player_score,
        'dealer_hand': game.dealer_hand,
        'is_active': game.is_active
    })


def stand_view(request, game_id):
    game = Game.objects.get(id=game_id)

    dealer_hand = game.dealer_hand
    dealer_score = game.dealer_score
    deck = game.deck

    while dealer_score < 17:
        new_card = deck.pop(0)
        dealer_hand.append(new_card)
        dealer_score = calculate_score(dealer_hand)

    game.dealer_hand = dealer_hand
    game.dealer_score = dealer_score
    game.is_active = False
    game.save()

    return redirect('game_result', game_id=game.id)

def result_view(request, game_id):
    game = Game.objects.get(id=game_id)

    dealer_hand = game.dealer_hand
    player_hand = game.player_hand

    if game.player_score > 21:
        game.game_result = "Dealer wins!"
    elif game.dealer_score > 21 or game.player_score > game.dealer_score:
        game.game_result = "You win!"
    elif game.player_score == game.dealer_score:
        game.game_result = "It's a draw!"
    else:
        game.game_result = "Dealer wins!"

    game.save()

    context = {
        'game':game,
        'player_hand': player_hand,
        'dealer_hand': dealer_hand 
    }

    return render(request, 'game/result.html', context)
