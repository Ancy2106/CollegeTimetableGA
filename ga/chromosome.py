import random


class Chromosome:
    """
    Represents one possible timetable solution.

    A chromosome contains a list of timetable entries.

    Each timetable entry represents:

        {
            "allocation": allocation object,
            "timeslot": timeslot object,
            "classroom": classroom object
        }

    The Genetic Algorithm creates many Chromosomes
    and evaluates them using the fitness function.
    """

    def __init__(self, timetable=None):

        if timetable is None:
            self.timetable = []

        else:
            self.timetable = timetable

        # Fitness score of this chromosome
        self.fitness = 0

    # ---------------------------------------------------------
    # CALCULATE FITNESS
    # ---------------------------------------------------------

    def calculate_fitness(self, fitness_function):

        self.fitness = fitness_function(
            self.timetable
        )

        return self.fitness

    # ---------------------------------------------------------
    # CREATE RANDOM COPY
    # ---------------------------------------------------------

    def copy(self):

        return Chromosome(
            timetable=self.timetable.copy()
        )

    # ---------------------------------------------------------
    # MUTATION
    # ---------------------------------------------------------

    def mutate(self, timeslots, classrooms, mutation_rate=0.05):
        """
        Randomly changes the timeslot or classroom
        of timetable entries.

        The fitness function will later determine
        whether the mutation creates constraint violations.
        """

        if not timeslots or not classrooms:
            return

        for entry in self.timetable:

            if random.random() < mutation_rate:

                entry["timeslot"] = random.choice(
                    timeslots
                )

            if random.random() < mutation_rate:

                entry["classroom"] = random.choice(
                    classrooms
                )

    # ---------------------------------------------------------
    # CROSSOVER
    # ---------------------------------------------------------

    def crossover(self, other):

        if not self.timetable:

            return Chromosome([])

        if not other.timetable:

            return Chromosome(
                self.timetable.copy()
            )

        point = random.randint(
            1,
            min(
                len(self.timetable),
                len(other.timetable)
            ) - 1
        )

        child_timetable = (

            self.timetable[:point]

            +

            other.timetable[point:]
        )

        return Chromosome(
            child_timetable
        )

    # ---------------------------------------------------------
    # STRING REPRESENTATION
    # ---------------------------------------------------------

    def __repr__(self):

        return (
            f"Chromosome("
            f"entries={len(self.timetable)}, "
            f"fitness={self.fitness})"
        )
