import random
import copy

from ga.chromosome import Chromosome
from ga.fitness import fitness


class GeneticAlgorithm:
    """
    Genetic Algorithm for College Timetable Generation.

    Default population:
        30 chromosomes

    Default generations:
        100

    Uses:
        SubjectAllocation
        Faculty
        Classroom
        Department
        Semester
        Section
        TimeSlot
        FacultyAvailability
    """

    def __init__(
        self,
        faculty,
        subjects,
        classrooms,
        departments,
        timeslots,
        allocations=None,
        availability=None,
        population_size=30,
        generations=100,
        mutation_rate=0.10
    ):

        self.faculty = faculty
        self.subjects = subjects
        self.classrooms = classrooms
        self.departments = departments
        self.timeslots = timeslots

        self.allocations = allocations or []
        self.availability = availability or []

        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    # =========================================================
    # GET TEACHING TIME SLOTS
    # =========================================================

    def get_teaching_slots(self):
        """
        Returns only slots that can contain classes.

        Break and Lunch remain inside the database
        and will later be displayed in the timetable.

        They are simply excluded from GA scheduling.
        """

        teaching_slots = [

            slot

            for slot in self.timeslots

            if str(
                getattr(
                    slot,
                    "session",
                    ""
                )
            ).strip().lower()

            not in [
                "break",
                "lunch"
            ]
        ]

        return teaching_slots

    # =========================================================
    # FACULTY AVAILABILITY
    # =========================================================

    def is_faculty_available(
        self,
        faculty,
        timeslot
    ):
        """
        Checks faculty availability.

        If there is no availability record,
        faculty is assumed to be available.
        """

        faculty_id = getattr(
            faculty,
            "id",
            None
        )

        timeslot_id = getattr(
            timeslot,
            "id",
            None
        )

        for record in self.availability:

            if (
                getattr(
                    record,
                    "faculty_id",
                    None
                )
                == faculty_id

                and

                getattr(
                    record,
                    "timeslot_id",
                    None
                )
                == timeslot_id
            ):

                return getattr(
                    record,
                    "available",
                    True
                )

        return True

    # =========================================================
    # CHOOSE CLASSROOM
    # =========================================================

    def choose_classroom(
        self,
        allocation
    ):
        """
        Select an appropriate classroom.

        Lab subjects:
            Prefer laboratory rooms.

        Theory subjects:
            Prefer normal classrooms.

        Preferred room:
            Used when specified.
        """

        if not self.classrooms:

            return None

        subject_type = str(
            getattr(
                allocation,
                "subject_type",
                "Theory"
            )
        ).strip().lower()

        preferred_room = str(
            getattr(
                allocation,
                "preferred_room",
                ""
            )
        ).strip().lower()

        # -----------------------------------------------------
        # Preferred room
        # -----------------------------------------------------

        if preferred_room:

            matching_rooms = [

                room

                for room in self.classrooms

                if (

                    preferred_room
                    in str(
                        getattr(
                            room,
                            "room_number",
                            ""
                        )
                    ).lower()

                )

                or

                (

                    preferred_room
                    in str(
                        getattr(
                            room,
                            "room_name",
                            ""
                        )
                    ).lower()

                )
            ]

            if matching_rooms:

                return random.choice(
                    matching_rooms
                )

        # -----------------------------------------------------
        # Laboratory
        # -----------------------------------------------------

        if subject_type == "lab":

            lab_rooms = [

                room

                for room in self.classrooms

                if "lab"
                in str(
                    getattr(
                        room,
                        "room_type",
                        ""
                    )
                ).lower()
            ]

            if lab_rooms:

                return random.choice(
                    lab_rooms
                )

        # -----------------------------------------------------
        # Theory classroom
        # -----------------------------------------------------

        theory_rooms = [

            room

            for room in self.classrooms

            if "lab"
            not in str(
                getattr(
                    room,
                    "room_type",
                    ""
                )
            ).lower()
        ]

        if theory_rooms:

            return random.choice(
                theory_rooms
            )

        # -----------------------------------------------------
        # Final fallback
        # -----------------------------------------------------

        return random.choice(
            self.classrooms
        )

    # =========================================================
    # GET TEACHING SLOTS
    # =========================================================

    def get_teaching_slots(self):
        """
        Returns only teaching periods.

        Break and Lunch slots are excluded
        from Genetic Algorithm scheduling.
        """

        if not self.timeslots:
            return []

        teaching_slots = []

        for slot in self.timeslots:

            session = str(
                getattr(
                    slot,
                    "session",
                    ""
                )
            ).strip().lower()

            if session not in (
                "break",
                "lunch"
            ):

                teaching_slots.append(
                    slot
                )

        return teaching_slots

    # =========================================================
    # CREATE LECTURE
    # =========================================================

    def create_lecture(
        self,
        allocation
    ):
        """
        Converts one SubjectAllocation into
        one timetable lecture.
        """

        faculty = allocation.faculty
        subject = allocation.subject
        department = allocation.department
        semester = allocation.semester
        section = allocation.section

        # -----------------------------------------------------
        # Classroom
        # -----------------------------------------------------

        classroom = self.choose_classroom(
            allocation
        )

        if classroom is None:

            return None

        # -----------------------------------------------------
        # Teaching slots only
        # -----------------------------------------------------

        teaching_slots = (
            self.get_teaching_slots()
        )

        if not teaching_slots:

            return None

        # -----------------------------------------------------
        # Select random teaching slot
        # -----------------------------------------------------

        timeslot = random.choice(
            teaching_slots
        )

        # -----------------------------------------------------
        # Faculty availability
        # -----------------------------------------------------

        faculty_available = (
            self.is_faculty_available(
                faculty,
                timeslot
            )
        )

        # -----------------------------------------------------
        # Subject name
        # -----------------------------------------------------

        subject_name = getattr(
            subject,
            "subject_name",
            getattr(
                subject,
                "name",
                str(subject)
            )
        )

        # -----------------------------------------------------
        # Faculty name
        # -----------------------------------------------------

        faculty_name = getattr(
            faculty,
            "faculty_name",
            getattr(
                faculty,
                "name",
                str(faculty)
            )
        )

        # -----------------------------------------------------
        # Department name
        # -----------------------------------------------------

        department_name = getattr(
            department,
            "department_name",
            getattr(
                department,
                "name",
                str(department)
            )
        )

        # -----------------------------------------------------
        # Semester
        # -----------------------------------------------------

        semester_name = getattr(
            semester,
            "semester_name",
            getattr(
                semester,
                "name",
                getattr(
                    semester,
                    "semester",
                    str(semester)
                )
            )
        )

        # -----------------------------------------------------
        # Section
        # -----------------------------------------------------

        section_name = getattr(
            section,
            "section_name",
            getattr(
                section,
                "name",
                str(section)
            )
        )

        # -----------------------------------------------------
        # Create lecture dictionary
        # -----------------------------------------------------

        lecture = {

            "allocation_id":
                allocation.id,

            "department":
                department_name,

            "department_id":
                allocation.department_id,

            "semester":
                semester_name,

            "semester_id":
                allocation.semester_id,

            "section":
                section_name,

            "section_id":
                allocation.section_id,

            "subject":
                subject_name,

            "subject_id":
                allocation.subject_id,

            "faculty":
                faculty_name,

            "faculty_id":
                allocation.faculty_id,

            "room":
                classroom.room_number,

            "room_id":
                classroom.id,

            "room_type":
                classroom.room_type,

            "day":
                timeslot.day,

            "period":
                timeslot.period,

            "timeslot_id":
                timeslot.id,

            "start_time":
                timeslot.start_time,

            "end_time":
                timeslot.end_time,

            "session":
                getattr(
                    timeslot,
                    "session",
                    "Theory"
                ),

            "type":
                allocation.subject_type,

            "required_hours":
                allocation.weekly_hours,

            "consecutive_hours":
                allocation.consecutive_hours,

            "preferred_room":
                allocation.preferred_room,

            "priority":
                allocation.priority,

            "faculty_available":
                faculty_available
        }

        return lecture

    # =========================================================
    # CREATE RANDOM TIMETABLE
    # =========================================================

    def create_random_timetable(
        self
    ):
        """
        Creates one complete random timetable.

        SubjectAllocation determines how many
        lectures each subject requires.
        """

        timetable = []

        for allocation in self.allocations:

            required_hours = max(
                1,
                int(
                    allocation.weekly_hours
                )
            )

            for _ in range(
                required_hours
            ):

                lecture = self.create_lecture(
                    allocation
                )

                if lecture is not None:

                    timetable.append(
                        lecture
                    )

        return timetable

    # =========================================================
    # INITIALIZE POPULATION
    # =========================================================

    def initialize_population(
        self
    ):
        """
        Creates the initial population.

        Default:
            30 chromosomes
        """

        population = []

        for _ in range(
            self.population_size
        ):

            timetable = (
                self.create_random_timetable()
            )

            chromosome = Chromosome(
                timetable
            )

            chromosome.calculate_fitness(
                fitness
            )

            population.append(
                chromosome
            )

        return population

    # =========================================================
    # SELECTION
    # =========================================================

    def selection(
        self,
        population
    ):
        """
        Select strongest chromosomes.

        Top 30% become parents.
        """

        population = sorted(
            population,
            key=lambda chromosome:
                chromosome.fitness,
            reverse=True
        )

        parent_count = max(
            2,
            int(
                self.population_size * 0.30
            )
        )

        return population[
            :parent_count
        ]

    # =========================================================
    # CROSSOVER
    # =========================================================

    def crossover(
        self,
        parent1,
        parent2
    ):
        """
        Combines two parent timetables.
        """

        if not parent1.timetable:

            return Chromosome(
                copy.deepcopy(
                    parent2.timetable
                )
            )

        if not parent2.timetable:

            return Chromosome(
                copy.deepcopy(
                    parent1.timetable
                )
            )

        minimum_length = min(
            len(parent1.timetable),
            len(parent2.timetable)
        )

        if minimum_length < 2:

            return Chromosome(
                copy.deepcopy(
                    parent1.timetable
                )
            )

        split = random.randint(
            1,
            minimum_length - 1
        )

        child_timetable = (

            copy.deepcopy(
                parent1.timetable[
                    :split
                ]
            )

            +

            copy.deepcopy(
                parent2.timetable[
                    split:
                ]
            )
        )

        return Chromosome(
            child_timetable
        )

    # =========================================================
    # MUTATION
    # =========================================================

    def mutation(
        self,
        chromosome
    ):
        """
        Mutation can change:

            - Time slot
            - Classroom

        IMPORTANT:

        Break and Lunch can NEVER
        be selected by mutation.
        """

        teaching_slots = (
            self.get_teaching_slots()
        )

        if not teaching_slots:

            return chromosome

        if not self.classrooms:

            return chromosome

        for lecture in chromosome.timetable:

            # -------------------------------------------------
            # MUTATE TIME SLOT
            # -------------------------------------------------

            if random.random() < self.mutation_rate:

                timeslot = random.choice(
                    teaching_slots
                )

                lecture["day"] = (
                    timeslot.day
                )

                lecture["period"] = (
                    timeslot.period
                )

                lecture["timeslot_id"] = (
                    timeslot.id
                )

                lecture["start_time"] = (
                    timeslot.start_time
                )

                lecture["end_time"] = (
                    timeslot.end_time
                )

                lecture["session"] = getattr(
                    timeslot,
                    "session",
                    "Theory"
                )

                # ---------------------------------------------
                # Recheck faculty availability
                # ---------------------------------------------

                faculty_id = lecture.get(
                    "faculty_id"
                )

                available = True

                for record in self.availability:

                    if (

                        getattr(
                            record,
                            "faculty_id",
                            None
                        )
                        == faculty_id

                        and

                        getattr(
                            record,
                            "timeslot_id",
                            None
                        )
                        == timeslot.id
                    ):

                        available = getattr(
                            record,
                            "available",
                            True
                        )

                        break

                lecture[
                    "faculty_available"
                ] = available

            # -------------------------------------------------
            # MUTATE CLASSROOM
            # -------------------------------------------------

            if random.random() < self.mutation_rate:

                classroom = (
                    self.choose_classroom_from_lecture(
                        lecture
                    )
                )

                if classroom:

                    lecture["room"] = (
                        classroom.room_number
                    )

                    lecture["room_id"] = (
                        classroom.id
                    )

                    lecture["room_type"] = (
                        classroom.room_type
                    )

        chromosome.calculate_fitness(
            fitness
        )

        return chromosome

    # =========================================================
    # CHOOSE CLASSROOM FOR MUTATION
    # =========================================================

    def choose_classroom_from_lecture(
        self,
        lecture
    ):
        """
        Select a classroom appropriate
        for the lecture.
        """

        if not self.classrooms:

            return None

        lecture_type = str(
            lecture.get(
                "type",
                "Theory"
            )
        ).strip().lower()

        preferred_room = str(
            lecture.get(
                "preferred_room",
                ""
            )
        ).strip().lower()

        # -----------------------------------------------------
        # Preferred room
        # -----------------------------------------------------

        if preferred_room:

            matching = [

                room

                for room in self.classrooms

                if (

                    preferred_room
                    in str(
                        getattr(
                            room,
                            "room_number",
                            ""
                        )
                    ).lower()

                )

                or

                (

                    preferred_room
                    in str(
                        getattr(
                            room,
                            "room_name",
                            ""
                        )
                    ).lower()

                )
            ]

            if matching:

                return random.choice(
                    matching
                )

        # -----------------------------------------------------
        # Lab
        # -----------------------------------------------------

        if lecture_type == "lab":

            labs = [

                room

                for room in self.classrooms

                if "lab"
                in str(
                    getattr(
                        room,
                        "room_type",
                        ""
                    )
                ).lower()
            ]

            if labs:

                return random.choice(
                    labs
                )

        # -----------------------------------------------------
        # Theory
        # -----------------------------------------------------

        normal_rooms = [

            room

            for room in self.classrooms

            if "lab"
            not in str(
                getattr(
                    room,
                    "room_type",
                    ""
                )
            ).lower()
        ]

        if normal_rooms:

            return random.choice(
                normal_rooms
            )

        return random.choice(
            self.classrooms
        )

    # =========================================================
    # RUN GENETIC ALGORITHM
    # =========================================================

    def run(
        self
    ):
        """
        Runs the complete Genetic Algorithm.
        """

        print(
            "=========================================="
        )

        print(
            "GENETIC ALGORITHM STARTED"
        )

        print(
            f"Population Size : "
            f"{self.population_size}"
        )

        print(
            f"Generations     : "
            f"{self.generations}"
        )

        print(
            f"Mutation Rate   : "
            f"{self.mutation_rate}"
        )

        print(
            f"Allocations     : "
            f"{len(self.allocations)}"
        )

        print(
            f"Time Slots      : "
            f"{len(self.timeslots)}"
        )

        print(
            f"Teaching Slots  : "
            f"{len(self.get_teaching_slots())}"
        )

        print(
            "=========================================="
        )

        # -----------------------------------------------------
        # INITIAL POPULATION
        # -----------------------------------------------------

        population = (
            self.initialize_population()
        )

        if not population:

            print(
                "ERROR: Population could not be created."
            )

            return None

        best_solution = None

        # -----------------------------------------------------
        # GENERATIONS
        # -----------------------------------------------------

        for generation in range(
            self.generations
        ):

            # -------------------------------------------------
            # Sort population
            # -------------------------------------------------

            population = sorted(
                population,
                key=lambda chromosome:
                    chromosome.fitness,
                reverse=True
            )

            current_best = population[0]

            # -------------------------------------------------
            # Save global best
            # -------------------------------------------------

            if (
                best_solution is None

                or

                current_best.fitness
                > best_solution.fitness
            ):

                best_solution = Chromosome(
                    copy.deepcopy(
                        current_best.timetable
                    )
                )

                best_solution.fitness = (
                    current_best.fitness
                )

            # -------------------------------------------------
            # Display progress
            # -------------------------------------------------

            print(
                f"Generation "
                f"{generation + 1}/"
                f"{self.generations}"
                f" | Best Fitness = "
                f"{current_best.fitness}"
            )

            # -------------------------------------------------
            # Perfect score
            # -------------------------------------------------

            if current_best.fitness >= 1000:

                print(
                    "Perfect timetable found!"
                )

                break

            # -------------------------------------------------
            # Selection
            # -------------------------------------------------

            parents = self.selection(
                population
            )

            if not parents:

                break

            # -------------------------------------------------
            # New population
            # -------------------------------------------------

            new_population = []

            # -------------------------------------------------
            # ELITISM
            # -------------------------------------------------

            elite = Chromosome(
                copy.deepcopy(
                    current_best.timetable
                )
            )

            elite.fitness = (
                current_best.fitness
            )

            new_population.append(
                elite
            )

            # -------------------------------------------------
            # CREATE CHILDREN
            # -------------------------------------------------

            while len(
                new_population
            ) < self.population_size:

                parent1 = random.choice(
                    parents
                )

                parent2 = random.choice(
                    parents
                )

                child = self.crossover(
                    parent1,
                    parent2
                )

                child = self.mutation(
                    child
                )

                child.calculate_fitness(
                    fitness
                )

                new_population.append(
                    child
                )

            population = (
                new_population
            )

        # -----------------------------------------------------
        # FINAL RESULT
        # -----------------------------------------------------

        population = sorted(
            population,
            key=lambda chromosome:
                chromosome.fitness,
            reverse=True
        )

        final_best = population[0]

        if (
            best_solution is not None

            and

            best_solution.fitness
            > final_best.fitness
        ):

            final_best = (
                best_solution
            )

        print(
            "=========================================="
        )

        print(
            "GENETIC ALGORITHM COMPLETED"
        )

        print(
            f"Best Fitness      : "
            f"{final_best.fitness}"
        )

        print(
            f"Timetable Entries : "
            f"{len(final_best.timetable)}"
        )

        print(
            "=========================================="
        )

        return final_best
