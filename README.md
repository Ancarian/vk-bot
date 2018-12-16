# vk-downloader

Its torrent downloader with remote access to your system by using VK Bot Api

steps:
1. you send command from your remote phone/compute/etc using VK bot
2. server(for example Raspberry PI media centre) execute that command
3. server send you result

allowed commands:
1. commands
2. stats. Return statistic of mem, cpu and hard drive
3. torrents. Return list of all torrents (pattern 'id. torrent's name')
4. pause [id]. Pause torrent
5. pauseAll. Pause all torrents
6. resume [id]. Resume torrent
7. resumeAll. Resume all torrents
8. pausedownloaded. Pause all downloaded torrents
9. delete [id]. Delete torrent from torrents list and hard drive(but if torrent files not in use) 
