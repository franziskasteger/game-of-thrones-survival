🚗 **This project was created as the final project for the Le Wagon Datascience & AI bootcamp in Lisbon**

# Game of Thrones Survival ⚔️

I ♥️ Game of Thrones. And I ♥️ speculating about how long I would survive in a movie or TV show. So finally we were able to make a website that will create a character based on the user's character traits and then predict how long they would survive in **Game of Thrones**.

## Approach

📊 We used datasets available on **kaggle**, and did our own **webscraping** to enhance those datasets with more information.

🧹 The data cleaning was not as easy as expected, as we had to deal with many **missing values** and **duplicates**. Our scraped data helped us here, to fill in some of the missing values and give us enough information to impute the rest.

❓ We then moved on to building the quiz to create a character for the user. We created our own dataset that we used to map a user to one of 20 groups or houses Game of Thrones. This was not too complicated, but we needed to make sure that each group had a distinct set of **feature combinations**, as there couldn't be any duplicates in this dataset.

💀 Once the character creation was done, we built two **models** to predict whether the newly created character would die, and if so, in which season. Linear models turned out not to work very well, so we settled on using **XGBoost**.

📜 Additionally, our project involved the development of a storyline and images using **generative AI** from OpenAI. If the character is predicted to die in a certain season, this will create a story of death and a matching image. And if the character is lucky enough to survive, it will be a short tale of their life.
