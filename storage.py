import sqlite3 as sql

connection_initialized = 0
def initialize_connection():
    '''Initializes connection with the users database'''
    global con 
    global cur 
    con = sql.connect("users.db")
    cur= con.cursor()
    
    connection_initialized = 1
    return True

def add_user(user_name, email, password):
    '''
    takes new user's data, and inserts them in the table 
    (only if user_name is unique)
    input:
    1. user_name: string representing unique username.
    2. email: string representing email of the new user.
    3. password: string representing password of the new user.
    output:
    1. bool value representing success or failure in adding the new
       user to the database.
    '''
    if connection_initialized == 0 and initialize_connection() == False:
        return False

    #get a user_id to assign to the user_name
    last_user_id = cur.execute('select max(user_id) from users').fetchone()[0]
    if last_user_id == None:
        new_user_id = 1
    else:
        new_user_id = last_user_id + 1

    #add username to the users table
    if len(cur.execute('select * from users where user_name=?', (user_name,)).fetchall()) != 0:
        return False

    cur.execute('insert into users values (?,?)', (new_user_id, user_name))

    #add email to the email table
    cur.execute('insert into user_emails values (?,?)', (new_user_id, email))
    #add password to the password table
    cur.execute('insert into user_passwords values (?,?)', (new_user_id, password))
    #commit the commands to the database
    con.commit()
    return True

def update_email(user_name, email):
    '''Takes user_name and email and updates the email of the user in the database
    Input:
        1. user_name: string representing user_name.
        2. email: string representing email to be updated
    Output:
        1. Boolean value representing whether the operation succeeded or not.'''
    if connection_initialized == 0 and initialize_connection() == False:
        return False

    # if username exists, update the email
    if len(cur.execute('select * from users where user_name=?', (user_name,)).fetchall()) != 0:
        #fetch the user_id of the user_name
        user_id = cur.execute('select user_id from users where user_name=?', (user_name,)).fetchone()[0]
        #udpate the email using the fetched user_id
        cur.execute('update user_emails set email=? where user_id=?', (email, user_id))
    else:
        return False

    # commit the commands to the database
    con.commit()
    return True

def update_password(user_name, password):
    '''Takes user_name and password and updates the password of the user in the database
    Input:
        1. user_name: string representing user_name.
        2. password: string representing password to be updated
    Output:
        1. Boolean value representing whether the operation succeeded or not.'''
    if connection_initialized == 0 and initialize_connection() == False:
        return False

    # if username exists, update the password
    if len(cur.execute('select * from users where user_name=?', (user_name,)).fetchall()) != 0:
        #fetch the user_id of the user_name
        user_id = cur.execute('select user_id from users where user_name=?', (user_name,)).fetchone()[0]
        #udpate the password using the fetched user_id
        cur.execute('update user_passwords set password=? where user_id=?', (password, user_id))
    else:
        return False

    # commit the commands to the database
    con.commit()
    return True

def add_summary(user_name, text):
    '''Adds summary to the table of summaries
    INPUT:
        1. user_name: string representing the user_name
        2. text: string representing the summary
    OUTPUT:
        1. A boolean value representing wether the operation succeeded or not.'''
    if connection_initialized == 0 and initialize_connection() == False:
        return False
    
    #if username exists, add summary to the table
    if len(cur.execute('select * from users where user_name=?', (user_name,)).fetchall()) != 0:
        #get the user_id
        user_id = cur.execute('select user_id from users where user_name=?', (user_name,)).fetchone()[0]
        #fetch a summary_id
        last_summary_id = cur.execute('select max(summary_id) from summaries').fetchone()[0]
        if last_summary_id == None:
            new_summary_id = 1
        else:
            new_summary_id = last_summary_id + 1
        #add summary_id and summary to the summaries table
        cur.execute('insert into summaries values (?,?,?)', (new_summary_id, user_id, text))
    else:
        return False
    #commit the commands
    con.commit()
    return True

def update_summary(summary_id, text):
    '''Updates a summary recognized by summary_id
    INPUT:
        1. summary_id: int representing unique summary_id.
        2. text: string representing the udpated summary.
    OUTPUT:
        1. Boolean value representing wether the operation succeeded or not.'''
    if connection_initialized == 0 and initialize_connection() == False:
        return False

    # if summary_id exists, update the summary
    if len(cur.execute('select * from summaries where summary_id=?', (summary_id,)).fetchall()) != 0:
        #udpate the summary using the summary_id
        cur.execute('update summaries set summary=? where summary_id=?', (text, summary_id))
    else:
        return False

    # commit the commands to the database
    con.commit()
    return True

def get_summary_list(user_name):
    '''Returns list of summaries saved by the user
    INPUT:
        1. user_name: string representing unique user_name.
    OUTUPT:
        1. A list in containing tuples of summary_id and summaries.
        2. None if there was an error in connecting to the database.'''
    if connection_initialized == 0 and initialize_connection() == False:
        return None

    #if username exists, get list of summaries
    if len(cur.execute('select * from users where user_name=?', (user_name,)).fetchall()) != 0:
        #get user_id
        user_id = cur.execute('select user_id from users where user_name=?', (user_name,)).fetchone()[0]
        #get list of (summary_id, summary)
        summary_list = cur.execute('select summary_id, summary from summaries where user_id=?', (user_id,)).fetchall()
    else:
        return []
    #return the list of (summary_id, summary)
    return summary_list

def get_user_details(user_name):
    '''Returns details of a user from its user_name
    INPUT:
        1. user_name: string representing unique user_name
    OUTPUT:
        1. A tuple in the form of (user_name, user_email, user_password)'''
    if connection_initialized == 0 and initialize_connection() == False:
        return False

    #if username exists, get user_id
    if len(cur.execute('select * from users where user_name=?', (user_name,)).fetchall()) != 0:
        user_id = cur.execute('select user_id from users where user_name=?', (user_name,)).fetchone()[0]
        #get email_id of the user
        email = cur.execute('select email from user_emails where user_id=?', (user_id,)).fetchone()[0]
        #get password of the user
        password = cur.execute('select password from user_passwords where user_id=?', (user_id,)).fetchone()[0]
        #combine user_name, email_id, password into a tuple
        user_detail = (user_id, email, password)
    else:
        return ()
    #commit the commands
    con.commit()
    #return the tuple
    return user_detail

def does_user_exist(user_name):
    '''Returns true if the user_name exists, else returns false.
    INPUT:
        1. user_name: string representing user_name to query about.
    OUTPUT:
        1. Returns either true or false.'''
    if connection_initialized == 0 and initialize_connection() == False:
        return False
    
    #if user_name exists, return True else return False
    return len(cur.execute('select * from users where user_name=?', (user_name,)).fetchall()) != 0