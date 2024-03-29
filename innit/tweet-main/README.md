# GPT Tweet Generation

Live version of this app at [tweets.streamlit.app](https://tweets.streamlit.app)

## Description

This [Streamlit](https://streamlit.io) mini-app generates Tweet texts using OpenAI's [GPTs](https://beta.openai.com/docs/models/overview) for texts and [DALL·E](https://beta.openai.com/docs/guides/images) for images.

The text prompt creation form accepts a topic as well as an optional mood parameter and a Twitter account for "style transfer" (Update: Due to Twitter's new API [limits](https://developer.twitter.com/en/docs/twitter-api/rate-limits) style transfer likely does not work anymore). The app then generates a prompt with an instruction to write a respective Tweet and sends this to the OpenAI API which - using one of their GPT models that have been trained on a lot of publicly available text content - predicts the next likely to be used (word) tokens and thus generates the Tweet content. Furthermore, the app can request and display an image from OpenAI's DALL·E model using the previously generated Tweet text as a prompt.

## Contribution

I hope this will be of value to people seeking to understand GPTs' current capabilities and the overall progress of natural language processing (NLP) and generative AI. Plus maybe you can even use the app to generate some interesting Tweets for your Twitter account.

Please reach out to me at nikolas@schriefer.me with any feedback - especially suggestions to improve this - or questions you might have.
