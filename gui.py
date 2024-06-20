import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLabel, QLineEdit

from browserfile_checker import convert_to_json, save_json_file
from spotify_module import get_spotify_client, get_liked_songs, get_spotify_playlists
from ytmusic_module import YTMusic, create_ytmusic_playlists, create_liked_songs_playlist
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify to YouTube Music Transfer")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.info_label = QLabel("Transfer Spotify Playlists to YouTube Music", self)
        layout.addWidget(self.info_label)

        self.client_id_input = QLineEdit(self)
        self.client_id_input.setPlaceholderText("Enter Spotify Client ID")
        layout.addWidget(self.client_id_input)

        self.client_secret_input = QLineEdit(self)
        self.client_secret_input.setPlaceholderText("Enter Spotify Client Secret")
        layout.addWidget(self.client_secret_input)

        self.redirect_uri_input = QLineEdit(self)
        self.redirect_uri_input.setPlaceholderText("Enter Spotify Redirect URI")
        layout.addWidget(self.redirect_uri_input)

        self.raw_data_input = QTextEdit(self)
        self.raw_data_input.setPlaceholderText("Enter the RequestHeader raw data from Firefox")
        layout.addWidget(self.raw_data_input)

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        self.start_button = QPushButton("Start Transfer", self)
        self.start_button.clicked.connect(self.start_transfer)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_transfer(self):
        client_id = self.client_id_input.text()
        client_secret = self.client_secret_input.text()
        redirect_uri = self.redirect_uri_input.text()
        raw_data = self.raw_data_input.toPlainText()

        if not client_id or not client_secret or not redirect_uri or not raw_data:
            self.log_text.append("Please enter all required fields (Spotify API credentials and raw data).")
            return

        self.log_text.append("Generating browser.json file...")
        try:
            json_data = convert_to_json(raw_data)
            save_json_file("browser.json", json_data)
            self.log_text.append("browser.json file has been generated.")
        except Exception as e:
            self.log_text.append(f"Error generating browser.json: {str(e)}")
            logger.error("Error generating browser.json: %s", str(e))
            return

        self.log_text.append("Fetching playlists and liked songs from Spotify...")
        logger.info("Fetching playlists and liked songs from Spotify...")

        try:
            sp = get_spotify_client(client_id, client_secret, redirect_uri)
            spotify_playlists = get_spotify_playlists(sp)
            liked_songs = get_liked_songs(sp)
            self.log_text.append("Creating YouTube Music playlists and adding liked songs...")
            logger.info("Creating YouTube Music playlists and adding liked songs...")
            ytmusic_instance = YTMusic('browser.json')
            create_ytmusic_playlists(ytmusic_instance, spotify_playlists)
            create_liked_songs_playlist(ytmusic_instance, liked_songs)
            self.log_text.append("Transfer complete.")
            logger.info("Transfer complete.")
        except Exception as e:
            self.log_text.append(f"Error occurred: {str(e)}")
            logger.error("Error occurred during transfer: %s", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
