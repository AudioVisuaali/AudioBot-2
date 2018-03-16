from asyncio import sleep as asleep
from random import randint

class Fishing:

    # Checking emoji reaction
    def emoji_check(self, reaction, user):
        return reaction.emoji.startswith(('✅', '❌'))

    async def main(self, bot, database, message, arguments):
        #TODO REMAKE THIS IS TRASH
        # Getting name
        name = bot.utils.author_nickanme(message.author)

        # Sending message
        temporary = await bot.say(message.channel, ":fishing_pole_and_fish: **| {} is fishing.... (wait)**".format(name))

        # Sleep for
        rsleep = randint(100, 300)
        await asleep(rsleep)

        # GET item rand
        randomizer_item = randint(0, 400)

        # What item
        if randomizer_item <= 10:
            spot = 0
        elif randomizer_item < 50:
            spot = 1
        else:
            spot = 2

        # Picking item randomly LUL
        kekk = self.fish_inv()
        hand = kekk[spot][randint(0, len(kekk[spot])-1)]

        # Sending message
        await bot.delete_message(temporary)
        temporary_reaction = await bot.say(message.channel, ":fishing_pole_and_fish: **| {}, you got {}! \n\nDo you want to sell it for: {} memes**".format(name, hand["name"], hand["value"]))

        # Add reactions
        for item_emoji in ["✅","❌"]:
            await bot.add_reaction(temporary_reaction, item_emoji)

        # Wait for reaction
        react_result = await bot.wait_for_reaction(user=message.author, timeout=30, check=self.emoji_check)

        # Del message
        await bot.delete_message(temporary_reaction)

        # If wanting to sell
        try:
            if react_result.reaction.emoji.startswith("✅"):

                # Must get at this point because updates and optimization
                users_wealth = bot.database.user.get(message.author.id).points
                bot.database.user.points_alter(message.author.id, hand["value"])

                bot.database.pointhistory.add(message.author.id, message.server.id, 4, "Fishing", False, "", "", "+"+str(hand["value"]), "", hand["display_name"], "", "", "", 0, hand["value"], 0)
                msg = ":fishing_pole_and_fish: **| {}, you got: {} from fishing! \n\nYou sold it for: {} memes and now have {}**".format(name, hand["name"], hand["value"], users_wealth+ hand["value"])

            # AFK or deny to sell
            else:
                msg = ":fishing_pole_and_fish: **| {}, you got {}, {} memes, but you chose to not sell it!**".format(name, hand["name"], hand["value"])
        except:
            msg = ":fishing_pole_and_fish: **| {}, you got {}, {} memes, but you chose to not sell it!**".format(name, hand["name"], hand["value"])

        # Send message
        await bot.say(message.channel, msg)

    def fish_inv(self):

        return [
                [{
                    "name": ":dvd:",
                    "display_name": "DVD",
                    "value": 200
                },{
                    "name": ":cd:",
                    "display_name": "CD",
                    "value": 150
                },{
                    "name": ":medal:",
                    "display_name": "Medal",
                    "value": 100
                },{
                    "name": ":blowfish:",
                    "display_name": "Blowfish",
                    "value": 80
                },{
                    "name": ":fish:",
                    "display_name": "Fish",
                    "value": 55
                },{
                    "name": ":tropical_fish:",
                    "display_name": "Tropical Fish",
                    "value": 75
                }],

                # 2
                [{
                    "name": ":eggplant:",
                    "display_name": "Eggplant",
                    "value": 20
                },{
                    "name": ":peach:",
                    "display_name": "Peach",
                    "value": 25
                },{
                    "name": ":banana:",
                    "display_name": "Banana",
                    "value": 18
                },{
                    "name": ":pizza:",
                    "display_name": "Pizza",
                    "value": 17
                },{
                    "name": ":rice_cracker:",
                    "display_name": "Rice Cracker",
                    "value": 22
                }],

                # 3
                [{
                    "name": ":soccer:",
                    "display_name": "Soccer",
                    "value": 1
                },{
                    "name": ":boot:",
                    "display_name": "Boots",
                    "value": 5
                },{
                    "name": ":coffin:",
                    "display_name": "Coffin",
                    "value": 4
                },{
                    "name": ":paperclip:",
                    "display_name": "Paperclip",
                    "value": 1
                },{
                    "name": ":mag_right:",
                    "display_name": "Magnifying Glass",
                    "value": 5
                },{
                    "name": ":shopping_cart:",
                    "display_name": "Shopping Cart",
                    "value": 5
                },{
                    "name": ":lock:",
                    "display_name": "Lock",
                    "value": 4
                },{
                    "name": ":triangular_ruler:",
                    "display_name": "Triangular Ruler",
                    "value": 1
                },{
                    "name": ":poop:",
                    "display_name": "PASKAA",
                    "value": 2
                },{
                    "name": ":mans_shoe:",
                    "display_name": "Shoe",
                    "value": 1
                },{
                    "name": ":umbrella:",
                    "display_name": "Umbrella",
                    "value": 4
                }]
        ]
