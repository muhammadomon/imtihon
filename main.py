from databases import *

def login_register():
    n=input("1.Login \n2.Register \nTanlang: ")

    if n=='1':
        username=input("Username: ")
        password=input("Password: ")

        login(username, password)

        b=is_admin(username)
        
        if b:
            admin_menu()

        elif b==False:
            pupil_menu(username)

        


    elif n=='2':
        first_name=input('Name: ')
        last_name=input('Surname: ')
        birth_day=input("Birthday: ")
        phone=input('Phone(ex.+998991234567): ')
    
        username=input("Username: ")

        password=input("Password: ")
        password2=input("Password confirm: ")

        if password==password2:
            data=dict(
                first_name=first_name,
                last_name=last_name,
                birth_day=birth_day,
                phone=phone,
                username=username,
                password=password
            )

            add_user(data)
            print("Success")
            login_register()
        else:
            print("Password Error! Try again")
            login_register()

        
login_register()


         