import os
import platform


def play_chord(*nums):
    # Skip playing sounds on Windows since 'play' command isn't available
    if platform.system() == "Windows":
        print("Debug - Skipping sound on Windows platform")
        return
        
    commands = [
        "play",
        "-n",
        "-c1",
        "--no-show-progress",
        "synth",
    ] + [
        "sin %-" + str(num)
        for num in nums
    ] + [
        "fade h 0.5 1 0.5",
        "> /dev/null"
    ]
    try:
        print(f"Debug - Attempting to play sound: {' '.join(commands)}")
        os.system(" ".join(commands))
    except Exception as e:
        print(f"Debug - Error playing sound: {e}")


def play_error_sound():
    play_chord(11, 8, 6, 1)


def play_finish_sound():
    play_chord(12, 9, 5, 2)
