import mysql.connector as conn
from datetime import date
from datetime import timedelta

mydb = conn.connect(host="localhost", user="root", port=3307, passwd="22Ma33aM@123")
cursor = mydb.cursor()
cursor.execute("use library")
def selectIt():
    print("\n") 
    print("-------------------------------------------")
    print("Press 1: To view all available books")
    print("Press 2: To add a new book")
    print("Press 3: To see available users")
    print("Press 4: To add a new user")
    print("Press 5: To issue a book")
    print("Press 6: To return a book")
    print("Press 7: To remove a book")
    print("Press 8: To see the issue record")
    print("Press 9: To see overdue records")
    print("-------------------------------------------")
    print("\n")
    
selectIt()
choice = 0
while choice != 10:
    print("\n")
    print("---------------------------------------------")
    choice = int(input("Enter your choice            :        "))
    print("---------------------------------------------")
    print("\n")

    if choice == 1:
        cursor.execute("Select * from Book_data")
        data = cursor.fetchall()
        for i in data:
            print("Id                    ", i[0])
            print("Title                 ", i[1])
            print("Author                ", i[2])
            print("Availabity Status     ", i[3])
            print("Quantity Available    ", i[4])
            print("-------------------------------------------")
        selectIt()
            
            
    if choice == 2:
        print("To add a new book")
        Id = input("Enter book ID                :        ")
        cursor.execute("SELECT * FROM Book_data WHERE Book_Id = '{}'".format(Id))
        data = cursor.fetchone()
        if cursor.rowcount > 0:
            print(" ********** This book already exists **********")
            ch=int(input("If you wish to reset the quantity of the current book press 1 , else 0  :  "))
            if ch==1:
                qty=int(input("Enter the new set quantity                                              :  "))
                cursor.execute("update book_data set quantity_available={} where book_id='{}' ".format(qty,Id))
                mydb.commit()
                print("Quantity updated Successfully")
                selectIt()
            else:
                selectIt()
                continue
        else:
            title = input("Enter Book name              :        ")
            author = input("Enter Author name            :        ")
            qty_available = int(input("Enter Quantity available     :        "))
            cursor.execute(
                "INSERT INTO BOOK_DATA VALUES('{}','{}','{}','{}',{})".format(
                    Id, title, author, "YES", qty_available
                )
            )
            if cursor.rowcount > 0:
                print("Data inserted successfully")
            else:
                print("Please try again")

            mydb.commit()
            selectIt()

    if choice == 3:
        cursor.execute("Select * from user")
        data = cursor.fetchall()
        for i in data:
            print("User Id                    ", i[0])
            print("Name                       ", i[1])
            print("-----------------------------------")
        selectIt()
        

    if choice == 4:
        new_user_id = int(input("Enter User ID                :        "))
        cursor.execute("SELECT * FROM user WHERE User_Id = {}".format(new_user_id))
        data = cursor.fetchone()
        if cursor.rowcount > 0:
            print("This user already exists")
            continue
        else:
            name = input("Enter your name              :        ")
            cursor.execute("INSERT INTO USER VALUES({},'{}')".format(new_user_id, name))
            if cursor.rowcount > 0:
                print("Data inserted successfully")
            else:
                print("Please try again")

            mydb.commit()
        selectIt()


    if choice == 5:
        user_id = int(input("Enter User ID                                    "))
        cursor.execute("SELECT * FROM user WHERE User_Id = {}".format(user_id))
        data = cursor.fetchone()
        if cursor.rowcount == 0:
            print("No user exists")
            continue
        else:
            number_of_books = int(input("Enter number of books to issue                   "))
            if number_of_books > 3 and number_of_books < 0:
                print("You can't issue more than 3 books")
            else:
                for x in range(number_of_books):
                    book_id = input(
                        "Enter Book Id of the book you want to issue      "
                    )
                    cursor.execute(
                        "SELECT * FROM BOOK_DATA WHERE BOOK_ID=%s", (book_id,)
                    )
                    data = cursor.fetchone()
                    if cursor.rowcount == 0:
                        print("No book with this id exists")
                        x -= 1

                    else:
                        today = date.today()
                        return_date = today + timedelta(days=14)
                        days_left = (return_date - today).days
                        cursor.execute(
                            "INSERT INTO ISSUE_DATA VALUES({},'{}','{}','{}','{}')".format(
                                user_id, book_id, today, return_date, "NO"
                            )
                        )
                        mydb.commit()
                        
                        cursor.execute("update book_data set Quantity_Available=Quantity_Available-1 where book_id='{}' ".format(book_id))
                        mydb.commit()
                        print("Book issued successfully")
        selectIt()

    if choice == 6:
        user_id = int(input("Enter User Id  :  "))
        book_id = input("Enter Book Id  :  ")
        cursor.execute(
            "Select * from issue_data where user_id={} and book_id='{}'".format(
                user_id, book_id
            )
        )

        data = cursor.fetchall()
        if cursor.rowcount == 0:
            print("No such record exists")
            selectIt()
        else:
            cursor.execute("SELECT datediff(curdate(),issue_date) FROM issue_data WHERE user_id = {} AND book_id = '{}'".format(user_id, book_id))

            data2 = cursor.fetchall()
            cursor.execute(
                "update book_data set Quantity_Available=Quantity_Available+1 where book_id='{}'".format(
                    book_id
                )
            )
            data3=cursor.fetchall()
            mydb.commit()
            cursor.execute(
                "delete from issue_data where user_id={} and book_id='{}' ".format(
                    user_id, book_id
                )
            )
            mydb.commit()
            print("Return successful")
            
            
            if data2[0][0] > 14:
                print("As your book is overdue , you need to pay a fine of ",data2[0][0]-14,"$")
            selectIt()

    if choice == 7:
        book_id = input("Enter Book Id which you want to delete    :    ")
        cursor.execute("SELECT * FROM BOOK_DATA WHERE BOOK_ID=%s", (book_id,))
        data = cursor.fetchall()
        if cursor.rowcount == 0:
            print("No book with this id exists")
        else:
            cursor.execute("SELECT * FROM issue_DATA WHERE BOOK_ID=%s", (book_id,))
            data2 = cursor.fetchall()
            print("The following records still have this book")
            for i in data2 :
                print("User ID                    ", i[0])
                print("Book ID                    ", i[1])
                print("Issue Date                 ", i[2])
                print("Expected Return Date       ", i[3])
                print("--------------------------------------------------------------")
            ch=int(input("Are you sure you want to delete the book. Press 1 for yes and any other number for no    :    "))
            if ch==1:
                cursor.execute("DELETE FROM BOOK_DATA WHERE BOOK_ID=%s", (book_id,))
                print("Book deleted successfully")
                mydb.commit()
            else:
                print("****************** No deletion has happened ******************")
        selectIt()
        
        
    if choice == 8:
        # days_left = (return_date-today).days
        today = date.today()
        cursor.execute(
            "update issue_data set overdue_status='YES' where datediff(curdate(),issue_date)>14"
        )
        mydb.commit()
        cursor.execute("Select * from issue_data")
        data = cursor.fetchall()
        cursor.execute("Select datediff(curdate(),issue_date) from issue_data")
        data2 = cursor.fetchall()
        j = 0
        for i in data:
            print("User ID                    ", i[0])
            print("Book ID                    ", i[1])
            print("Issue Date                 ", i[2])
            print("Expected Return Date       ", i[3])
            print("Overdue Status             ", i[4])
            if data2[j][0] < 14:
                print(
                    "Fine                        None",
                )
            else:
                print("Fine                       ", data2[j][0] - 14, "$")
            print()
            j += 1
            print("-----------------------------------------")
        selectIt()
            
            
            
            
    if choice == 9 :
        today = date.today()
        cursor.execute(
            "update issue_data set overdue_status='YES' where datediff(curdate(),issue_date)>14"
        )
        mydb.commit()
        cursor.execute("Select * from issue_data where overdue_status='YES' ")
        data = cursor.fetchall()
        cursor.execute("Select datediff(curdate(),issue_date) from issue_data where overdue_status='YES'")
        data2 = cursor.fetchall()
        j = 0
        for i in data:
            print("User ID                    ", i[0])
            print("Book ID                    ", i[1])
            print("Issue Date                 ", i[2])
            print("Expected Return Date       ", i[3])
            print("Overdue Status             ", i[4])
            if data2[j][0] < 14:
                print(
                    "Fine                        None",
                )
            else:
                print("Fine                       ", data2[j][0] - 14, "$")
            j += 1
            print("-----------------------------------")
            selectIt()