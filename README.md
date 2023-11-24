# GermanX

Tab 1:
Used for practicing German prepositions.
Displays a random preposition and a word in German.
The user selects the correct preposition from the provided options.
Tracks correct and incorrect answers, as well as the number of learned words.

Tab 3:
Used for adding and removing words from the dictionary.
Words are saved in a JSON file (data_deutsch_word.json).
Provides the ability to specify the article, word, ending, and type of the word.

Button Images:
Each button on Tab 1 has an image representing different actions (start, restart, etc.).

Data Saving and Loading:
Data such as learned words is saved to the data_deutsch_word.json file.
The application automatically loads words from the file on startup.

Exception Handling:
Exception handling is implemented for cases such as missing data files and other possible errors.

Logging:
The logging module is used to log events in the application.

User Interface:
The application interface is created using the Qt Designer program (untitled.ui).

Dictionary Addition:
Users can add new words to the dictionary by specifying the article, word, ending, and word type.

## Launching the application
To launch the application, follow these steps:
Install the required dependencies:

   ```bash
   pip install -r requirements.txt
