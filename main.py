import os

from create_playlist import create_playlist
from script import scrape
from train import train

if __name__ == "__main__":
    search_term = input("Enter Search Term")
    os.remove("audio_feat.csv")

    print("Searching spotify")
    scrape("random music")
    scrape(search_term)

    print("Training model")
    train()

    print("Creating your playlist")
    create_playlist(search_term)
