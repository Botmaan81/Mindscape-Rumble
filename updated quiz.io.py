import mysql.connector as sqltor
import sys
import random
import pandas as pd
import matplotlib.pyplot as plt

# Database connection
mydb = sqltor.connect(
    host="localhost",
    user="root",
    password="root",
    database='quiz'
)
mycursor = mydb.cursor()

# Main Program Layout
def Home():
    print('''Welcome To Quiz.io
1. Format Questions
2. Take Quiz
3. Question Bank
4. Exit
''')
    try:
        f = int(input('Enter Your Choice:'))
    except ValueError:
        print('Please enter a valid number.')
        Home()
        return

    print()
    if f == 1:
        pass_word = input('Enter Teacher Password: ')
        if pass_word == 'Welcome':
            Format_Ques()
        else:
            print('You have entered an invalid password, please try again....')
            Home()
    elif f == 2:  # To take the Quiz
        Quiz()
    elif f == 3:  # To see the Questions
        Ques_Bank()
    elif f == 4:  # To exit
        print('Exiting The Quiz...')
        mydb.commit()
        mycursor.close()
        mydb.close()
        sys.exit()
    else:  # Invalid input
        print('You have entered an invalid input, please try again')
        print()
        Home()

# Program To feed Questions into the System
def Format_Ques():
    try:
        ch = int(input('''What do you wish to format in the Question Bank
1) Add Questions
2) Update Questions
3) Delete Questions
4) Exit
Enter your Choice: '''))
    except ValueError:
        print('Please enter a valid number.')
        Format_Ques()
        return

    print()
    
    # Entering Questions
    if ch == 1:
        Add_Ques()
    elif ch == 2:
        Update_Ques()
    elif ch == 3:
        Remove_Ques()
    elif ch == 4:
        Home()
    else:
        print('Please Enter a valid response')
        Format_Ques()

# Program to take the Quiz         
def Quiz():
    print('Welcome To Quiz Portal')
    print()
    mycursor.execute("SELECT * FROM ques_bank")
    data = mycursor.fetchall()
    st_id = input('Enter your Scholar no.: ')
    name = input('Enter your Name: ')
    rc = mycursor.rowcount
    try:
        noq = int(input('Enter the number of questions to attempt: '))
    except ValueError:
        print('Please enter a valid number.')
        Quiz()
        return

    if rc >= noq:
        l = random.sample(range(rc), noq)  # Get unique random indices
        print('Quiz has started')
        score = 0

        for i in l:
            question = data[i]
            print()
            print('Q.', question[1])  # Display the question text
            print('A.', question[2], '\t\tB.', question[3], '\t\tC.', question[4], '\t\tD.', question[5])
            print()
            ans = None
            while ans is None:
                choice = input('Answer (A, B, C, D): ').strip().upper()
                if choice in ['A', 'B', 'C', 'D']:
                    ans = question[2 + ord(choice) - ord('A')]
                else:
                    print('Kindly select A, B, C, or D as options only')

            if ans == question[6]:
                print('Correct!!')
                score += 1
            else:
                print(f'Sorry but your answer is incorrect... the correct answer is {question[6]}')

        print(f'The Quiz has ended!! {name}, Your final score is = {score} Points!!')
        print()
        
        feature = input('Do You wish to see Percentage of your Performance (Yes/No): ').strip().lower()
        if feature == 'yes':
            percentage = (score / noq) * 100
            print(f'You got {percentage:.2f}%')
        elif feature != 'no':
            print('Please Enter a Valid Response')

        graph = input('Do you wish to see your performance graphically (Yes/No): ').strip().lower()
        print()
        
        mycursor.execute('INSERT INTO student_score (scholar_no, name, ques_attempt, score) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE score = score, ques_attempt = ques_attempt', (st_id, name, noq, score))

        if graph == 'yes':
            mycursor.execute('SELECT score FROM student_score')
            mark_obt = [item[0] for item in mycursor.fetchall()]
            mycursor.execute('SELECT ques_attempt FROM student_score')
            ques_attempt = [item[0] for item in mycursor.fetchall()]
            plt.plot(ques_attempt, mark_obt)
            plt.xlabel('Questions Attempted')
            plt.ylabel('Marks Obtained')
            plt.title('Performance Chart')
            plt.show()
        elif graph != 'no':
            print('Please Enter a Valid response')

        print()
        input('Press ENTER to continue')
        print()
        Home()
    else:
        print(f'You have entered more than possible questions asked in the quiz... Please enter a maximum of {rc} number of questions to attempt')
        print()
        Quiz()

def Ques_Bank():
    print('Welcome to Question Bank')
    print()
    f = int(input('''What do you wish to refer from the Question Bank 
1. Full Table
2. Size
3. Shape
4. A Certain question
5. Exit
Enter your choice no.: '''))
    print()
    if f == 1:
        mycursor.execute("SELECT * FROM ques_bank")
        for row in mycursor.fetchall():
            print(row)
        print()
    elif f == 2:
        mycursor.execute("SELECT COUNT(*) FROM ques_bank")
        print(f'Total Questions: {mycursor.fetchone()[0]}')
        print()
    elif f == 3:
        mycursor.execute("SELECT COUNT(*) FROM ques_bank")
        print(f'Shape: (Rows: {mycursor.fetchone()[0]}, Columns: 6)')
        print()
    elif f == 4:
        num = int(input('Please enter which question do you want to view: '))
        print()
        mycursor.execute('SELECT * FROM ques_bank WHERE qid = %s', (num,))
        question = mycursor.fetchone()
        if question:
            print(question)
        else:
            print('Please enter a valid question number.')
            print()
            Ques_Bank()
    elif f == 5:
        print()
    else:
        print('Invalid choice, please try again.')
        print()
        Ques_Bank()

    print('To proceed please press ENTER')
    print()
    Home()

def Add_Ques():
    print('Welcome To Question Portal')
    ques = input('Enter Question: ')
    opt1 = input('Enter Option 1: ')
    opt2 = input('Enter Option 2: ')
    opt3 = input('Enter Option 3: ')
    opt4 = input('Enter Option 4: ')
    
    # Choosing the Answer
    ans = None
    while True:
        try:
            op = int(input('Enter Correct Option No. (1-4): '))
            if op in [1, 2, 3, 4]:
                ans = [opt1, opt2, opt3, opt4][op - 1]
                break
            else:
                print('Please choose a valid option (1-4).')
        except ValueError:
            print('Please enter a valid number.')

    # Using Connection to feed questions into the Database
    mycursor.execute("INSERT INTO ques_bank (ques, opt1, opt2, opt3, opt4, ans) VALUES (%s, %s, %s, %s, %s, %s)", (ques, opt1, opt2, opt3, opt4, ans))           
    mydb.commit()
    add_ques = input('Question added successfully.. Do you want to add more (Yes/No): ').strip().lower()
    if add_ques == 'yes':
        Add_Ques()
    else:
        Format_Ques()

def Update_Ques():
    print('Welcome To Question Portal')
    print()
    print('Select your question which you want to update from the bank')
    mycursor.execute("SELECT * FROM ques_bank")
    for row in mycursor.fetchall():
        print(row)
    print()
    
    up_ques = int(input('Enter the question no. that you want to update in the Question Bank: '))
    mycursor.execute('SELECT * FROM ques_bank WHERE qid = %s', (up_ques,))
    if mycursor.fetchone():
        opt1 = input('Enter Option 1: ')
        opt2 = input('Enter Option 2: ')
        opt3 = input('Enter Option 3: ')
        opt4 = input('Enter Option 4: ')
        
        # Choosing the Answer
        ans = None
        while True:
            try:
                op = int(input('Enter Correct Option No. (1-4): '))
                if op in [1, 2, 3, 4]:
                    ans = [opt1, opt2, opt3, opt4][op - 1]
                    break
                else:
                    print('Please choose a valid option (1-4).')
            except ValueError:
                print('Please enter a valid number.')

        # Using Connection to update questions in the Database
        mycursor.execute('UPDATE ques_bank SET opt1 = %s, opt2 = %s, opt3 = %s, opt4 = %s, ans = %s WHERE qid = %s', (opt1, opt2, opt3, opt4, ans, up_ques))
        mydb.commit()
        print('Your Question has been updated. Please check the Question Bank for more info...')
    else:
        print('Your requested question does not exist.')
        print()
        Format_Ques()

def Remove_Ques():
    print('Welcome to Question Portal')
    print()
    print('Select the Question which you want to remove from the bank')
    mycursor.execute("SELECT * FROM ques_bank")
    for row in mycursor.fetchall():
        print(row)
    rem_ques = int(input('Enter the question no. that you want to remove from the Question Bank: '))
    mycursor.execute('SELECT * FROM ques_bank WHERE qid = %s', (rem_ques,))
    if mycursor.fetchone():
        mycursor.execute('DELETE FROM ques_bank WHERE qid = %s', (rem_ques,))
        mydb.commit()
        print('Question has been removed from the Question Bank.')
    else:
        print('Your requested question does not exist.')
        Format_Ques()

Home()