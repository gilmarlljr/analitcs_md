from empath import Empath

lexicon = Empath()

print(lexicon.analyze("I receive messages from people I don't know weekly telling me of her condition. She is scamming people of money and they are turning to me for advice.It is taking a severe toll on my mental health at this point, I am struggling with anxiety and slipping into a depression again. It takes a toll having literally no family and trying to put yourself through school, work two jobs and have a stable normal life at 23."
                , normalize=True))
print(lexicon.create_category("games", ["games"], model="reddit"))