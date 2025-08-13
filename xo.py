class Board:
    def __init__(self):
        self.cells=[["__"for _ in range(3)]for _ in range(3)]
    def display(self):
        for row in self.cells:
            print("|".join(row))
    def update(self,row,col,symbol):
        row=row-1
        col=col-1
        if self.cells[row][col]=="__":
            self.cells[row][col]=symbol
            return True
        return False
    def is_full(self):
        return all(cell !="__" for row in self.cells for cell in row)
    def check_winner(self,symbol):
        for i in range(3):
            if all(self.cells[i][j]==symbol for j in range(3))or\
                    all(self.cells[j][i]==symbol for j in range(3)):
                return True
            if all(self.cells[i][2-i]==symbol for i in range(3))or all(self.cells[i][i]==symbol for i in range(3)):
                return True
            return False
class Player:
    def __init__(self,name,symbol):
        self.name=name
        self.symbol=symbol
class Game:
    def __init__(self,player1,player2):
        self.board=Board()
        self.players=[player1, player2]
        self.current_player=0
    def switch_turn(self):
        self.current_player=1-self.current_player
    def play(self):
        while True:
            self.board.display()
            player=self.players[self.current_player]
            print(f"turn {player.name}({player.symbol})")
            try:
                row = int(input("(3-1)Number row: "))
                col = int(input("(3-1 )Number column: "))
            except ValueError:
                print("Invalid row or column")
                continue
            if row<1 or row>3 or col<1 or col>3:
                print("Invalid row or column")
                continue
            if not self.board.update(row,col,player.symbol):
                print("Invalid move")
                continue
            if self.board.check_winner(player.symbol):
                self.board.display()
                print(f"winner is {player.name}")
                break
            if self.board.is_full():
                self.board.display()
                print(f"The game is tied")
                break
            self.switch_turn()

name1=input("enter one player name: ")
name2=input("enter two player name: ")
player1=Player(name1,"X")
player2=Player(name2,"O")
game=Game(player1,player2)
game.play()
