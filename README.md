SpotiYouti v0.1.0


Welcome to SpotiYouti!

You can use this application to transfer all your playlists and liked songs from Spotify to YouTube Music.


Requirements & Usage:

1.Spotify Client ID, Client Secret, and Redirect URI. 
  
  Follow this video tutorial to obtain these credentials  ( https://www.youtube.com/watch?v=ZriGgdo_JDA )

2.Mozilla Firefox:

Open YouTube Music in Firefox and log in to your account.
Go to the application menu > More Tools > Web Developer Tools.
Navigate to the Network tab in the developer tools and type /browse in the filter box.
Find a POST request, right-click on it, and select "Copy Value" > "Copy Request Headers".


Extract and Run:

Extract the .rar file from the build folder.
Run SpotiYouTi.exe.
You'll see a window similar to the one below:
![spoti](https://github.com/AatomiccB/transfer_between_spotify_and_ytmusic/assets/173203205/1101301b-9c0c-4ff7-8657-e28571049a91)



Steps:

Paste the copied raw request header data fromFirefox into the designated area.
Enter your Spotify credentials in the corresponding boxes.
Hit "Start Transfer" to begin.
For now, you can start and stop transfers.


Future Updates:

Adding the ability to pause and resume transfers.

Displaying logs within the application.

Adding an estimated time timer for the transfers.

Thank you for using SpotiYouti!


