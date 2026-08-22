# 🎓 College Timetable Generator Using Genetic Algorithm

A web-based **College Timetable Generator** that automatically creates optimized weekly timetables using a **Genetic Algorithm**.

The system schedules subjects, faculty, classrooms, sections, and time slots while avoiding conflicts and satisfying scheduling constraints.

## 🚀 Features

* 🧬 Genetic Algorithm-based optimization
* 👨‍🏫 Prevents faculty clashes
* 🏫 Prevents classroom clashes
* 🎓 Prevents section clashes
* 🔬 Supports laboratory sessions with consecutive periods
* 📚 Ensures required weekly teaching hours
* ☕ Excludes break and lunch periods
* 🧪 Crossover and mutation operations
* ⭐ Elitism to preserve the best solutions
* 📈 Fitness-based optimization across generations
* 🔍 Filter timetables by department, semester, and section

## 🧬 Genetic Algorithm Process

```text
Initial Population
       ↓
Fitness Evaluation
       ↓
Parent Selection
       ↓
Crossover
       ↓
Mutation
       ↓
Next Generation
       ↓
Best Timetable
```

Each timetable is treated as a **chromosome**.

The algorithm evaluates timetable quality using a fitness function and improves solutions over multiple generations.

## ⚙️ Technologies Used

* Python
* Flask
* MySQL
* HTML
* CSS
* JavaScript
* Genetic Algorithm

## 🔒 Scheduling Constraints

The system ensures:

* No faculty member is assigned to two classes at the same time.
* No classroom is assigned to multiple classes at the same time.
* No section has multiple classes in the same time slot.
* Each subject receives its required weekly hours.
* Laboratory sessions occupy consecutive periods.
* Only valid teaching slots are used.
* Faculty availability is respected.

## 📊 Genetic Algorithm Configuration

```python
population_size = 30
generations = 100
mutation_rate = 0.1
```

The algorithm uses:

* **Selection** – chooses the strongest timetable solutions.
* **Crossover** – combines two parent solutions.
* **Mutation** – changes time slots or classrooms to introduce diversity.
* **Elitism** – preserves the best solutions.
* **Fitness Function** – evaluates timetable quality and penalizes conflicts.

## 💻 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/college-timetable-generator.git
cd college-timetable-generator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your **MySQL database** and update the database connection settings.

Run the application:

```bash
python app.py
```

## 🎯 Project Goal

The goal of this project is to automate college timetable generation and use a **Genetic Algorithm** to search for better scheduling solutions while satisfying academic and resource constraints.

## 👨‍💻 Author

Developed as an academic project for automated college timetable generation and optimization.
