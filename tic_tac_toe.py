import streamlit as st
import random
from typing import List

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
    
    def make_move(self, position: int) -> bool:
        if self.board[position] == ' ' and not self.game_over:
            self.board[position] = self.current_player
            self.check_winner()
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                self.winner = self.board[combo[0]]
                self.game_over = True
                return
        
        if ' ' not in self.board:
            self.game_over = True
    
    def get_empty_positions(self) -> List[int]:
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def minimax(self, is_maximizing: bool, alpha: float = float('-inf'), beta: float = float('inf')) -> int:
        if self.winner == 'O': return 1
        elif self.winner == 'X': return -1
        elif self.game_over: return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for move in self.get_empty_positions():
                self.board[move] = 'O'
                self.check_winner()
                score = self.minimax(False, alpha, beta)
                self.board[move] = ' '
                self.winner = None
                self.game_over = False
                
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha: break
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_empty_positions():
                self.board[move] = 'X'
                self.check_winner()
                score = self.minimax(True, alpha, beta)
                self.board[move] = ' '
                self.winner = None
                self.game_over = False
                
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha: break
            return best_score
    
    def get_best_move(self) -> int:
        best_score = float('-inf')
        best_move = None
        
        for move in self.get_empty_positions():
            self.board[move] = 'O'
            self.check_winner()
            score = self.minimax(False)
            self.board[move] = ' '
            self.winner = None
            self.game_over = False
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

def initialize_session_state():
    if 'game' not in st.session_state:
        st.session_state.game = TicTacToe()
    if 'player_symbol' not in st.session_state:
        st.session_state.player_symbol = 'X'
    if 'ai_difficulty' not in st.session_state:
        st.session_state.ai_difficulty = 'Hard'
    if 'theme' not in st.session_state:
        st.session_state.theme = 'Light'
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

def reset_game():
    st.session_state.game = TicTacToe()
    st.session_state.game_started = True

def apply_theme(theme: str):
    if theme == 'Dark':
        st.markdown("""
            <style>
            .main { background-color: #0E1117; color: #FAFAFA; }
            .stButton>button { background-color: #262730; color: white; height: 80px; font-size: 20px; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .main { background-color: #FFFFFF; color: #31333F; }
            .stButton>button { background-color: #F0F2F6; color: #31333F; height: 80px; font-size: 20px; }
            </style>
        """, unsafe_allow_html=True)

def render_game_board():
    game = st.session_state.game
    cols = st.columns(3)
    
    for i in range(9):
        with cols[i % 3]:
            if game.board[i] == ' ':
                if st.button(' ', key=f'btn_{i}', use_container_width=True, disabled=game.game_over):
                    if game.make_move(i):
                        if not game.game_over and game.current_player == 'O':
                            ai_move()
                            st.rerun()
            else:
                btn_color = "#FF4B4B" if game.board[i] == 'X' else "#00D4B1"
                st.markdown(f"""
                    <div style='background-color: {btn_color}; color: white; padding: 25px 0; 
                    text-align: center; border-radius: 5px; font-size: 24px; font-weight: bold;'>
                    {game.board[i]}
                    </div>
                """, unsafe_allow_html=True)

def ai_move():
    game = st.session_state.game
    if st.session_state.ai_difficulty == 'Easy':
        empty_positions = game.get_empty_positions()
        if empty_positions:
            game.make_move(random.choice(empty_positions))
    else:
        best_move = game.get_best_move()
        if best_move is not None:
            game.make_move(best_move)

def render_game_result():
    game = st.session_state.game
    if game.winner:
        if game.winner == st.session_state.player_symbol:
            st.success("🎉 You Win!")
        else:
            st.error("🤖 AI Wins!")
    elif game.game_over:
        st.info("🤝 Tie!")

def main():
    initialize_session_state()
    apply_theme(st.session_state.theme)
    
    st.title("Tic Tac Toe AI 🎮")
    
    if not st.session_state.game_started:
        st.header("Welcome to Tic Tac Toe!")
        st.write("Challenge our AI in this classic game!")
        
        with st.sidebar:
            st.header("⚙️ Settings")
            st.session_state.player_symbol = st.radio("Your symbol:", ['X', 'O'])
            st.session_state.ai_difficulty = st.selectbox("AI Difficulty:", ['Easy', 'Hard'])
            st.session_state.theme = st.radio("Theme:", ['Light', 'Dark'])
            
            if st.button("🎮 Start Game", use_container_width=True):
                reset_game()
                st.rerun()
        
    else:
        st.header("Game On!")
        
        if not st.session_state.game.game_over:
            current_symbol = st.session_state.game.current_player
            player_turn = "Your turn" if current_symbol == st.session_state.player_symbol else "AI's turn"
            st.subheader(f"{player_turn} ({current_symbol})")
        
        render_game_board()
        
        if st.session_state.game.game_over:
            render_game_result()
            if st.button("🔄 Play Again", use_container_width=True):
                reset_game()
                st.rerun()
        
        if st.button("← Back to Menu", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()

if __name__ == "__main__":
    main()