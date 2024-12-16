import sys
from Ghost_Platform import *
from Genetic_Algorithm import *
if __name__=="__main__": 
    best_model = genetic_algorithm(game:=ghost_platform(), input_size:=len(game.get_state()), output_size:=3)
    game.model = best_model
    if game.mode_game["Training AI"]:save_model(game.model, torch.optim.Adam(game.model.parameters(), lr=0.001),game.model_path)
pygame.quit(),sys.exit()