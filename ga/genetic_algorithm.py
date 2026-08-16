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

        # Database Data
        self.faculty = faculty
        self.subjects = subjects
        self.classrooms = classrooms
        self.departments = departments
        self.timeslots = timeslots

        self.allocations = allocations or []
        self.availability = availability or []

    # GA Parameters
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    # ---------------------------------------------------
    # Teaching Slots
    # (Break/Lunch removed automatically)
    # ---------------------------------------------------

        self.teaching_slots = [

            slot

            for slot in self.timeslots

            if str(
                getattr(slot, "session", "")
            ).strip().lower()

            not in [
                "break",
                "lunch"
            ]
        ]

    # ---------------------------------------------------
    # Track Used Slots
    # Prevents duplicate slot assignment
    # ---------------------------------------------------

        self.used_slots = {}

    # Format:
    # {
    #   ("CSE",7,"A"): {
    #       ("Monday",1),
    #       ("Monday",2)
    #   }
    # }

    # ---------------------------------------------------
    # Faculty Busy Slots
    # ---------------------------------------------------

        self.faculty_schedule = {}

    # ---------------------------------------------------
    # Classroom Busy Slots
    # ---------------------------------------------------

        self.room_schedule = {}

    # ---------------------------------------------------
    # Random Seed
    # Gives different timetable every generation
    # ---------------------------------------------------

        random.seed()

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
        slot
    ):

        # If no availability restrictions exist,
        # faculty is considered available

        if not self.availability:

            return True

        for availability in self.availability:

            if (
                availability.faculty_id == faculty.id
                and
                availability.timeslot_id == slot.id
            ):

                return True

        return False

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
    # CREATE RANDOM TIMETABLE
    # =========================================================

    def create_random_timetable(self):
        """
        Create a complete timetable.

        HARD CONSTRAINTS:

        1. Labs are scheduled before theory.
        2. A lab must occupy its complete consecutive block.
        3. Lab periods must be truly consecutive.
        4. No faculty clash.
        5. No classroom clash.
        6. No section clash.
        7. Only ONE LAB BLOCK per section per day.
        8. Every allocation must receive exactly weekly_hours.
        """

        import random

        timetable = []

        # =====================================================
        # RESET TRACKING
        # =====================================================

        self.used_slots = {}

        self.faculty_schedule = {}

        self.room_schedule = {}

        # =====================================================
        # NEW: TRACK LAB DAYS
        #
        # Example:
        #
        # {
        #     ("CSE", 7, "A", "Friday"): True
        # }
        # =====================================================

        self.lab_day_schedule = set()

        # =====================================================
        # SEPARATE LABS AND THEORY
        # =====================================================

        lab_allocations = []
        theory_allocations = []

        for allocation in self.allocations:

            consecutive_hours = max(
                1,
                int(
                    getattr(
                        allocation,
                        "consecutive_hours",
                        1
                    )
                )
            )

            if consecutive_hours > 1:

                lab_allocations.append(
                    allocation
                )

            else:

                theory_allocations.append(
                    allocation
                )

        # =====================================================
        # RANDOMIZE
        # =====================================================

        random.shuffle(
            lab_allocations
        )

        random.shuffle(
            theory_allocations
        )

        # =====================================================
        # 1. GENERATE LABS FIRST
        # =====================================================

        for allocation in lab_allocations:

            weekly_hours = max(
                1,
                int(
                    allocation.weekly_hours
                )
            )

            consecutive_hours = max(
                2,
                int(
                    getattr(
                        allocation,
                        "consecutive_hours",
                        2
                    )
                )
            )

            lectures_created = 0

            attempts = 0

            # Number of complete lab blocks required
            required_blocks = (
                weekly_hours //
                consecutive_hours
            )

            blocks_created = 0

            # =================================================
            # CREATE COMPLETE LAB BLOCKS
            # =================================================

            while (

                blocks_created < required_blocks

                and

                attempts < 500

            ):

                lectures = self.create_consecutive_lectures(
                    allocation,
                    consecutive_hours
                )

                # ---------------------------------------------
                # ACCEPT ONLY COMPLETE BLOCK
                # ---------------------------------------------

                if (

                    lectures

                    and

                    len(lectures)
                    == consecutive_hours

                ):

                    day = lectures[0]["day"]

                    # -----------------------------------------
                    # BUILD UNIQUE SECTION KEY
                    # -----------------------------------------

                    section_key = (
                        allocation.department_id,
                        allocation.semester,
                        allocation.section,
                        day
                    )

                    # -----------------------------------------
                    # HARD CONSTRAINT:
                    #
                    # ONLY ONE LAB BLOCK
                    # FOR ONE SECTION
                    # ON ONE DAY
                    # -----------------------------------------

                    if section_key in self.lab_day_schedule:

                        # Undo the temporary reservation
                        # created by create_consecutive_lectures

                        for lecture in lectures:

                            self.unregister_lecture(
                                lecture
                            )

                        attempts += 1

                        continue

                    # -----------------------------------------
                    # ACCEPT LAB BLOCK
                    # -----------------------------------------

                    self.lab_day_schedule.add(
                        section_key
                    )

                    timetable.extend(
                        lectures
                    )

                    lectures_created += (
                        consecutive_hours
                    )

                    blocks_created += 1

                attempts += 1

            # =================================================
            # HARD VALIDATION
            # =================================================

            if lectures_created != weekly_hours:

                return None

        # =====================================================
        # 2. GENERATE THEORY CLASSES
        # =====================================================

        for allocation in theory_allocations:

            weekly_hours = max(
                1,
                int(
                    allocation.weekly_hours
                )
            )

            lectures_created = 0

            attempts = 0

            while (

                lectures_created < weekly_hours

                and

                attempts < 500

            ):

                lectures = self.create_lecture(
                    allocation
                )

                if lectures:

                    timetable.extend(
                        lectures
                    )

                    lectures_created += len(
                        lectures
                    )

                attempts += 1

            # =================================================
            # HARD VALIDATION
            # =================================================

            if lectures_created != weekly_hours:

                return None

        # =====================================================
        # FINAL HARD CONSTRAINT VALIDATION
        # =====================================================

        if not self.validate_complete_timetable(
            timetable
        ):

            return None

        # =====================================================
        # FINAL CHECK:
        # ONLY ONE LAB SET PER DAY PER SECTION
        # =====================================================

        labs_per_day = {}

        for lecture in timetable:

            if lecture.get(
                "consecutive_hours",
                1
            ) > 1:

                key = (

                    lecture.get(
                        "department_id"
                    ),

                    lecture.get(
                        "semester"
                    ),

                    lecture.get(
                        "section"
                    ),

                    lecture.get(
                        "day"
                    )
                )

                allocation_id = lecture.get(
                    "allocation_id"
                )

                if key not in labs_per_day:

                    labs_per_day[key] = (
                        allocation_id
                    )

                elif (

                    labs_per_day[key]
                    != allocation_id

                ):

                    # Two different labs
                    # on the same day

                    return None

        random.shuffle(
            timetable
        )

        return timetable

   # =========================================================
   # CREATE LECTURE
   # =========================================================

    def create_lecture(
        self,
        allocation
    ):
        """
        Create exactly one complete class block.

        Theory:
            consecutive_hours = 1

        Lab:
            consecutive_hours = 2 or more

        Returns:
            List of lecture dictionaries
        """

        import random

        faculty = allocation.faculty
        subject = allocation.subject
        department = allocation.department
        semester = allocation.semester
        section = allocation.section

        # ==========================================
        # GET REQUIRED CONSECUTIVE HOURS
        # ==========================================

        consecutive_hours = max(
            1,
            int(
                getattr(
                    allocation,
                    "consecutive_hours",
                    1
                ) or 1
            )
        )

        # ==========================================
        # CHOOSE VALID CLASSROOM
        # ==========================================

        classroom = self.choose_classroom(
            allocation
        )

        if classroom is None:

            return []

        # ==========================================
        # CREATE CLASS IDENTIFIER
        # ==========================================

        class_key = (
            allocation.department_id,
            allocation.semester_id,
            allocation.section_id
        )

        if class_key not in self.used_slots:

            self.used_slots[class_key] = set()

        # ==========================================
        # GROUP TEACHING SLOTS BY DAY
        # ==========================================

        slots_by_day = {}

        for slot in self.teaching_slots:

            if slot.day not in slots_by_day:

                slots_by_day[slot.day] = []

            slots_by_day[slot.day].append(
                slot
            )

        # Sort slots by period
        for day in slots_by_day:

            slots_by_day[day].sort(
                key=lambda slot: slot.period
            )

        # Randomize days
        days = list(slots_by_day.keys())

        random.shuffle(days)

        # ==========================================
        # FIND VALID COMPLETE BLOCK
        # ==========================================

        selected_slots = None

        for day in days:

            day_slots = slots_by_day[day]

            # Every possible starting position
            for start in range(
                len(day_slots)
                - consecutive_hours
                + 1
            ):

                candidate_slots = day_slots[
                    start:
                    start + consecutive_hours
                ]

                # ======================================
                # CHECK PERIODS ARE TRULY CONSECUTIVE
                # ======================================

                periods_valid = True

                for index in range(
                    len(candidate_slots) - 1
                ):

                    current_slot = candidate_slots[index]

                    next_slot = candidate_slots[
                        index + 1
                    ]

                    # ======================================
                    # PERIOD NUMBER MUST BE CONSECUTIVE
                    # ======================================

                    if (
                        next_slot.period
                        != current_slot.period + 1
                    ):

                        periods_valid = False
                        break

                    # ======================================
                    # TIME MUST ALSO BE CONTINUOUS
                    # A lab cannot cross BREAK or LUNCH
                    # ======================================

                    current_end = (
                        current_slot.end_time
                    )

                    next_start = (
                        next_slot.start_time
                    )

                    if str(current_end) != str(next_start):

                        periods_valid = False
                        break

                if not periods_valid:

                    continue

                # ======================================
                # CHECK ALL SLOTS BEFORE RESERVING
                # ======================================

                block_valid = True

                for slot in candidate_slots:

                    slot_key = (
                        slot.day,
                        slot.period
                    )

                    # ------------------------------
                    # CLASS / SECTION CLASH
                    # ------------------------------

                    if (
                        slot_key
                        in self.used_slots[class_key]
                    ):

                        block_valid = False
                        break

                    # ------------------------------
                    # FACULTY CLASH
                    # ------------------------------

                    faculty_key = (
                        allocation.faculty_id,
                        slot.day,
                        slot.period
                    )

                    if (
                        faculty_key
                        in self.faculty_schedule
                    ):

                        block_valid = False
                        break

                    # ------------------------------
                    # ROOM CLASH
                    # ------------------------------

                    room_key = (
                        classroom.id,
                        slot.day,
                        slot.period
                    )

                    if (
                        room_key
                        in self.room_schedule
                    ):

                        block_valid = False
                        break

                    # ------------------------------
                    # FACULTY AVAILABILITY
                    # ------------------------------

                    if not self.is_faculty_available(
                        faculty,
                        slot
                    ):

                        block_valid = False
                        break

                # ======================================
                # COMPLETE BLOCK FOUND
                # ======================================

                if block_valid:

                    selected_slots = candidate_slots

                    break

            if selected_slots:

                break

        # ==========================================
        # NO VALID BLOCK
        # ==========================================

        if selected_slots is None:

            return []

        # ==========================================
        # RESERVE ALL SLOTS
        # Only after entire block is validated
        # ==========================================

        for slot in selected_slots:

            slot_key = (
                slot.day,
                slot.period
            )

            self.used_slots[class_key].add(
                slot_key
            )

            faculty_key = (
                allocation.faculty_id,
                slot.day,
                slot.period
            )

            self.faculty_schedule[
                faculty_key
            ] = True

            room_key = (
                classroom.id,
                slot.day,
                slot.period
            )

            self.room_schedule[
                room_key
            ] = True

        # ==========================================
        # GET DISPLAY NAMES
        # ==========================================

        subject_name = getattr(
            subject,
            "subject_name",
            getattr(
                subject,
                "name",
                ""
            )
        )

        faculty_name = getattr(
            faculty,
            "faculty_name",
            getattr(
                faculty,
                "name",
                ""
            )
        )

        department_name = getattr(
            department,
            "department_name",
            getattr(
                department,
                "name",
                ""
            )
        )

        semester_value = getattr(
            semester,
            "semester",
            getattr(
                semester,
                "semester_name",
                ""
            )
        )

        section_name = getattr(
            section,
            "section_name",
            getattr(
                section,
                "name",
                ""
            )
        )

        # ==========================================
        # CREATE LECTURE RECORDS
        # ==========================================

        lectures = []

        for slot in selected_slots:

            lecture = {

                "allocation_id":
                    allocation.id,

                "department":
                    department_name,

                "department_id":
                    allocation.department_id,

                "semester":
                    semester_value,

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
                    slot.day,

                "period":
                    slot.period,

                "timeslot_id":
                    slot.id,

                "start_time":
                    slot.start_time,

                "end_time":
                    slot.end_time,

                "session":
                    slot.session,

                "type":
                    allocation.subject_type,

                "subject_type":
                    allocation.subject_type,

                "required_hours":
                    allocation.weekly_hours,

                "consecutive_hours":
                    consecutive_hours,

                "preferred_room":
                    allocation.preferred_room,

                "priority":
                    allocation.priority,

                "faculty_available":
                    True
            }

            lectures.append(lecture)

        # Must return the COMPLETE block
        return lectures

    def build_lecture(self, allocation, slot):

        # ==========================================
        # FIND AN AVAILABLE ROOM
        # ==========================================

        room_id = None

        for classroom in self.classrooms:

            if self.is_room_available(
                classroom.id,
                slot
            ):

                room_id = classroom.id

                break

        # No room available
        if room_id is None:

            return None

        # ==========================================
        # SAFE ALLOCATION VALUES
        # ==========================================

        allocation_id = getattr(
            allocation,
            "id",
            None
        )

        subject_id = getattr(
            allocation,
            "subject_id",
            None
        )

        faculty_id = getattr(
            allocation,
            "faculty_id",
            None
        )

        department_id = getattr(
            allocation,
            "department_id",
            None
        )

        semester = getattr(
            allocation,
            "semester",
            None
        )

        section = getattr(
            allocation,
            "section",
            None
        )

        # ==========================================
        # BUILD LECTURE
        # ==========================================

        lecture = {

            # IDs
            "allocation_id": allocation_id,

            "subject_id": subject_id,

            "faculty_id": faculty_id,

            "room_id": room_id,

            "classroom_id": room_id,

            "timeslot_id": slot.id,

            # Department
            "department_id": department_id,

            "department": department_id,

            # Class information
            "semester": semester,

            "section": section,

            # Time information
            "day": slot.day,

            "period": slot.period,

            # Class type
            "lecture_type": getattr(
                allocation,
                "lecture_type",
                getattr(
                    allocation,
                    "class_type",
                    None
                )
            )
        }

        return lecture

    def is_room_available(
        self,
        room_id,
        slot
    ):

        slot_key = (
            slot.day,
            slot.period
        )

        # Check whether room is already occupied
        if slot_key in self.room_schedule:

            if room_id in self.room_schedule[slot_key]:

                return False

        return True

    def is_slot_available(
        self,
        allocation,
        slot
    ):
        """
        Check all hard constraints before placing a lecture.

        Returns True only when:
        - Slot is not already used by the same section
        - Faculty has no clash
        - Faculty is available
        - A classroom is available
        """

        # ==========================================
        # GET SLOT IDENTIFIERS
        # ==========================================

        slot_id = slot.id

        day = slot.day

        # ==========================================
        # GET ALLOCATION INFORMATION
        # ==========================================

        faculty_id = getattr(
            allocation,
            "faculty_id",
            None
        )

        department_id = getattr(
            allocation,
            "department_id",
            None
        )

        semester = getattr(
            allocation,
            "semester",
            None
        )

        section = getattr(
            allocation,
            "section",
            None
        )

        # ==========================================
        # 1. CHECK SECTION CLASH
        # ==========================================

        section_key = (
            department_id,
            semester,
            section,
            slot_id
        )

        if section_key in self.used_slots:

            return False

        # ==========================================
        # 2. CHECK FACULTY CLASH
        # ==========================================

        if faculty_id is not None:

            faculty_key = (
                faculty_id,
                slot_id
            )

            if faculty_key in self.faculty_schedule:

                return False

        # ==========================================
        # 3. CHECK FACULTY AVAILABILITY
        # ==========================================

        if hasattr(
            self,
            "faculty_availability"
        ):

            availability = self.faculty_availability

            if faculty_id is not None:

                # Try common availability formats
                faculty_slots = availability.get(
                    faculty_id
                )

                if faculty_slots is not None:

                    if isinstance(
                        faculty_slots,
                        (list, set, tuple)
                    ):

                        if slot_id not in faculty_slots:

                            return False

        # ==========================================
        # SLOT IS AVAILABLE
        # ==========================================

        return True

    def register_lecture(self, lecture):

        slot_key = (
            lecture["day"],
            lecture["period"]
        )

        faculty_id = lecture["faculty_id"]

        room_id = lecture["room_id"]

        allocation_id = lecture["allocation_id"]

        # ---------------------------------------------
        # USED SLOT
        # ---------------------------------------------

        if allocation_id not in self.used_slots:

            self.used_slots[allocation_id] = []

        self.used_slots[allocation_id].append(
            slot_key
        )

        # ---------------------------------------------
        # FACULTY SCHEDULE
        # ---------------------------------------------

        if faculty_id not in self.faculty_schedule:

            self.faculty_schedule[faculty_id] = set()

        self.faculty_schedule[faculty_id].add(
            slot_key
        )

        # ---------------------------------------------
        # ROOM SCHEDULE
        # ---------------------------------------------

        if slot_key not in self.room_schedule:

            self.room_schedule[slot_key] = set()

        self.room_schedule[slot_key].add(
            room_id
        )
    # =========================================================
    # CREATE CONSECUTIVE LECTURES
    # =========================================================

    def create_consecutive_lectures(
        self,
        allocation,
        consecutive_hours
    ):
        """
        Create exactly one complete consecutive lab block.

        Hard constraints:
        - Same day
        - Consecutive period numbers
        - Actual time continuity
        - Cannot cross break/lunch
        - Faculty must be available
        - Section cannot have another class
        - Room cannot clash
        - Entire block must be valid before registering
        """

        import random
        from datetime import datetime

        # ==========================================
        # GET TEACHING SLOTS
        # ==========================================

        teaching_slots = list(self.teaching_slots)

        # ==========================================
        # GROUP BY DAY
        # ==========================================

        slots_by_day = {}

        for slot in teaching_slots:

            day = slot.day

            if day not in slots_by_day:
                slots_by_day[day] = []

            slots_by_day[day].append(slot)

        possible_blocks = []

        # ==========================================
        # FIND VALID CONSECUTIVE BLOCKS
        # ==========================================

        for day, slots in slots_by_day.items():

            slots.sort(
                key=lambda x: x.period
            )

            for start_index in range(len(slots)):

                block = slots[
                    start_index:
                    start_index + consecutive_hours
                ]

                # Must have complete block
                if len(block) != consecutive_hours:
                    continue

                block_valid = True

                # ======================================
                # CHECK PERIOD + TIME CONTINUITY
                # ======================================

                for i in range(len(block) - 1):

                    current_slot = block[i]
                    next_slot = block[i + 1]

                    # Same day
                    if current_slot.day != next_slot.day:
                        block_valid = False
                        break

                    # Consecutive periods
                    if (
                        next_slot.period
                        != current_slot.period + 1
                    ):
                        block_valid = False
                        break

                    # Actual time continuity
                    current_end = str(
                        current_slot.end_time
                    ).strip()

                    next_start = str(
                        next_slot.start_time
                    ).strip()

                    if current_end != next_start:
                        block_valid = False
                        break

                if not block_valid:
                    continue

                possible_blocks.append(block)

        # ==========================================
        # RANDOMIZE POSSIBLE BLOCKS
        # ==========================================

        random.shuffle(possible_blocks)

        # ==========================================
        # TRY EACH BLOCK
        # ==========================================

        for block in possible_blocks:

            # --------------------------------------
            # FIRST: CHECK ENTIRE BLOCK
            # --------------------------------------

            block_valid = True

            for slot in block:

                if not self.is_slot_available(
                    allocation,
                    slot
                ):
                    block_valid = False
                    break

            if not block_valid:
                continue

            # --------------------------------------
            # BUILD ENTIRE BLOCK
            # --------------------------------------

            lectures = []

            for slot in block:

                lecture = self.build_lecture(
                    allocation,
                    slot
                )

                if lecture is None:

                    block_valid = False
                    break

                lectures.append(lecture)

            # --------------------------------------
            # REGISTER ONLY COMPLETE BLOCK
            # --------------------------------------

            if (
                block_valid
                and len(lectures) == consecutive_hours
            ):

                for lecture in lectures:

                    self.register_lecture(
                        lecture
                    )

                return lectures

        # ==========================================
        # NO VALID BLOCK FOUND
        # ==========================================

        return []

    def validate_complete_timetable(self, timetable):

        from collections import defaultdict

        allocation_count = defaultdict(int)

        # ==========================================
        # COUNT LECTURES FOR EACH ALLOCATION
        # ==========================================

        for lecture in timetable:

            allocation_id = lecture.get(
                "allocation_id"
            )

            if allocation_id is not None:

                allocation_count[
                    allocation_id
                ] += 1

        # ==========================================
        # CHECK REQUIRED WEEKLY HOURS
        # ==========================================

        for allocation in self.allocations:

            required_hours = max(
                1,
                int(
                    allocation.weekly_hours
                )
            )

            actual_hours = allocation_count.get(
                allocation.id,
                0
            )

            if actual_hours != required_hours:

                return False

        # ==========================================
        # CHECK FOR SLOT CONFLICTS
        # ==========================================

        used_section_slots = set()

        used_faculty_slots = set()

        used_room_slots = set()

        for lecture in timetable:

            day = lecture.get("day")

            period = lecture.get("period")

            allocation_id = lecture.get(
                "allocation_id"
            )

            faculty_id = lecture.get(
                "faculty_id"
            )

            classroom_id = lecture.get(
                "classroom_id"
            )

            section_key = (
                allocation_id,
                day,
                period
            )

            faculty_key = (
                faculty_id,
                day,
                period
            )

            room_key = (
                classroom_id,
                day,
                period
            )

            # Section conflict

            if section_key in used_section_slots:

                return False

            used_section_slots.add(
                section_key
            )

            # Faculty conflict

            if faculty_id is not None:

                if faculty_key in used_faculty_slots:

                    return False

                used_faculty_slots.add(
                    faculty_key
                )

            # Room conflict

            if classroom_id is not None:

                if room_key in used_room_slots:

                    return False

                used_room_slots.add(
                    room_key
                )

        return True

    def unregister_lecture(self, lecture):

        day = lecture.get("day")

        period = lecture.get("period")

        faculty_id = lecture.get(
            "faculty_id"
        )

        classroom_id = lecture.get(
            "classroom_id"
        )

        department_id = lecture.get(
            "department_id"
        )

        semester = lecture.get(
            "semester"
        )

        section = lecture.get(
            "section"
        )

        # =================================================
        # REMOVE SECTION OCCUPANCY
        # =================================================

        section_key = (
            department_id,
            semester,
            section,
            day,
            period
        )

        if section_key in self.used_slots:

            del self.used_slots[
                section_key
            ]

        # =================================================
        # REMOVE FACULTY OCCUPANCY
        # =================================================

        faculty_key = (
            faculty_id,
            day,
            period
        )

        if faculty_key in self.faculty_schedule:

            del self.faculty_schedule[
                faculty_key
            ]

        # =================================================
        # REMOVE ROOM OCCUPANCY
        # =================================================

        room_key = (
            classroom_id,
            day,
            period
        )

        if room_key in self.room_schedule:

            del self.room_schedule[
                room_key
            ]
    # =========================================================
    # INITIALIZE POPULATION
    # =========================================================

    def initialize_population(self):

        population = []

        attempts = 0

        max_attempts = self.population_size * 20

        while (
            len(population) < self.population_size
            and attempts < max_attempts
        ):

            timetable = self.create_random_timetable()

            # Reject incomplete timetable
            if not timetable:

                attempts += 1
                continue

            chromosome = Chromosome(
                timetable
            )

            chromosome.calculate_fitness(
                fitness
            )

            population.append(
                chromosome
            )

            attempts += 1

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
        Improved mutation.

        Mutates:
            • Time Slot
            • Classroom

        Prevents:
            • Faculty clashes
            • Room clashes
            • Class clashes
            • Break/Lunch assignment
        """

        if not chromosome.timetable:
            return chromosome

        teaching_slots = self.get_teaching_slots()

        if not teaching_slots:
            return chromosome

        for lecture in chromosome.timetable:

            # ---------------------------------------------
            # TIME SLOT MUTATION
            # ---------------------------------------------

            if random.random() < self.mutation_rate:

                shuffled_slots = teaching_slots.copy()
                random.shuffle(shuffled_slots)

                for slot in shuffled_slots:

                    class_key = (
                        lecture["department"],
                        lecture["semester"],
                        lecture["section"]
                    )

                    slot_key = (
                        slot.day,
                        slot.period
                    )

                    # -------------------------
                    # Class Clash
                    # -------------------------

                    clash = False

                    for other in chromosome.timetable:

                        if other == lecture:
                            continue

                        if (
                            other["department"] == lecture["department"]
                            and
                            other["semester"] == lecture["semester"]
                            and
                            other["section"] == lecture["section"]
                            and
                            other["day"] == slot.day
                            and
                            other["period"] == slot.period
                        ):
                            clash = True
                            break

                    if clash:
                        continue

                    # -------------------------
                    # Faculty Clash
                    # -------------------------

                    clash = False

                    for other in chromosome.timetable:

                        if other == lecture:
                            continue

                        if (
                            other["faculty_id"] == lecture["faculty_id"]
                            and
                            other["day"] == slot.day
                            and
                            other["period"] == slot.period
                        ):
                            clash = True
                            break

                    if clash:
                        continue

                    # -------------------------
                    # Room Clash
                    # -------------------------

                    clash = False

                    for other in chromosome.timetable:

                        if other == lecture:
                            continue

                        if (
                            other["room_id"] == lecture["room_id"]
                            and
                            other["day"] == slot.day
                            and
                            other["period"] == slot.period
                        ):
                            clash = True
                            break

                    if clash:
                        continue

                    # -------------------------
                    # Faculty Availability
                    # -------------------------

                    faculty_obj = next(

                        (
                            f for f in self.faculty
                            if f.id == lecture["faculty_id"]
                        ),

                        None

                    )

                    if faculty_obj:

                        if not self.is_faculty_available(
                            faculty_obj,
                            slot
                        ):
                            continue

                    # -------------------------
                    # Apply Mutation
                    # -------------------------

                    lecture["day"] = slot.day

                    lecture["period"] = slot.period

                    lecture["timeslot_id"] = slot.id

                    lecture["start_time"] = slot.start_time

                    lecture["end_time"] = slot.end_time

                    lecture["session"] = slot.session

                    break

            # ---------------------------------------------
            # CLASSROOM MUTATION
            # ---------------------------------------------

            if random.random() < self.mutation_rate:

                room = self.choose_classroom_from_lecture(
                    lecture
                )

                if room:

                    room_busy = False

                    for other in chromosome.timetable:

                        if other == lecture:
                            continue

                        if (
                            other["room_id"] == room.id
                            and
                            other["day"] == lecture["day"]
                            and
                            other["period"] == lecture["period"]
                        ):
                            room_busy = True
                            break

                    if not room_busy:

                        lecture["room"] = room.room_number

                        lecture["room_id"] = room.id

                        lecture["room_type"] = room.room_type

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

    def calculate_fitness(
        self,
        timetable
    ):
        """
        Calculate timetable fitness.

        Higher score = better timetable.

        Hard constraint violations receive
        very large penalties.
        """

        if not timetable:
            return -1000000

        fitness = 1000

        # ==========================================
        # TRACK OCCUPIED RESOURCES
        # ==========================================

        section_slots = {}

        faculty_slots = {}

        room_slots = {}

        # ==========================================
        # CHECK EACH LECTURE
        # ==========================================

        for lecture in timetable:

            try:

                day = lecture.get(
                    "day"
                )

                period = lecture.get(
                    "period"
                )

                department = lecture.get(
                    "department"
                )

                semester = lecture.get(
                    "semester"
                )

                section = lecture.get(
                    "section"
                )

                faculty = lecture.get(
                    "faculty"
                )

                room = lecture.get(
                    "room"
                )

                allocation_id = lecture.get(
                    "allocation_id"
                )

            except AttributeError:

                # Invalid lecture structure
                return -1000000

            # ======================================
            # SECTION CLASH
            # ======================================

            section_key = (
                department,
                semester,
                section,
                day,
                period
            )

            if section_key in section_slots:

                fitness -= 10000

            else:

                section_slots[section_key] = True

            # ======================================
            # FACULTY CLASH
            # ======================================

            faculty_key = (
                faculty,
                day,
                period
            )

            if faculty_key in faculty_slots:

                fitness -= 10000

            else:

                faculty_slots[faculty_key] = True

            # ======================================
            # ROOM CLASH
            # ======================================

            room_key = (
                room,
                day,
                period
            )

            if room_key in room_slots:

                fitness -= 10000

            else:

                room_slots[room_key] = True

        # ==========================================
        # CHECK REQUIRED HOURS
        # ==========================================

        allocation_counts = {}

        for lecture in timetable:

            allocation_id = lecture.get(
                "allocation_id"
            )

            allocation_counts[
                allocation_id
            ] = (
                allocation_counts.get(
                    allocation_id,
                    0
                )
                + 1
            )

        for allocation in self.allocations:

            allocation_id = getattr(
                allocation,
                "id",
                None
            )

            required_hours = max(
                1,
                int(
                    getattr(
                        allocation,
                        "weekly_hours",
                        1
                    )
                )
            )

            actual_hours = allocation_counts.get(
                allocation_id,
                0
            )

            # Missing or extra classes are hard failures
            if actual_hours != required_hours:

                fitness -= (
                    abs(
                        required_hours
                        - actual_hours
                    )
                    * 10000
                )

        # ==========================================
        # REWARD COMPLETE TIMETABLE
        # ==========================================

        expected_classes = sum(
            max(
                1,
                int(
                    getattr(
                        allocation,
                        "weekly_hours",
                        1
                    )
                )
            )
            for allocation in self.allocations
        )

        if len(timetable) == expected_classes:

            fitness += 1000

        return fitness

    # =========================================================
    # RUN GENETIC ALGORITHM
    # =========================================================

    def run(self):

        print("\n==========================================")
        print("GENETIC ALGORITHM STARTED")
        print("Population Size :", self.population_size)
        print("Generations     :", self.generations)
        print("Mutation Rate   :", self.mutation_rate)
        print("Allocations     :", len(self.allocations))
        print("Teaching Slots  :", len(self.teaching_slots))
        print("==========================================")

        population = []

        attempts = 0
        max_attempts = self.population_size * 50

        # ======================================
        # CREATE INITIAL POPULATION
        # ======================================

        while (
            len(population) < self.population_size
            and attempts < max_attempts
        ):

            timetable = self.create_random_timetable()

            if timetable is not None:

                population.append(timetable)

            attempts += 1

        if not population:

            print("\n==========================================")
            print("FAILED TO CREATE INITIAL POPULATION")
            print("==========================================")

            return []

        best_timetable = None
        best_fitness = float("-inf")

        # ======================================
        # GENERATIONS
        # ======================================

        for generation in range(self.generations):

            scored_population = []

            for timetable in population:

                fitness = self.calculate_fitness(
                    timetable
                )

                scored_population.append(
                    (
                        fitness,
                        timetable
                    )
                )

            scored_population.sort(
                key=lambda x: x[0],
                reverse=True
            )

            current_best_fitness = (
                scored_population[0][0]
            )

            current_best_timetable = (
                scored_population[0][1]
            )

            print(
                f"Generation "
                f"{generation + 1}/{self.generations} "
                f"| Best Fitness = "
                f"{current_best_fitness}"
            )

            if current_best_fitness > best_fitness:

                best_fitness = current_best_fitness

                best_timetable = current_best_timetable

            # ==================================
            # ELITISM
            # ==================================

            new_population = []

            elite_count = min(
                2,
                len(scored_population)
            )

            for i in range(elite_count):

                new_population.append(
                    scored_population[i][1]
                )

            # ==================================
            # CREATE NEXT GENERATION
            # ==================================

            while (
                len(new_population)
                < self.population_size
            ):

                timetable = (
                    self.create_random_timetable()
                )

                if timetable is not None:

                    new_population.append(
                        timetable
                    )

                else:

                    break

            if not new_population:

                break

            population = new_population

        # ======================================
        # FINAL RESULT
        # ======================================

        print("\n==========================================")
        print("GENETIC ALGORITHM FINISHED")
        print("Best Fitness :", best_fitness)
        print(
            "Total Classes :",
            len(best_timetable)
            if best_timetable
            else 0
        )
        print("==========================================\n")

        return best_timetable or []
