from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from os import environ
from dotenv import load_dotenv
from sqlalchemy import desc

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

# Tables

class Staff(db.Model):

    __tablename__ = "staff"

    staff_ID = db.Column(db.Integer, primary_key=True)
    staff_FName = db.Column(db.String(50), nullable=False)
    staff_LName = db.Column(db.String(50), nullable=False)
    staff_password = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.Enum("Chairman", "CEO", "Sales", "Consultancy", "Solutioning", "Engineering", "HR", "Finance", "IT"), nullable=False)
    country = db.Column(db.Enum("Malaysia", "Indonesia", "Vietnam", "Hong Kong", "Singapore"), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    access_ID = db.Column(db.Integer, nullable=False)


    # properties of the staff when it is created
    def __init__(self, staff_ID, staff_FName, staff_LName, staff_password, dept, country, email, access_ID):
        self.staff_ID = staff_ID
        self.staff_FName = staff_FName
        self.staff_LName = staff_LName
        self.staff_password = staff_password
        self.dept = dept
        self.country = country
        self.email = email
        self.access_ID = access_ID

    # specify how to represent our staff object as a JSON string
    def json(self):
        return {
            self.staff_ID : {
                "staff_FName": self.staff_FName,
                "staff_LName": self.staff_LName,
                "staff_password": self.staff_password,
                "dept": self.dept,
                "country": self.country,
                "email": self.email,
                "access_ID": self.access_ID
            }
        }
    

class Skill(db.Model):

    __tablename__ = "skill"

    skill_name = db.Column(db.String(50), primary_key=True)
    skill_desc = db.Column(db.Text, nullable=False)
   

    # properties of the skill when it is created
    def __init__(self, skill_name, skill_desc):
        self.skill_name = skill_name
        self.skill_desc = skill_desc

    # specify how to represent our role_listing object as a JSON string
    def json(self):
        return {
            self.skill_name: self.skill_desc
        }


class StaffSkill(db.Model):

    __tablename__ = "staff_skill"

    staff_ID = db.Column(db.Integer, db.ForeignKey("staff.staff_ID"), primary_key=True)
    skill_name = db.Column(db.String(50), db.ForeignKey("skill.skill_name"), primary_key=True)


    # properties of the staff when it is created
    def __init__(self, staff_ID, skill_name):
        self.staff_ID = staff_ID
        self.skill_name = skill_name


    # specify how to represent our staff object as a JSON string
    def json(self):
        return self.skill_name
    
    def staff_json(self):
        return {
            self.staff_ID : self.skill_name
        }


class Role(db.Model):

    __tablename__ = "role"

    role_name = db.Column(db.String(20), primary_key=True)
    role_desc = db.Column(db.Text, nullable=False)
   

    # properties of the role_listing when it is created
    def __init__(self, role_name, role_desc):
        self.role_name = role_name
        self.role_desc = role_desc

    # specify how to represent our role_listing object as a JSON string
    def json(self):
        return {
            self.role_name: self.role_desc
        }


class RoleListing(db.Model):

    __tablename__ = "role_listing"

    rolelisting_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(20), db.ForeignKey("role.role_name"), nullable=False)
    application_opening = db.Column(db.Date, nullable=False)
    application_deadline = db.Column(db.Date, nullable=False)
    manager_ID = db.Column(db.Integer, db.ForeignKey("staff.staff_ID"), nullable=False)
    dept = db.Column(db.Enum("Chairman", "CEO", "Sales", "Consultancy", "Solutioning", "Engineering", "HR", "Finance", "IT"), nullable=False)
    country = db.Column(db.Enum("Malaysia", "Indonesia", "Vietnam", "Hong Kong", "Singapore"), nullable=False)
   

    # properties of the role_listing when it is created
    def __init__(self, role_name, application_opening, application_deadline, manager_ID, dept, country):
        self.role_name = role_name
        self.application_opening = application_opening
        self.application_deadline = application_deadline
        self.manager_ID = manager_ID
        self.dept = dept
        self.country = country


    # specify how to represent our role_listing object as a JSON string
    def json(self):
        return { 
            self.rolelisting_ID : {
                "role_name": self.role_name,
                "application_opening": self.application_opening.strftime('%Y-%m-%d'),
                "application_deadline": self.application_deadline.strftime('%Y-%m-%d'),
                "manager_ID": self.manager_ID,
                "dept": self.dept,
                "country": self.country
            }
        }
    
    
class RoleSkill(db.Model):

    __tablename__ = "role_skill"

    role_name = db.Column(db.String(20), db.ForeignKey("role.role_name"), primary_key=True)
    skill_name = db.Column(db.String(50), db.ForeignKey("skill.skill_name"), primary_key=True)
   

    # properties of the role_listing when it is created
    def __init__(self, role_name, skill_name):
        self.role_name = role_name
        self.skill_name = skill_name

    # specify how to represent our role_skill object as a JSON string
    def json(self):
        return self.skill_name


class Application(db.Model):

    __tablename__ = "application"

    staff_ID = db.Column(db.Integer, db.ForeignKey("staff.staff_ID"), primary_key=True)
    rolelisting_ID = db.Column(db.Integer, db.ForeignKey('role_listing.rolelisting_ID'), primary_key=True)
    application_date = db.Column(db.Date, nullable=False)
    percentage_match = db.Column(db.Numeric(precision=5, scale=2), nullable=False)
    

    # properties of the role_listing when it is created
    def __init__(self, staff_ID, rolelisting_ID, application_date, percentage_match):
        self.staff_ID = staff_ID
        self.rolelisting_ID = rolelisting_ID
        self.application_date = application_date
        self.percentage_match = percentage_match


    # specify how to represent our role_listing object as a JSON string
    def json_by_rolelistingID(self):
        return {
            "staff_ID": self.staff_ID,
            "application_date": self.application_date.strftime('%Y-%m-%d'),
            "percentage_match": self.percentage_match
        }
    
    def json_by_rolelistingID_staffID(self):
        return {
            "application_date": self.application_date.strftime('%Y-%m-%d'),
            "percentage_match": self.percentage_match
        }
    
    def json_by_staffID(self):
        return {
            "rolelisting_ID": self.rolelisting_ID,
            "application_date": self.application_date.strftime('%Y-%m-%d'),
            "percentage_match": self.percentage_match
        }
    
    def json(self):
        return {
            "staff_ID": self.staff_ID,
            "rolelisting_ID": self.rolelisting_ID,
            "application_date": self.application_date.strftime('%Y-%m-%d'),
            "percentage_match": self.percentage_match
        }
    


#############################################################################################################
# Routing

# returns all staff
@app.route("/staff")
def get_all():
    stafflist = Staff.query.all()

    staff_results = []

    staffskilllist = StaffSkill.query.order_by(StaffSkill.staff_ID).all()

    staffskill_results = [staff_skill.staff_json() for staff_skill in staffskilllist] 

    for staff in stafflist:

        new_dict = staff.json()

        staff_ID = list(new_dict.keys())[0]

        matching_results = [item[staff_ID] for item in staffskill_results if staff_ID in item]

        new_dict[staff_ID]["staff_skills"] = matching_results     

        staff_results.append(new_dict)

    if len(stafflist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "staff": staff_results
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no staff."
        }
    ), 404

# return 1 staff
@app.route("/staff/<staff_ID>")
def find_by_staffID(staff_ID):
    staff = Staff.query.filter_by(staff_ID=staff_ID).first()
    if staff:
        return jsonify(
            {
                "code": 200,
                "data": staff.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Staff does not exist."
        }
    ), 404


# return skill_sets of particular staff
@app.route('/get_staff_skill/<staff_ID>')
def get_staff_skill(staff_ID):

    staffskilllist = StaffSkill.query.filter_by(staff_ID = staff_ID).all()

    return jsonify(
        {
            "code": 200,
            "data": [staff_skill.json() for staff_skill in staffskilllist]
        }
    )

# to retrieve dept & country in a list
@app.route('/get_dept_country/<column_name>')
def enum_values(column_name):
    
    column = getattr(Staff, column_name)

    if hasattr(column.type, "enums"):
        enum_values = column.type.enums
        enum_values.sort()
        return jsonify(
        {
            "code": 200,
            "data": enum_values
        }
    )


# to retrieve all skill & skill_desc in a list of dictionary
@app.route('/get_all_skill')
def get_all_skill():

    skilllist = Skill.query.all()

    return jsonify(
        {
            "code": 200,
            "data": [skill.json() for skill in skilllist]
        }
    )


# to retrieve all role & role_desc in a list of dictionary
@app.route('/get_all_role')
def get_all_role():

    rolelist = Role.query.all()

    return jsonify(
        {
            "code": 200,
            "data": [role.json() for role in rolelist]
        }
    )


# get skill sets of a specific role
@app.route('/get_role_skill/<role_name>')
def get_role_skill(role_name):

    roleskilllist = RoleSkill.query.filter_by(role_name = role_name).all()

    return jsonify(
        {
            "code": 200,
            "data": [role_skill.json() for role_skill in roleskilllist]
        }
    )


# returns all open role listing
@app.route("/openrolelisting")
def get_all_open_rolelisting():

    # get rolelisting whereby the application_opening is before today inclusive
    condition1 = RoleListing.application_opening <= db.func.current_date() + 1
    # get rolelisting whereby the application_deadline is today or after
    condition2 = RoleListing.application_deadline >= db.func.current_date() + 1

    manager_ID = request.args.get('manager_ID')

    condition3 = RoleListing.manager_ID == manager_ID

    if manager_ID:
        rolelistinglist = RoleListing.query.filter(condition1, condition2, condition3).all()

    else:
        rolelistinglist = RoleListing.query.filter(condition1, condition2).all()


    if len(rolelistinglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "rolelisting": [rolelisting.json() for rolelisting in rolelistinglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no open role listings."
        }
    ), 404


# returns all close role listing - only for HR
@app.route("/closerolelisting")
def get_all_close_rolelisting():

    # get rolelisting whereby the application_opening is before today inclusive
    condition1 = RoleListing.application_opening <= db.func.current_date() + 1
    # get rolelisting whereby the application_deadline is today or after
    condition2 = RoleListing.application_deadline >= db.func.current_date() + 1

    rolelistinglist = RoleListing.query.filter(~(condition1 & condition2)).all()
    if len(rolelistinglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "rolelisting": [rolelisting.json() for rolelisting in rolelistinglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no close role listings."
        }
    ), 404


# get specific role listing
# this function does not check if the role is open or not (i did not add bcos we want HR can see close role listing)
@app.route("/rolelisting/<rolelisting_ID>")
def get_a_rolelisting(rolelisting_ID):

    rolelisting = RoleListing.query.filter_by(rolelisting_ID=rolelisting_ID).first()

    if rolelisting:
        return jsonify(
            {
                "code": 200,
                "data": rolelisting.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Role Listing does not exist."
        }
    ), 404


# add a role listing 
@app.route("/addrolelisting", methods=['POST'])
def create_rolelisting():

    # this returns in dictionary format
    rolelisting = request.get_json()

    # check if role listing exists
    condition1 = RoleListing.role_name == rolelisting["role_name"]
    condition2 = RoleListing.application_opening == rolelisting["application_opening"]
    condition3 = RoleListing.application_deadline == rolelisting["application_deadline"]
    condition4 = RoleListing.manager_ID == rolelisting["manager_ID"]
    condition5 = RoleListing.dept == rolelisting["dept"]
    condition6 = RoleListing.country == rolelisting["country"]

    results = RoleListing.query.filter(condition1, condition2, condition3, condition4, condition5, condition6).first()

    if results:
        return jsonify(
            {
                "code": 400,
                "data": rolelisting,
                "message": "Role Listing exists."
            }
        ), 400

    # creating the role listing instance
    new_rolelisting = RoleListing(**rolelisting)

    try:
        db.session.add(new_rolelisting)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": rolelisting,
                "message": "An error occurred creating the role listing."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_rolelisting.json()
        }
    ), 201


# update a role listing
@app.route("/updaterolelisting/<rolelisting_ID>", methods=['PUT'])
def update_rolelisting(rolelisting_ID):

    rolelisting = request.get_json()

    # check if role listing exists

    condition1 = RoleListing.role_name == rolelisting["role_name"]
    condition2 = RoleListing.application_opening == rolelisting["application_opening"]
    condition3 = RoleListing.application_deadline == rolelisting["application_deadline"]
    condition4 = RoleListing.manager_ID == rolelisting["manager_ID"]
    condition5 = RoleListing.dept == rolelisting["dept"]
    condition6 = RoleListing.country == rolelisting["country"]

    results = RoleListing.query.filter(condition1, condition2, condition3, condition4, condition5, condition6).first()

    if results:
        return jsonify(
            {
                "code": 400,
                "data": rolelisting,
                "message": "Role Listing exists."
            }
        ), 400
    
    
    update_rolelisting = RoleListing.query.filter_by(rolelisting_ID=rolelisting_ID).first()

    update_rolelisting.role_name = rolelisting["role_name"]
    update_rolelisting.application_opening = datetime.strptime(rolelisting["application_opening"], "%Y-%m-%d").date()
    update_rolelisting.application_deadline = datetime.strptime(rolelisting["application_deadline"], "%Y-%m-%d").date()
    update_rolelisting.manager_ID = rolelisting["manager_ID"]
    update_rolelisting.dept = rolelisting["dept"]
    update_rolelisting.country = rolelisting["country"]

    db.session.commit()

    return jsonify(
        {
            "code": 200,
            "data": update_rolelisting.json()
        }
    )


# delete a role listing
@app.route("/deleterolelisting/<rolelisting_ID>", methods=['DELETE'])
def delete_rolelisting(rolelisting_ID):

    # Check if the role listing exists in the database
    rolelisting = RoleListing.query.filter_by(rolelisting_ID=rolelisting_ID).first()

    if rolelisting:
        try:
            db.session.delete(rolelisting)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": rolelisting_ID,
                    "message": "Role Listing deleted successfully"
                }
            ), 200
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "data": rolelisting,
                    "message": "An error occurred when deleting the role listing."
                }
            ), 500
    else:
        return jsonify(
            {
                "code": 404,
                "data": rolelisting_ID,
                "message": "Role Listing does not exist."
            }
        ), 404

# get all applications from a rolelisting_ID
# or choose to get 1 application from a rolelisting_ID by passing the staff_ID in params
#   e.g., /applications/1?staff_ID=1030
@app.route("/applications/<rolelisting_ID>")
def get_all_applications_for_a_rolelisting(rolelisting_ID):

    staff_ID = request.args.get('staff_ID')

    if staff_ID:
        results = Application.query.filter_by(rolelisting_ID=rolelisting_ID, staff_ID=staff_ID).order_by(Application.application_date, desc(Application.percentage_match)).first()

    else:
        results = Application.query.filter_by(rolelisting_ID=rolelisting_ID).order_by(Application.application_date, desc(Application.percentage_match)).all()

    if results:

        if staff_ID:
            return jsonify(
            {
                "code": 200,
                "data": results.json_by_rolelistingID_staffID()
            }
        )

        return jsonify(
            {
                "code": 200,
                "data": [applicants.json_by_rolelistingID() for applicants in results]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no applicants for the role."
        }
    ), 404


# add an application
@app.route("/addapplication", methods=['POST'])
def create_application():

    # this returns in dictionary format
    application = request.get_json()

    # check if role listing exists
    condition1 = Application.staff_ID == application["staff_ID"]
    condition2 = Application.rolelisting_ID == application["rolelisting_ID"]
    
    results = Application.query.filter(condition1, condition2).first()

    if results:
        return jsonify(
            {
                "code": 400,
                "data": application,
                "message": "Application exists."
            }
        ), 400

    # creating the role listing instance
    new_application = Application(**application)

    try:
        db.session.add(new_application)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": application,
                "message": "An error occurred creating the application."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_application.json()
        }
    ), 201


# delete an application
@app.route("/deleteapplications/<staff_ID>/<rolelisting_ID>", methods=['DELETE'])
def delete_application(staff_ID, rolelisting_ID):

    # Check if the role listing exists in the database
    application = Application.query.filter_by(staff_ID=staff_ID, rolelisting_ID=rolelisting_ID).first()

    if application:
        try:
            db.session.delete(application)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "staff_ID": staff_ID,
                        "rolelisting_ID": rolelisting_ID
                        },
                    "message": "Application deleted successfully"
                }
            ), 200
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "staff_ID": staff_ID,
                        "rolelisting_ID": rolelisting_ID
                        },
                    "message": "An error occurred when deleting the application."
                }
            ), 500
    else:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "staff_ID": staff_ID,
                    "rolelisting_ID": rolelisting_ID
                    },
                "message": "Application does not exist."
            }
        ), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
