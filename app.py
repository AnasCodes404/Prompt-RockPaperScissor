from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# HTML template for the game
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rock Paper Scissors Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 400px;
        }
        h1 {
            margin-bottom: 20px;
            color: #333;
        }
        .choices {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        .choice {
            font-size: 2rem;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .choice:hover {
            transform: scale(1.1);
        }
        .message {
            margin-top: 20px;
            font-size: 18px;
            color: #333;
        }
        .message.error {
            color: red;
        }
        .message.success {
            color: green;
        }
        .icon {
            font-size: 3rem;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body>
    <div class="container">
        <h1>Rock Paper Scissors</h1>
        <div class="choices">
            <div class="choice" onclick="play('rock')">
                <i class="fas fa-hand-rock icon"></i><br>Rock
            </div>
            <div class="choice" onclick="play('paper')">
                <i class="fas fa-hand-paper icon"></i><br>Paper
            </div>
            <div class="choice" onclick="play('scissors')">
                <i class="fas fa-hand-scissors icon"></i><br>Scissors
            </div>
        </div>
        <p id="message" class="message"></p>
    </div>

    <script>
        function play(choice) {
            fetch(`/play/${choice}`)
                .then(response => response.json())
                .then(data => {
                    const messageElement = document.getElementById('message');
                    messageElement.textContent = data.message;
                    messageElement.className = 'message ' + (data.success ? 'success' : 'error');
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/play/<choice>')
def play(choice):
    choices = ['rock', 'paper', 'scissors']
    if choice not in choices:
        return jsonify({'success': False, 'message': 'Invalid choice. Please select rock, paper, or scissors.'})

    computer_choice = random.choice(choices)
    result = determine_winner(choice, computer_choice)

    return jsonify({'success': True, 'message': f'You chose {choice}. Computer chose {computer_choice}. {result}'})

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return 'It\'s a tie!'
    elif (player_choice == 'rock' and computer_choice == 'scissors') or \
         (player_choice == 'paper' and computer_choice == 'rock') or \
         (player_choice == 'scissors' and computer_choice == 'paper'):
        return 'You win!'
    else:
        return 'You lose!'

if __name__ == '__main__':
    app.run(debug=True)
