from flask import Flask, render_template, request, redirect, url_for, session
from forms import CreateFormatForm, CreateStaffForm
import shelve, Format, Customer
import Username
from signupform import CreateUserFormSignup
from loginform import CreateUserFormLogin

app = Flask(__name__)
admin_dict={
    'password':'1234567890',
    'staff_id':'88900'
}

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


@app.route('/navbar2')
def navbar():
    return render_template('navbar2.html')

@app.route('/error')
def error():
    return render_template("error.html")


@app.route('/createForm', methods=['GET', 'POST'])
def create_form():
    create_format_form = CreateFormatForm(request.form)
    if request.method == 'POST' and create_format_form.validate():
        users_dict = {}
        db = shelve.open('form.db', 'c')
        try:
            users_dict = db['forms']
        except:
            print("Error in retrieving Users from user.db.")
        form = Format.User(create_format_form.first_name.data, create_format_form.last_name.data,
                         create_format_form.gender.data, create_format_form.membership.data, create_format_form.remarks.data)
        users_dict[form.get_user_id()] = form
        db['forms'] = users_dict
        db.close()
        return render_template('home.html')
    return render_template('createForm.html', form=create_format_form)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_staff_form.validate():
        staffs_dict = {}
        db = shelve.open('staff.db', 'c')
        try:
            staffs_dict = db['staff']
        except:
            print("Error in adding Credentials to staff.db.")

        customer = Customer.customer(create_staff_form.first_name.data,
                                     create_staff_form.last_name.data,
                                     create_staff_form.gender.data, create_staff_form.membership.data,
                                     create_staff_form.remarks.data, create_staff_form.email.data,
                                     create_staff_form.date_joined.data, create_staff_form.address.data)
        staffs_dict[customer.get_customer_id()] = customer
        db['staff'] = staffs_dict
        db.close()
        if create_staff_form.last_name.data == admin_dict['password'] and create_staff_form.address.data == admin_dict['staff_id']:
            return render_template('navbar2.html')
        else: return render_template('error.html')
    return render_template('createCustomer.html', form=create_staff_form)



@app.route('/retrieveForms')
def retrieve_forms():
    forms_dict = {}
    db = shelve.open('form.db', 'r')
    forms_dict = db['forms']
    db.close()

    forms_list = []
    for key in forms_dict:
        form = forms_dict.get(key)
        forms_list.append(form)
    return render_template('retrieveForms.html', count=len(forms_list), forms_list=(forms_list))


@app.route('/retrieveCustomers')
def retrieve_customers():
    staffs_dict = {}
    db = shelve.open('staff.db', 'r')
    staffs_dict = db['staff']
    db.close()

    staffs_list = []
    for key in staffs_dict:
        staff = staffs_dict.get(key)
        staffs_list.append(staff)
    return render_template('retrieveCustomers.html', count=len(staffs_list), customers_list=staffs_list)



@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateStaffForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        staffs_dict = {}
        db = shelve.open('staff.db', 'w')
        customers_dict = db['staff']
        customer = customers_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_membership(update_customer_form.membership.data)
        customer.set_remarks(update_customer_form.remarks.data)
        customer.set_date_joined(update_customer_form.date_joined.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_address(update_customer_form.address.data)
        db['staff'] = customers_dict
        db.close()
        return redirect(url_for('retrieve_customers'))
    else:
        staffs_dict = {}
        db = shelve.open('staff.db', 'r')
        customers_dict = db['staff']
        db.close()
        customer = customers_dict.get(id)
        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.membership.data = customer.get_membership()
        update_customer_form.remarks.data = customer.get_remarks()
        update_customer_form.date_joined.data = customer.get_date_joined()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.address.data = customer.get_address()

        return render_template('updateCustomer.html', form=update_customer_form)


@app.route('/deleteForm/<int:id>', methods=['POST'])
def delete_form(id):
    users_dict = {}
    db = shelve.open('form.db', 'w')
    users_dict = db['forms']
    users_dict.pop(id)
    db['forms'] = users_dict
    db.close()
    return render_template('navbar2.html')


@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('staff.db', 'w')
    customers_dict = db['staff']
    customers_dict.pop(id)
    db['staff'] = customers_dict
    db.close()
    Login=False
    while Login==False:
     return render_template('navbar2.html')


app.secret_key = 'myguy'


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/error2')
def error2():
    return render_template('error2.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    create_user_form =  CreateUserFormLogin(request.form)
    if request.method == 'POST':
        username = create_user_form.username.data
        password = create_user_form.password.data

        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['user']
        db.close()

        for key in users_dict:
            user = users_dict.get(key)
            if username == user.get_username() and password == user.get_password():
                return redirect(url_for('home2'))
            else:
                return redirect(url_for('signup'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    create_user_form = CreateUserFormSignup(request.form)
    if request.method == 'POST':
        user = Username.User(create_user_form.username.data,create_user_form.password.data)
        username=create_user_form.username.data
        user_dict = {}
        user_dict[username]=user

        db = shelve.open("user.db", "c")
        db['user'] = user_dict
        db.close()


        return redirect(url_for('home2'))
    return render_template('signup.html')


@app.route('/home2')
def home2():
    if 'username' in session:
        username = session['username']
        return f'Logged in as {username}!<br><b><a href = "/logout">click here to logout</a></b>'
    return render_template('home2.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

user_dict={}
db=shelve.open("user.db","c")
try:
    if 'user' in db:
        login_dict=db['user']
    else:
        db['user']=user_dict
        db.close()
except:
    None



if __name__ == '__main__':
    app.run()