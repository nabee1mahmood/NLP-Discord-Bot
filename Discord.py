#********************************#
# Name: Nabeel Mahmood           #
# Username: <if applicable>      #
# Problem Set: PS2               #
# Due Date: October 1st, 2024    #
#********************************#


import discord
import math
import re
import random
from dotenv import load_dotenv
import os
from PS2 import predict_next_ten_words_trigrams
from PS2 import calc_bigram_log
from PS2 import calc_trigram_log
from PS2 import predict_next_word_bigram

from PS2 import unigram_lm



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    
    if message.content.startswith('$hello'):
        words = message.content.split()

        if len(words) >= 3:  
            w1, w2 = words[-2], words[-1]
            
        if len(words) == 2:  
            w1, w2 = words[0], words[1]


       
    
        predict_bigram = predict_next_word_bigram(w2, 10)
        bigram_log_prob = calc_bigram_log(w1, w2)
        predict_trigram = predict_next_ten_words_trigrams(w1, w2, 10)
        trigram_log_prob = calc_trigram_log(w1, w2)

        
        
    
        
      
        await message.channel.send(f'Bigram: {predict_bigram}')
        await message.channel.send(f'Bigram Log Probability: {bigram_log_prob}')
        await message.channel.send(f'Trigram: {predict_trigram}')
        await message.channel.send(f'Trigram Log Probability: {trigram_log_prob}')

        

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

client.run(token)