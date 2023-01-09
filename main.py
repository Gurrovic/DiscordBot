import discord
import random
import requests
import json
from discord.ext import commands
from discord import app_commands

API_KEY = "913c4fca-1a7e-4a1a-8b6b-781b0315c8c8"
TOKEN = "MTA1NzcxNzQ5MjM0NjI2MTU4NA.G6k9MH.N6lc4fKbaTE-Kg4lg3BOlrKaqIniWYlGF0g8Ac"
bot = commands.Bot(command_prefix=".", intents=discord.Intents().all())


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


def dadjoke():
    url = "https://dad-jokes.p.rapidapi.com/random/joke"
    headers = {
        "X-RapidAPI-Key": "c97ea713eemshca13ec3d5baf015p14ee4fjsn2fe4ad44d794",
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    quote = json_data["body"][0]["setup"] + " " + json_data["body"][0]["punchline"]
    return quote


def dogfact():
    response = requests.get("https://some-random-api.ml/facts/dog")
    json_data = json.loads(response.text)
    fact = json_data["fact"]
    return fact


def dog():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    res = response.json()
    em = discord.Embed()
    em.set_image(url=res["message"])
    return em


sad_words = [
    "sad",
    "depressed",
    "unhappy",
    "angry",
    "miserable",
    "depressing"
]

starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person / bot!"
]

wim_hof = [
    "“If you can learn how to use your mind, anything is possible.“",
    "“I'm not afraid of dying. I'm afraid not to have lived.“",
    "“You are a great person / bot!“",
    "“Make it simple for yourself by calming your mind from anger, understanding what makes you sad, "
    "and replicating the experiences that make you happy. If you want strength and success, just do it!“",
    "“Cold is a stressor, so if you are able to get into the cold and control your body’s response to it, you will be able to control stress.“",
    "“People come up to me with questions like, “Should I breathe through the nose?” or “The diaphragm this or that,” "
    "and I just say, “Yeah breathe, motherfuckers! Don’t think, just do it! Get into the depth of your own lungs!“",
    "“We can do more than what we think. Its a belief system that I have adopted and it has become my motto. There is "
    "more than meets the eye and unless you are willing to experience new things, you'll never realize your full potential.“",
    "“Give it all you got!“",
    "“Cold is merciless. It shows you where you are. What you are.“",
    "“That's what nature meant us to do, breathe deep when we are stressed.“",
    "“I think of the cold as a noble force.“",
    "“I never had a teacher, and I never had lessons, other than hard Nature itself.“",




]


@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}! This is a slash command!",
                                            ephemeral=True)


@bot.tree.command(name="say")
@app_commands.describe(thing_to_say="What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")


@bot.event
async def on_message(message):
    # await bot.process_commands(message)
    if message.author == bot.user:
        return

    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username} said: '{user_message}' in channel [{channel}]")

    if channel == "bot":
        if user_message == ".roll":
            await message.channel.send(f"{username} rolled a dice and got: [{str(random.randint(1, 6))}]")
            return
        if message.content.startswith('.random'):
            dice_args = message.content.split()
            if len(dice_args) == 1:
                await message.channel.send(f"{username}'s RNG: [{str(random.randint(1, 100))}]")
                return
            if len(dice_args) == 2:
                try:
                    maxNumber = int(dice_args[1])
                    await message.channel.send(f"{username}'s RNG: [{random.randint(1, maxNumber)}]")
                except ValueError:
                    await message.channel.send(
                        'Invalid input. Use .random [number] to roll a random number with max number [number]')
            else:
                await message.channel.send(
                    'Invalid input. Use .random [number] to roll a random number with max number [number]')

        if user_message == ".hello":
            await message.channel.send(f"Hello {username}!")
            return

        if user_message == ".quote":
            await message.channel.send(get_quote())
            return

        if user_message == ".dadjoke":
            await message.channel.send(dadjoke())
            return

        if user_message == ".dogfact":
            await message.channel.send(dogfact())
            return

        if user_message == ".dog":
            await message.channel.send(embed=dog())
            return

        if message.content.startswith('.guess'):
            await message.channel.send('Guess a number between 1 and 10')

            random_number = random.randint(1, 10)
            guess = await bot.wait_for('message')
            if guess.content.isdigit() and 1 <= int(guess.content) <= 10:
                if int(guess.content) == random_number:
                    await message.channel.send('You are right!')
                else:
                    await message.channel.send('Sorry. Correct number is: ' + str(random_number))

        if user_message == ".ping":
            await message.channel.send(f"My latency is: {round(bot.latency * 1000)}ms")
            return

        if user_message == ".help":
            await message.channel.send(
                "Available commands:\n.hello\n.quote\n.dadjoke\n.dogfact\n.dog\n.roll\n"
                ".random\n.guess\n.ping\n.wimhof\n.help\n.rps")
            return

        if user_message == ".wimhof":
            await message.channel.send(random.choice(wim_hof))
            return

        if any(word in user_message for word in sad_words):
            await message.channel.send(random.choice(starter_encouragements))
            return

        if message.content.startswith(".rps"):
            score_player = 0
            score_bot = 0
            started = False
            await message.channel.send('ROCK - PAPER - SCISSORS')
            while True:
                await message.channel.send('Choose rock, paper, or scissors. Or quit to exit.')

                if started:
                    await message.channel.send(f"My score: {score_bot}")
                    await message.channel.send(f"Your score: {score_player}")
                cmd = await bot.wait_for('message')
                cmd = str(cmd.content)
                if cmd == "quit":
                    await message.channel.send('Game over!')
                    break
                if cmd not in ["rock", "paper", "scissors"]:
                    await message.channel.send("Please choose either rock, paper, or scissors.")
                    return
                bot_choice = random.choice(["rock", "paper", "scissors"])
                if cmd == "rock":
                    if bot_choice == "rock":
                        await message.channel.send("It's a tie! We both chose [rock]. Nobody gets points.")
                    elif bot_choice == "paper":
                        await message.channel.send("I win! [Paper] beats [rock]. I get a point!")
                        score_bot += 1
                    else:
                        await message.channel.send("You win! [Rock] beats [scissors]. You get a point!")
                        score_player += 1
                elif cmd == "paper":
                    if bot_choice == "rock":
                        await message.channel.send("You win! [Paper] beats [rock]. You get a point!")
                        score_player += 1
                    elif bot_choice == "paper":
                        await message.channel.send("It's a tie! We both chose [paper]. Nobody gets points.")
                    else:
                        await message.channel.send("I win! [Scissors] beats [paper]. I get a point!")
                        score_bot += 1
                else:
                    if bot_choice == "rock":
                        await message.channel.send("I win! [Rock] beats [scissors]. I get a point!")
                        score_bot += 1
                    elif bot_choice == "paper":
                        await message.channel.send("You win! [Scissors] beats [paper]. You get a point!")
                        score_player += 1
                    else:
                        await message.channel.send("It's a tie! We both chose [scissors]. Nobody gets points.")
                started = True

        if message.content.startswith('.hangman'):
            word_list = ['apple', 'banana', 'orange', 'strawberry']
            word = random.choice(word_list)
            word_letters = set(word)
            alphabet = set('abcdefghijklmnopqrstuvwxyz')
            used_letters = set()
            lives = 6

            def check_win(guessed_word=""):
                if set(guessed_word) == word_letters:
                    return True
                else:
                    return False

            def check_lost():
                if lives <= 0:
                    return True
                else:
                    return False

            def get_word_string():
                word_string = ''
                for letter in word:
                    if letter in used_letters:
                        word_string += letter
                    else:
                        word_string += '-'
                print(word_string)
                return word_string

            def get_lives_string():
                return 'Lives: ' + str(lives)

            def get_used_letters_string():
                return 'Used letters: ' + ' '.join(sorted(used_letters))

            await message.channel.send('Welcome to Hangman!')
            await message.channel.send('Here is the word:')
            await message.channel.send(get_word_string())
            await message.channel.send(get_lives_string())
            await message.channel.send(get_used_letters_string())

            while not check_win() and not check_lost():
                await message.channel.send('Guess a letter:')
                user_guess = await bot.wait_for('message')
                user_guess = user_guess.content.lower()
                if user_guess in alphabet - used_letters:
                    used_letters.add(user_guess)
                    if user_guess in word_letters:
                        word_letters.remove(user_guess)
                        await message.channel.send('Nice! The letter is in the word.')
                    else:
                        lives -= 1
                        await message.channel.send('Sorry, the letter is not in the word.')
                elif user_guess in used_letters:
                    await message.channel.send('You already used that letter. Guess another letter:')
                else:
                    await message.channel.send('Invalid input. Enter a letter:')

                await message.channel.send(get_word_string())
                await message.channel.send(get_lives_string())
                await message.channel.send(get_used_letters_string())

            if check_win():
                await message.channel.send('You won! The word was: ' + word)
            elif check_lost():
                await message.channel.send('You lost! The word was: ' + word)

bot.run(TOKEN)
