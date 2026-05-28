COMMANDS = {
    "decrease_volume": [
        "decrease the volume", "turn down the volume", "lower the volume",
        "volume down", "make it quieter", "reduce the sound", "turn it down",
        "can you lower the volume", "too loud turn it down", "bring the volume down",
        "less volume please", "quiet it down", "reduce volume", "sound down",
        "can you reduce the volume", "it is too loud", "lower it a bit",
        "volume is too high", "bring it down", "sound too loud lower it",
        "please decrease the volume", "make the sound lower", "turn down",
        "volume kam karo", "thoda kam karo", "bahut loud hai",
    ],

    "increase_volume": [
        "increase the volume", "turn up the volume", "raise the volume",
        "volume up", "make it louder", "louder please", "turn it up",
        "can you increase the volume", "i cannot hear bump it up", "crank up the volume",
        "more volume", "sound is too low turn it up", "raise the sound",
        "volume badao", "thoda aur loud karo", "sunai nahi de raha",
        "sound up please", "increase sound", "make it louder please",
        "can you raise the volume", "too low turn it up", "boost the volume",
        "pump up the volume", "sound zyada karo", "aur loud karo",
    ],

    "play_music": [
        "play the music", "start the music", "play music", "resume the music",
        "start playing", "play something", "turn on the music", "play a song",
        "start the song", "resume playback", "hit play", "play it",
        "music chalao", "gaana chalao", "start music", "begin playback",
        "play some music", "turn music on", "start playing music",
        "can you play music", "music start karo", "gaana shuru karo",
        "play audio", "resume music", "continue playing",
    ],

    "pause_music": [
        "pause the music", "stop the music", "pause the song", "pause it",
        "stop playing", "hold the music", "can you pause", "put the music on hold",
        "pause playback", "stop the song for now", "freeze the music", "pause please",
        "music roko", "gaana band karo", "hold on pause it", "stop music",
        "can you stop the music", "pause for a moment", "music rok do",
        "stop the audio", "hold music", "pause this song",
        "stop playing please", "pause music please", "music pause karo",
    ],

    "pick_up_call": [
        "pick up the call", "answer the call", "accept the call", "answer the phone",
        "pick up", "take the call", "receive the call", "answer it",
        "get the call", "yes answer", "pick up the phone", "accept incoming call",
        "call uthao", "phone uthao", "haan uthao", "attend the call",
        "receive incoming call", "answer please", "pick it up", "take the phone",
        "yes pick up", "answer the incoming call", "attend this call",
        "pickup the call", "get the phone",
    ],

    "decline_call": [
        "decline the call", "reject the call", "ignore the call", "do not answer",
        "dismiss the call", "hang up", "reject it", "send to voicemail",
        "decline incoming call", "no do not pick up", "cancel the call", "refuse the call",
        "call mat uthao", "nahi uthana", "cut the call", "disconnect the call",
        "do not receive the call", "reject please", "ignore it", "dismiss it",
        "send call to voicemail", "nahi chahiye call", "call cut karo",
        "decline this call", "do not answer the phone",
    ],

    "play_next_song": [
        "play the next song", "skip to next", "next song", "next track",
        "skip this song", "play the next track", "go to next song",
        "forward to next", "skip ahead", "change the song", "next one please", "skip it",
        "agla gaana chalao", "next gaana", "skip karo", "agle gaane pe jao",
        "go next", "next please", "move to next song", "forward song",
        "play next", "skip to the next one", "next track please",
        "change track", "agle gaane par",
    ],

    "play_previous_song": [
        "play the previous song", "go back to previous song", "previous track",
        "previous song", "last song", "play the last track", "go back one song",
        "rewind to previous", "back to previous", "play that last one again",
        "previous one please", "go back",
        "pichla gaana chalao", "wapas jao", "pehle wala gaana",
        "back song", "previous please", "go to last song", "play previous",
        "last track please", "rewind", "pichle gaane par jao",
        "play the song before", "go back one track", "previous gaana",
    ],

    "activate_dnd": [
        "activate do not disturb", "turn on do not disturb", "enable do not disturb",
        "do not disturb me", "activate dnd", "turn on dnd", "put on do not disturb",
        "i do not want to be disturbed", "enable dnd mode", "switch on do not disturb",
        "no disturbances please", "activate quiet mode",
        "disturb mat karo", "dnd on karo", "mujhe disturb mat karo",
        "silent mode on", "quiet mode activate", "notifications band karo",
        "do not disturb on", "enable quiet mode", "dnd lagao",
        "switch to dnd", "put on dnd mode", "no interruptions please",
    ],

    "deactivate_dnd": [
        "deactivate do not disturb", "turn off do not disturb", "disable do not disturb",
        "deactivate dnd", "turn off dnd", "disable dnd mode",
        "switch off do not disturb", "remove do not disturb", "cancel do not disturb",
        "i am available now", "turn off quiet mode", "disable quiet mode",
        "dnd hatao", "dnd band karo", "disturb karo ab", "notifications on karo",
        "remove dnd", "cancel dnd", "quiet mode off", "dnd off karo",
        "disable silent mode", "turn off dnd mode", "deactivate quiet mode",
        "i am back switch off dnd", "end do not disturb",
    ],
}


OUT_OF_SCOPE = [
    "what is the weather today", "open google maps", "how long until i reach home",
    "call mom", "what time is it", "set an alarm for 7am",
    "navigate to the nearest petrol station", "send a message to john",
    "what is the temperature outside", "open spotify",
    "how far is the nearest hospital", "remind me to buy groceries",
    "turn on the air conditioning", "what day is it today",
    "find a restaurant nearby", "how much fuel do i have",
    "read my messages", "translate hello to french",
    "what is the speed limit here", "open my calendar",
    "take a photo", "turn on bluetooth", "connect to wifi",
    "check my emails", "who is calling",
    "increase bass", "play movie", "stop playlist",
    "open youtube", "set reminder", "check traffic",
    "what song is this", "search for music", "play podcast",
    "turn on wifi", "read notifications", "open maps",
    "call office", "book a cab", "check battery",
]


EXTENSION_COMMANDS = {
    "increase_brightness": [
        "increase the brightness", "turn up the brightness", "make it brighter",
        "brightness up", "raise the brightness", "screen is too dim increase it",
        "higher brightness please", "more brightness", "brighten the screen",
        "can you increase screen brightness",
        "brightness badao", "screen roshan karo", "thoda bright karo",
        "screen dim hai increase karo", "brightness zyada karo",
        "make screen brighter", "up the brightness", "screen brightness up",
        "increase screen light", "brighter please",
    ],

    "decrease_brightness": [
        "decrease the brightness", "turn down the brightness", "make it dimmer",
        "brightness down", "lower the brightness", "reduce screen brightness",
        "screen is too bright lower it", "less brightness please",
        "dim the screen", "can you decrease the brightness",
        "brightness kam karo", "screen thanda karo", "thoda dim karo",
        "screen bahut bright hai", "brightness ghata do",
        "make screen dimmer", "down the brightness", "screen brightness down",
        "reduce screen light", "dimmer please",
    ],

    "start_vehicle": [
        "start the vehicle", "start the car", "turn on the car",
        "engine start", "start the engine", "ignition on",
        "fire up the engine", "turn the car on", "start it up", "power on the vehicle",
        "gaadi start karo", "car on karo", "engine on karo",
        "ignition start", "vehicle start karo", "car chalao",
        "start engine please", "power up the car", "vehicle on karo",
        "turn on engine",
    ],

    "stop_vehicle": [
        "stop the vehicle", "stop the car", "turn off the car",
        "engine stop", "stop the engine", "ignition off",
        "shut down the engine", "turn the car off", "switch off the vehicle",
        "power off the vehicle",
        "gaadi band karo", "car off karo", "engine band karo",
        "ignition off karo", "vehicle stop karo", "car rok do",
        "stop engine please", "power off the car", "vehicle off karo",
        "turn off engine",
    ],
}
