from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import pyqtSlot

class Game(QMainWindow):
    def __init__(self):
        super().__init__()

        # Combo box for game selection
        self.combo = QComboBox(self)
        self.combo.addItem("PowerBall")
        # self.combo.addItem("Mega Millions")
        # self.combo.addItem("Classic Lotto")
        self.combo.move(150, 100)

        # Label for game selection
        self.qlabel = QLabel("Select Game:", self)
        self.qlabel.move(50, 100)

        # Combo box for year selection
        self.combo_1 = QComboBox(self)
        self.combo_1.addItems(["2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016"])
        self.combo_1.move(150, 150)

        # Label for year selection
        self.qlabel_year = QLabel("Select Year:", self)
        self.qlabel_year.move(50, 150)

        # Download button
        self.button = QPushButton('Download', self)
        self.button.move(100, 250)
        self.button.clicked.connect(self.run)

        # Status label
        self.label = QLabel(self)
        self.label.setGeometry(200, 200, 200, 30)

        # Set main window properties
        self.setGeometry(50, 50, 500, 400)
        self.setWindowTitle("Web Mining Program")
        self.show()

    @pyqtSlot()
    def run(self):
        content_game = self.combo.currentText()
        content_date = self.combo_1.currentText()

        if content_game == "PowerBall":
            url = f"https://www.powerball.com/previous-results?gc=powerball&sd={content_date}-01-01&ed={content_date}-12-31"
            self.powerball(url)

    def powerball(self, url):
        try:
            df = pd.DataFrame(columns=['Date', 'White Balls', 'Power Ball', 'Power Play Multiplier', 'Sum of Numbers'])

            for i in range(1, 3000):
                new_url = url + "&pg=" + str(i)
                response = requests.get(new_url)

                if response.status_code != 200:
                    print(f"Error: Unable to fetch data from URL. Status code: {response.status_code}")
                    df.to_excel('powerball1.xlsx', index=False)
                    print("Data saved to powerball1.xlsx")
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                table = soup.find_all("div", {"class": "card-body ps-3 pe-4 pe-lg-5"}) 
                
                Is_Not_Matched = soup.find('div', class_='text-danger')
                if  Is_Not_Matched:
                    print(f"Error: Unable to fetch data from URL. Status code: {response.status_code}")
                    df.to_excel('powerball1.xlsx', index=False)
                    print("Data saved to powerball1.xlsx")
                    break

                for item in table:
                    try:
                        game_ball_group = item.find('div', class_='game-ball-group')
                        date_div = item.find('h5', class_='card-title')

                        white_balls = [int(ball.text) for ball in game_ball_group.find_all('div', class_='white-balls')]
                        powerball = int(game_ball_group.find('div', class_='powerball').text)
                        power_play_multiplier = int(item.find('span', class_='multiplier').text.replace('x', ''))
                        date_text = date_div.text.strip()

                        sum_of_numbers = sum(white_balls) + powerball

                        # Append data to DataFrame
                        df = pd.concat([df, pd.DataFrame({'Date': [date_text],
                                                         'White Balls': [white_balls],
                                                         'Power Ball': [powerball],
                                                         'Power Play Multiplier': [power_play_multiplier],
                                                         'Sum of Numbers': [sum_of_numbers]})], ignore_index=True)

                    except Exception as e:
                        df.to_excel('powerball1.xlsx', index=False)
                        print("Data saved to powerball1.xlsx")
                        print(f"An error occurred while processing an item: {e}")
                        continue

            df.to_excel('powerball1.xlsx', index=False)
            print("Data saved to powerball1.xlsx")
        
        except Exception as e:
            df.to_excel('powerball1.xlsx', index=False)
            print("Data saved to powerball1.xlsx")
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())
