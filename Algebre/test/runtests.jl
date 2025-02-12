using Test
using Algebre  # Charger du module prinpcipale

# Test 1: Vérification de la génération de deux entiers aléatoires dans un intervalle
@testset "Test de génération d'une paire aléatoire" begin
    interval = Interval(-10, 50)
    result = generate_random_pair(interval)
    @test length(result) == 2  # Le tableau doit contenir 2 éléments
    @test result[1] >= interval[1] && result[1] <= interval[2]  # Premier nombre dans l'intervalle
    @test result[2] >= interval[1] && result[2] <= interval[2]  # Deuxième nombre dans l'intervalle
end

# Test 2: Vérification de la génération d'un triplet de Fibonacci
@testset "Test de génération d'un triplet de Fibonacci" begin
    fib_state = Fibonacci(1, 1)
    result1 = next_triplet(fib_state)
    @test result1 == [1, 1, 2]  # Vérifie le premier triplet

    result2 = next_triplet(fib_state)
    @test result2 == [1, 2, 3]  # Vérifie le deuxième triplet

    result3 = next_triplet(fib_state)
    @test result3 == [2, 3, 5]  # Vérifie le troisième triplet
end

#Test 3: Vérification de la génération d'une progression arithmétique
@testset "Test de génération d'une progression arithmétique" begin
    start = 5
    step = 3
    progresseionArithemetique = ArithmeticProgression(start, step)
    n = 4
    result = generate_arithmetic_sequence(progresseionArithemetique, n)
    @test result == [5, 8, 11, 14] # Vérifie que la séquence est correcte
end
