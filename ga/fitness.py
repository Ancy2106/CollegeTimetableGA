from collections import defaultdict


def fitness(timetable):
    """
    Calculates the fitness score of a timetable.

    Maximum score:
        1000

    Hard constraints:
        - Faculty clash
        - Classroom clash
        - Class/section clash
        - Lab must use lab room
        - Faculty must be available
        - Required weekly hours

    Soft constraints:
        - Avoid 4+ continuous classes
        - Prefer labs earlier in the day
        - Avoid last period for theory
        - Reduce faculty idle gaps
    """

    score = 1000

    # =========================================================
    # TRACK USED SLOTS
    # =========================================================

    faculty_slots = defaultdict(set)

    room_slots = defaultdict(set)

    class_slots = defaultdict(set)

    subject_hours = defaultdict(int)

    faculty_daily = defaultdict(list)

    # =========================================================
    # PROCESS EACH LECTURE
    # =========================================================

    for lecture in timetable:

        faculty = lecture.get(
            "faculty_id",
            lecture.get("faculty")
        )

        room = lecture.get(
            "room_id",
            lecture.get("room")
        )

        department = lecture.get(
            "department_id",
            lecture.get("department")
        )

        semester = lecture.get(
            "semester_id",
            lecture.get("semester")
        )

        section = lecture.get(
            "section_id",
            lecture.get("section")
        )

        day = lecture.get(
            "day"
        )

        period = lecture.get(
            "period"
        )

        slot = (
            day,
            period
        )

        # =====================================================
        # HARD CONSTRAINT 1
        # FACULTY CLASH
        # =====================================================

        if slot in faculty_slots[faculty]:

            score -= 100

        else:

            faculty_slots[
                faculty
            ].add(slot)

        # =====================================================
        # HARD CONSTRAINT 2
        # CLASSROOM CLASH
        # =====================================================

        if slot in room_slots[room]:

            score -= 100

        else:

            room_slots[
                room
            ].add(slot)

        # =====================================================
        # HARD CONSTRAINT 3
        # CLASS / SECTION CLASH
        # =====================================================

        class_name = (
            department,
            semester,
            section
        )

        if slot in class_slots[
            class_name
        ]:

            score -= 100

        else:

            class_slots[
                class_name
            ].add(slot)

        # =====================================================
        # HARD CONSTRAINT 4
        # LAB MUST USE LAB ROOM
        # =====================================================

        lecture_type = str(
            lecture.get(
                "type",
                "Theory"
            )
        ).strip().lower()

        room_type = str(
            lecture.get(
                "room_type",
                ""
            )
        ).strip().lower()

        if lecture_type == "lab":

            if "lab" not in room_type:

                score -= 100

        # =====================================================
        # HARD CONSTRAINT 5
        # FACULTY AVAILABILITY
        # =====================================================

        faculty_available = lecture.get(
            "faculty_available",
            True
        )

        if not faculty_available:

            score -= 100

        # =====================================================
        # SUBJECT HOURS
        # =====================================================

        subject_id = lecture.get(
            "subject_id",
            lecture.get("subject")
        )

        subject_hours[
            subject_id
        ] += 1

        # =====================================================
        # FACULTY DAILY PERIODS
        # =====================================================

        faculty_daily[
            (faculty, day)
        ].append(period)

    # =========================================================
    # REQUIRED WEEKLY HOURS
    # =========================================================

    required_hours = {}

    for lecture in timetable:

        subject_id = lecture.get(
            "subject_id",
            lecture.get("subject")
        )

        required = int(
            lecture.get(
                "required_hours",
                0
            )
        )

        required_hours[
            subject_id
        ] = required

    for subject_id, required in required_hours.items():

        actual = subject_hours.get(
            subject_id,
            0
        )

        if actual != required:

            difference = abs(
                required - actual
            )

            score -= (
                difference * 20
            )

    # =========================================================
    # SOFT CONSTRAINTS
    # =========================================================

    for key, periods in faculty_daily.items():

        periods = sorted(
            periods
        )

        # -----------------------------------------------------
        # Avoid 4+ continuous classes
        # -----------------------------------------------------

        continuous = 1

        for i in range(
            1,
            len(periods)
        ):

            if (
                periods[i]
                == periods[i - 1] + 1
            ):

                continuous += 1

                if continuous >= 4:

                    score -= 10

            else:

                continuous = 1

        # -----------------------------------------------------
        # Faculty idle gaps
        # -----------------------------------------------------

        if len(periods) >= 2:

            for i in range(
                1,
                len(periods)
            ):

                gap = (
                    periods[i]
                    - periods[i - 1]
                )

                if gap > 1:

                    score -= (
                        gap - 1
                    ) * 2

    # =========================================================
    # PREFER MORNING LABS
    # =========================================================

    for lecture in timetable:

        lecture_type = str(
            lecture.get(
                "type",
                "Theory"
            )
        ).strip().lower()

        period = lecture.get(
            "period"
        )

        if (
            lecture_type == "lab"
            and period is not None
        ):

            if period >= 5:

                score -= 5

    # =========================================================
    # AVOID LAST PERIOD FOR THEORY
    # =========================================================

    for lecture in timetable:

        lecture_type = str(
            lecture.get(
                "type",
                "Theory"
            )
        ).strip().lower()

        period = lecture.get(
            "period"
        )

        if (
            lecture_type == "theory"
            and period == 7
        ):

            score -= 5

    # =========================================================
    # FINAL SCORE
    # =========================================================

    return max(
        score,
        0
    )
