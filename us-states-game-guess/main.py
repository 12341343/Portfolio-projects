import turtle
import pandas as pd
screen = turtle.Screen()
screen.title("US states game")
image = "blank_states_img.gif"
states = "50_states.csv"
screen.addshape(image)
turtle.shape(image)
score = 0
data = pd.read_csv(states)
states = data.state.to_list()
guessed_state = []
while score < 50:

    answer_state = screen.textinput(f"{score}/50 states correct", "What's another state name?").title()
    if answer_state == "Exit":
        missing_states = [state for state in guessed_state if state not in guessed_state]
        break
    if answer_state in states:
        guessed_state.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()

        state_data = data[data.state == answer_state]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(answer_state)
        score += 1
