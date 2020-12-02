import re
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


# Create database file
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

# Create table
Base = declarative_base()


class ToDo(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date)

    def __repr__(self):
        return self.task


def create_database():
    """Create Database"""

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Access database
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def get_rows_results(rows):
    """Get table results based on date query"""
    output = ''

    if rows:
        for i, task in enumerate(rows):
            output += '' + '{}. {}. {} {}\n'\
                .format(i + 1, task, task.deadline.day,
                        task.deadline.strftime('%b'))
        return output

    return 'Nothing to do!\n'


def get_tasks(session, tasks_date):
    """Print database tasks"""

    output = ""
    today = datetime.today()

    if tasks_date == "today":
        output = f"Today {today.day} {today.strftime('%b')}:\n"
        rows = session.query(ToDo).filter(ToDo.deadline == today.date()).all()
        output += get_rows_results(rows)

    elif tasks_date == "week":
        for i in range(7):
            day = today + timedelta(days=i)
            output += f"{day.strftime('%A')} {day.day} {day.strftime('%b')}:\n"
            rows = session.query(ToDo).filter(ToDo.deadline == day.date()).all()
            output += get_rows_results(rows)
            output += '\n'

    elif tasks_date == "all":
        output = "All tasks:\n"
        rows = session.query(ToDo).order_by(ToDo.deadline).all()
        output += get_rows_results(rows)

    elif tasks_date == "missed":
        output = "Missed tasks:\n"
        rows = session.query(ToDo).order_by(ToDo.deadline <= today.date()).all()
        output += get_rows_results(rows)

    print(output)


def add_task(session):
    """Add task to database"""

    # Create new row
    task_to_add = str(input("Enter task\n"))
    task_deadline = str(input("Enter deadline\n"))

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", task_deadline):
        sys.exit("Bad deadline format need to input format: YYYY-MM-DD")

    new_row = ToDo(task=f'{task_to_add}',
                   deadline=datetime.strptime(task_deadline,
                                              '%Y-%m-%d').date()
                   )
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def delete_task(session):
    """Remove a task from database"""

    user_input = "Choose the number of the task you want to delete:\n"
    rows = session.query(ToDo).order_by(ToDo.deadline).all()

    if rows:
        user_input += get_rows_results(rows)
        task_to_delete = int(input(user_input))
        specific_row = rows[task_to_delete - 1]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!")
    else:
        print("Nothing to delete")


def menu():
    """Implement user menu main function"""

    user_input = 'a'
    menu_string = "\n1) Today's tasks\n"\
                  "2) Week's tasks\n"\
                  "3) All tasks\n"\
                  "4) Missed tasks\n"\
                  "5) Add task\n"\
                  "6) Delete task\n"\
                  "0) Exit\n"

    session = create_database()

    while user_input != 0:
        user_input = int(input(f"{menu_string}"))
        if user_input == 1:
            get_tasks(session, "today")
        elif user_input == 2:
            get_tasks(session, "week")
        elif user_input == 3:
            get_tasks(session, "all")
        elif user_input == 4:
            get_tasks(session, "missed")
        elif user_input == 5:
            add_task(session)
        elif user_input == 6:
            delete_task(session)
        elif user_input == 0:
            sys.exit('Bye!')
        else:
            sys.exit('Incorrect input, try again.')


if __name__ == '__main__':
    menu()
