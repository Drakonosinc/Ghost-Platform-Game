import random
from Neural_Network import *
# Función de fitness
def fitness_function(model, game):
    game.model = model  # Asigna el modelo al juego antes de ejecutarlo
    score = game.run_with_model()
    return score

# Algoritmo Genético
def initialize_population(size, input_size, output_size):
    population = []
    for _ in range(size):
        model = SimpleNN(input_size, output_size)
        population.append(model)
    return population

def evaluate_population(population, game):
    fitness_scores = []
    for model in population:
        score = fitness_function(model, game)
        fitness_scores.append(score)
    min_score = abs(min(fitness_scores)) if min(fitness_scores) < 0 else 0
    fitness_scores = [score + min_score + 1 for score in fitness_scores]  # Asegúrate de que todos los fitness sean positivos
    return fitness_scores

def select_parents(population, fitness_scores):
    selected = random.choices(population, weights=fitness_scores, k=len(population))
    return selected

def crossover(parent1, parent2):
    child1, child2 = SimpleNN(parent1.fc1.in_features, parent1.fc2.out_features), SimpleNN(parent2.fc1.in_features, parent2.fc2.out_features)
    child1.fc1.weight.data = (parent1.fc1.weight.data + parent2.fc1.weight.data) / 2
    child2.fc1.weight.data = (parent1.fc1.weight.data + parent2.fc1.weight.data) / 2
    return child1, child2

def mutate(model, mutation_rate=0.01):
    with torch.no_grad():
        for param in model.parameters():
            if random.random() < mutation_rate:
                param.add_(torch.randn(param.size()) * 0.1)
    return model

def genetic_algorithm(game, input_size, output_size, generations=100, population_size=20, mutation_rate=0.01):
    population = initialize_population(population_size, input_size, output_size)
    for generation in range(generations):
        game.generation = generation
        fitness_scores = evaluate_population(population, game)
        parents = select_parents(population, fitness_scores)
        next_population = []
        for i in range(0, len(parents), 2):
            parent1, parent2 = parents[i], parents[i + 1]
            child1, child2 = crossover(parent1, parent2)
            next_population.append(mutate(child1, mutation_rate))
            next_population.append(mutate(child2, mutation_rate))
        population = next_population
    best_model = population[fitness_scores.index(max(fitness_scores))]
    game.model = best_model
    return best_model

def save_model(model, optimizer, path):
    print("save model")
    torch.save({
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, path)

def load_model(path, input_size, output_size, optimizer=None):
    try:
        print("load model")
        model = SimpleNN(input_size, output_size)
        checkpoint = torch.load(path)
        model.load_state_dict(checkpoint['model_state_dict'])
        if optimizer:
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return model
    except FileNotFoundError:
        print(f"The file {path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None