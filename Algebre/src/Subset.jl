module Subset

export ArithmeticProgression, generate_random_pair, generate_arithmetic_sequence, next_triplet, Interval, Fibonacci, get_next

# Structure abstraite pour représenter une famille d'intervalles et séquences
abstract type Algebra end

# Interface d'itération par défaut
Base.iterate(i::Algebra, state = 1) = (get_next(i), state + 1)
Base.length(i::Algebra) = 1

# Structure pour représenter un Intervalle
struct Interval <: Algebra
    bar
    low::Int
    high::Int 
end

Base.getindex(i::Interval, n::Int) = getindex(i, Val(n))
Base.getindex(i::Interval, ::Val{1}) = i.low
Base.getindex(i::Interval, ::Val{2}) = i.high

"""
Génère un tableau de 2 entiers aléatoires dans l'intervalle donné par `interval`.
"""
function generate_random_pair(interval::Interval)
    if interval.low > interval.high
        throw(ArgumentError("La borne inférieure doit être ≤ à la borne supérieure"))
    end
    return [rand(interval.low:interval.high), rand(interval.low:interval.high)]
end

# Structure pour représenter une Progression Arithmétique
mutable struct ArithmeticProgression <: Algebra
    bar
    start::Int
    step::Int   
end

Base.getindex(p::ArithmeticProgression, n::Int) = getindex(p, Val(n))
Base.getindex(p::ArithmeticProgression, ::Val{1}) = p.start
Base.getindex(p::ArithmeticProgression, ::Val{2}) = p.step

"""
Génère une séquence arithmétique de longueur `n`, à partir de la progression `prog`.
"""
function generate_arithmetic_sequence(prog::ArithmeticProgression, n::Int)
    return [prog.start + i * prog.step for i in 0:(n - 1)]
end

"""
Retourne l'élément suivant de la progression arithmétique et met à jour `prog`.
"""
function get_next(prog::ArithmeticProgression)
    next_val = prog.start
    prog.start += prog.step
    return next_val
end

Base.iterate(prog::ArithmeticProgression, state = 1) = (get_next(prog), state + 1)

# Structure pour représenter une séquence de Fibonacci
mutable struct Fibonacci <: Algebra
    bar
    prev::Int
    current::Int
end

"""
Retourne le prochain nombre de la séquence de Fibonacci.
"""
function get_next(fib::Fibonacci)
    next_val = fib.current
    fib.prev, fib.current = fib.current, fib.prev + fib.current
    return next_val
end

Base.iterate(fib::Fibonacci, state = 1) = (get_next(fib), state + 1)

"""
Génère un triplet consécutif de la séquence de Fibonacci.
"""
function next_triplet(fib::Fibonacci)
    a, b, c = fib.prev, fib.current, fib.prev + fib.current
    fib.prev, fib.current = b, c
    return [a, b, c]
end

end  # module
