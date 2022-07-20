# Analysis of sentiment: opinions about the Game of Thrones
## Scraping

Opinions.py loads the page with comments of users about the book "Game of Thrones". The program waits for loaded page and accepts cookies. Then it scrapes the content
of each comment and the rating value which user decided to put under his comment.

If all comments on particular subpage are scraped the script clicks "next page" button and repeat the process.

![image](https://user-images.githubusercontent.com/34272444/179871730-4461035a-1b25-4cc0-97d4-2348627a5d78.png)

Downloaded data (with text and rating) was used to train simple LSTM model. The goal is to predict rating which should be assigned to comments without rating.
