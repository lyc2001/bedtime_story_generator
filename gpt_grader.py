#pip install openai

import os
from openai import OpenAI
import pandas as pd
import time

client = OpenAI(
    api_key="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",
)

def get_completion(story_1, story_2, emoji_1, emoji_2, emoji_3):

    prompt = "which story is better and more appropriate for kids and related to these three emojis " + emoji_1 + emoji_2 + emoji_3 + "? " + story_1 + story_2 + ". Please response with only one word, first or second."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    response_message = response.choices[0].message.content
    print(response_message)

    return response_message

def get_score(story_1, story_2, emoji_1, emoji_2, emoji_3): 
    # api call to get score, 0 for first story and 1 for second story being better 
    # and 0.5 for error

    response = get_completion(story_1, story_2, emoji_1, emoji_2, emoji_3)

    if response == "first" or "first.":
        return 0

    elif response == "second" or "second.":
        return 1

    else:
        print("error: response is not first or second")
        return 0.5
    
# example call to get_score
def main():
    story_1 = "In the park, a boy named Sam felt angry after an argument with his best friend, Alex. Their friendship had hit a rough patch, and harsh words were exchanged. As Sam sat on a bench, his anger subsided, replaced by regret. He realized the importance of their friendship and decided to make amends. With a sincere apology, the two friends reconciled, understanding that friendships could withstand anger and disagreements. The park, once a place of tension, transformed into a symbol of forgiveness, reminding them that true friendships can weather even the stormiest of emotions."
    story_2 = "In the park, a happy boy named Ethan spent a glorious afternoon with his best friend, Oliver. Their laughter echoed through the trees as they played games and shared stories. Their friendship was a source of pure joy, reminding Ethan that in the simple moments of happiness spent with a dear friend, life was truly beautiful. As the sun dipped below the horizon, Ethan and Oliver knew that their bond was unbreakable, and they looked forward to more adventures and happy times in the future, their hearts full of the warmth of their enduring friendship."
    print(get_score(story_1, story_2, "👦", "🏞️", "👭"))

if __name__ == "__main__":
    main()