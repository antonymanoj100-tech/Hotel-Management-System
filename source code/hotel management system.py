import mysql.connector as mycon
con = mycon.connect(host="localhost",user="root",passwd="sobhana",database="hotel")
def showmenu():
        while True:
                print("@" * 30)
                print("----    HOTEL AJ INN   ----")
                print("@" * 30)
                print("Press 1 - Create a New Room")
                print("Press 2 - Show All Rooms")
                print("Press 3 - Show All Vacant Rooms")
                print("Press 4 - Show All Occupied Rooms")
                print("Press 5 - Book a Room")
                print("Press 6 - Check Out")
                print("Press 7 - Exit")
                choice = int(input("Enter your choice : "))
                if choice == 1:
                    createRoom()
                elif choice == 2:
                    showRooms()
                elif choice == 3:
                    showVacantRooms()
                elif choice == 4:
                    showOccupiedRooms()
                elif choice == 5:
                    bookRoom()
                elif choice == 6:
                    checkout()
                elif choice == 7:
                    break
def createRoom():
    print(" --- ENTER ROOM DETAILS  --- ")
    rno = int(input("Enter Room No. : "))
    rtype = input("Enter Room Type(Simple/Delux/Super Delux):")
    guest = int(input("Enter maximum number of guests : "))
    loc = input("Enter Location details : ")
    rent = int(input("Enter Per Day Charges : "))
    status = "Vacant"
    q = "insert into room values(%s,%s,%s,%s,%s,%s)"
    data = (rno,rtype,loc,guest,rent,status)
    cr1 = con.cursor()
    cr1.execute(q,data)
    con.commit()
    print("---  Room Created Successfully  ---")

def showRooms():
    q = "select * from room"
    cr1 = con.cursor()
    cr1.execute(q)
    res = cr1.fetchall()
    for row in res:
        print(row)

def showVacantRooms():
    q = "select * from room where status='Vacant'"
    cr1 = con.cursor()
    cr1.execute(q)
    res = cr1.fetchall()
    if res==[]:
            print("No vacant rooms")
    for row in res:
        print(row)
    return res
def showOccupiedRooms():
    q = "select room_no, cname, phone from room,booking where status='Occupied'  and room.rno=booking.room_no"
    cr1 = con.cursor()
    cr1.execute(q)
    res = cr1.fetchall()
    if res==[]:
            print("No Occupied rooms")
    for row in res:
        print(row)

"""def bookRoom():
    print("-" * 40)
    print("       BOOKING A ROOM ")
    print("-" * 40)
    print("vacant rooms")
    k=showVacantRooms()
    cname = input("Enter the Customer Name : ")
    idtype = input("Enter the ID submitted(PAN Card/License/Aadhar Card/Passport) : ")
    idno = input("Enter the ID number : ")
    address = input("Enter Address : ")
    phone = input("Enter Phone number : ")
    gender = input("Enter Gender : ")
    dcheckin = input("Enter Date of Check in (yyyy-mm-dd) : ")
    room_no = int(input("Enter Room number : "))
    q = "select * from room where status='Vacant'"
    cr1 = con.cursor()
    cr1.execute(q)
    res = cr1.fetchall()
    found=0
    for i in res:
            if i[0]==room_no:
                    found=1
            else:
                    found = 0
    if found==0:
             print("Enter a valid room number")
             room_no = int(input("Enter Room number : "))
    if k!=[]:
                    q = "insert into booking(cname,idno,idtype,address,phone,gender,dcheckin,room_no) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    data = (cname,idno,idtype,address,phone,gender,dcheckin,room_no)
                    cr = con.cursor()
                    cr.execute(q,data)
                    con.commit()
                    q = "update room set status='Occupied' where rno ="+ str(room_no)
                    cr.execute(q)
                    con.commit()
                    print("-" * 50)
                    print("      ROOM BOOKED")
                    print("-" * 50)"""
def bookRoom():
    print("-" * 40)
    print("       BOOKING A ROOM ")
    print("-" * 40)
    
    # Show vacant rooms
    vacant_rooms = showVacantRooms()
    if not vacant_rooms:
        print("No vacant rooms available.")
        return

    print("Vacant Rooms:")
    for room in vacant_rooms:
        print(f"Room Number: {room[0]}")

    cname = input("Enter the Customer Name: ")
    idtype = input("Enter the ID submitted (PAN Card/License/Aadhar Card/Passport): ")
    idno = input("Enter the ID number: ")
    address = input("Enter Address: ")
    phone = input("Enter Phone number: ")
    gender = input("Enter Gender: ")
    dcheckin = input("Enter Date of Check in (yyyy-mm-dd): ")

    # Validate room number input
    while True:
        try:
            room_no = int(input("Enter Room number: "))
            break
        except ValueError:
            print("Please enter a valid room number.")

    # Check if the room is vacant
    query = "SELECT * FROM room WHERE rno = %s AND status='Vacant'"
    cr1 = con.cursor()
    cr1.execute(query, (room_no,))
    res = cr1.fetchall()

    if not res:
        print("Invalid room number or the room is not vacant.")
        return

    # Proceed with booking
    insert_query = """
        INSERT INTO booking(cname, idno, idtype, address, phone, gender, dcheckin, room_no)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (cname, idno, idtype, address, phone, gender, dcheckin, room_no)
    cr1.execute(insert_query, data)
    con.commit()

    # Update room status to Occupied
    update_query = "UPDATE room SET status='Occupied' WHERE rno = %s"
    cr1.execute(update_query, (room_no,))
    con.commit()

    print("-" * 50)
    print("      ROOM BOOKED")
    print("-" * 50)

            
#Function to checkout a guest

def checkout():
    room_no = input("Enter the Room Number: ")
    
    # Check if the room is occupied
    query = "SELECT room_no, cname, phone FROM room, booking WHERE status='Occupied' AND room_no=%s"
    cr1 = con.cursor()
    cr1.execute(query, (room_no,))
    res = cr1.fetchall()

    if not res:
        print("Room is not currently occupied or does not exist.")
        return

    checkout_date = input("Enter the date of Checkout: ")

    # Update the room status to Vacant
    update_query = "UPDATE room SET status='Vacant' WHERE rno=%s"
    cr1.execute(update_query, (room_no,))
    con.commit()

    print("-" * 40)
    print("       CHECKOUT SUCCESS ")
    print("-" * 40)

    # Optional: Show updated room status
    cr1.execute("SELECT * FROM room")
    tes = cr1.fetchall()
    for i in tes:
        if i[0] == int(room_no) and i[5] == "Vacant":
            print(f"Room {i[0]} is now Vacant.")
            break

if con.is_connected():
        showmenu()


