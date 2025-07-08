import random
import time
import sys
from json_handler import check_json, create_json, write_json, read_json



def play_game():

    def ask_difficulty():
        while True:
            try:
                dif = int(input("Select the difficulty: "))
                if dif in [1, 2, 3]:
                    return dif
                else:
                    print("Unrecognized value.\nTry: 1 (Easy), 2 (Medium), 3 (Hard)")
            except ValueError:
                print("Please enter a valid number (1, 2, or 3).")



    def give_chances(dif):
        #.. we return the number of chances based on the difficulty and the label to score the data
        if dif == 1:
            return 10, "easy"
        elif dif == 2:
            return 5, "medium"
        elif dif == 3:
            return 3, "hard"
    
    def play_again(won, number=None):
        if won:
            while True:
                ans = input("Wanna play again?[y/n]: ")
                #.. play again
                if ans.lower() == "y":
                    new_dif = ask_difficulty()
                    new_chances, new_label = give_chances(new_dif)
                    check_guess(new_chances, new_label)

                #.. No more playing
                elif ans.lower() == "n":
                    print("See ya...")
                    sys.exit()
                else:
                    print("Incorrect value, please type y or n to continue playing or exit.")
        else:
            #.. when the user lost we show what the number was and ask if he wants to keep playing
            ans = input(
                f"OOOhh, seems like you wasted all your chances. The number was {number}\n"
                "Wanna try again? [y/n]: "
            )
            while True:
                if ans.lower() == "y":
                    new_dif = ask_difficulty()
                    new_chances, new_label = give_chances(new_dif)
                    check_guess(new_chances, new_label)
                elif ans.lower() == "n":
                    print("See ya...")
                    sys.exit()
                else:
                    print("Incorrect value, please type y or n to continue playing or exit.")

    #.. store the results in a .json file (score.json)
    def save_results(dif, attempts, duration):
        result = {
            "Difficulty": dif,
            "Attempts": attempts,
            "Duration": round(duration, 2)
        }
 
        if not check_json("score.json"):
            create_json()
        
        try: 
           data = read_json()
           data.append(result)
           write_json(data)
        except:
            pass
        
                
            
        
    def check_guess(chances, dif):
        start = time.time()
        number_to_guess = random.randint(1, 100)
        #.. print(number_to_guess) --> to debug 
        player_attempts = 0

        while player_attempts < chances:        
            try:
                num = int(input("Enter your guess: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if num == number_to_guess:
                #.. if user guesses at the first chance we gotta change de var value
                if player_attempts == 0:
                    player_attempts = 1
                print(f"***CONGRATS, you guessed the correct number_to_guess in {player_attempts + 1 if player_attempts != 1 else player_attempts}" 
                        f" attemp{"s" if player_attempts != 1 else ""}, YOU WON!!***")
                end = time.time()
                duration = end - start  #.. duration of the game
                print(f"Time used to guess the number: {duration:.2f} sc")

                save_results(dif, player_attempts, duration)
                play_again(True)
            elif num > number_to_guess:
                print(f"Incorrect! The number is less than {num}")
                player_attempts += 1
            elif num < number_to_guess:
                print(f"Incorrect! The number is grater than {num}")
                player_attempts += 1

        #.. Once chances are wasted, we ask if user wants to keep playing
        
        play_again(False, number=number_to_guess)
        

    #.. STARTING THE GAME ..#        
    print("Welcome to Number-Guessing-Game!!")
    print("Im thinking of a number between 1 and 100")
    print(
        "\nPlease select the difficulty level: \n"
        "1. Easy (10 chances)\n"
        "2. Medium (5 chances)\n"
        "3. Hard (3 chances)\n"
    )
    difficulty = ask_difficulty()
        
    chances, label = give_chances(difficulty)
    check_guess(chances, label)

if __name__ == "__main__":
    play_game()