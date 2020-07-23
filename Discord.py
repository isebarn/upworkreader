import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message.content.startswith('clear'))
    print(message.content.startswith('clear'))

    print(1)
    if message.content.startswith('clear'):
      print(2)
      channel = client.get_channel(732680171143954482)
      history = await channel.history(limit=200).flatten()
      counter = 0
      for message in history:
        counter += 1
        print("Deleted: {}/{}".format(counter, len(history)))

        try:
          await message.delete()
        except Exception as e:
          print('Cannot')


client.run('NzMyNzEwMzYxMDE0NDY4NzA2.Xw4j6Q.bV2KjT3_dCAGjosSTTv_7pYeEWI')
