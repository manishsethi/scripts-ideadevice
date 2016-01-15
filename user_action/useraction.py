#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
#    Write a web application to accept the following and create, delete or
#      modify a user with the same on a linux machine:

#    1. username
#    2. Shell type
#    3. Home folder
#    4. Password
#    5. Grant sudo privileges to the user or not.
#    6. Select between create, delete and modify.

#    The application has to be written in Python using the flask web framework.
#    The application will need to run as a specified user (The user will have sudo privileges).
#    The application will need to validate the input, verify that the username provided can indeed be created,
#    and go ahead with the specified operation that has been input.

# Author:  Manish Sethi
# Date: 15-1-2015
###############################################################################
from flask import Flask
from flask import render_template
from flask import request
import subprocess
import sys
import crypt

app = Flask(__name__)


def delUser(username):
    retStatement = ''
    delUserCommand = 'userdel -r ' + username

    try:
        cmd = subprocess.Popen(delUserCommand, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        (out, error) = cmd.communicate()
    except OSError, e:
        retStatement = 'userdel: Execution failed: '

    retStatement = out + ' ' + error
    print 'userdel: ' + retStatement

    # User add failed.

    if int(cmd.returncode) != 0:
        retVal = 'Failure:'
        retStatement = retVal + retStatement
    else:
        retVal = 'Success:'
        retStatement = retVal + retStatement

    return retStatement


def modUser(
    username,
    password,
    home,
    shelltype,
    ):
    retStatement = ''

    print 'username: ', username
    print 'password: ', password
    print 'home:     ', home
    print 'shell:    ', shelltype

    modUserCmd = 'usermod'

    if password != '':
        modUserCmd = modUserCmd + ' -p ' + password

    if shelltype != '':
        modUserCmd = modUserCmd + ' -s ' + shelltype

    if home != '':
        modUserCmd = modUserCmd + ' -d ' + home + ' -m '

    modUserCmd = modUserCmd + ' ' + username

    try:
        cmd = subprocess.Popen(modUserCmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        (out, error) = cmd.communicate()
    except OSError, e:
        retStatement = 'userdel: Execution failed: '

    retStatement = out + ' ' + error
    print 'usermod: ' + retStatement

    # User add failed.

    if int(cmd.returncode) != 0:
        retVal = 'Failure:'
        retStatement = retVal + retStatement
    else:
        retVal = 'Success:'
        retStatement = retVal + retStatement

    return retStatement


def createUser(
    username,
    password,
    home,
    shelltype,
    isGrantSudo,
    ):
    retStatement = ''
    print 'username: ', username
    print 'password: ', password
    print 'home:     ', home
    print 'shell:    ', shelltype
    print 'isGrantSudo: ', isGrantSudo

    encPassword = crypt.crypt(password, '22')

    if shelltype != '':
        myuserCreate = 'useradd -p ' + encPassword + ' -s ' + shelltype
    else:
        myuserCreate = 'useradd -p ' + encPassword

    if home == '':
        myuserCreate = myuserCreate + ' ' + username
    else:
        myuserCreate = myuserCreate + ' -d ' + home + ' -m ' + username

    print 'useradd: ', myuserCreate

    try:
        cmd = subprocess.Popen(myuserCreate, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        (out, error) = cmd.communicate()
    except OSError, e:
        retStatement = 'useradd: Execution failed: '

    retStatement = out + ' ' + error
    print 'useradd: ' + retStatement

    # User add failed.

    if int(cmd.returncode) != 0:
        retVal = 'Failure:'
        retStatement = retVal + retStatement
        print 'Error: ', retStatement
        return retStatement

    # Add the user to Sudoers.

    if int(isGrantSudo) == 1:
        addSudoers = 'adduser ' + username + ' sudo'
        print 'addSudoers: ', addSudoers
        try:
            cmd = subprocess.Popen(addSudoers, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            (out, error) = cmd.communicate()
        except OSError, e:
            retStatement = 'adduser: Execution failed: '

        retStatement = retStatement + ', ' + out + ', ' + error

    if int(cmd.returncode) == 0:
        retVal = 'Success:'
        retStatement = retVal + retStatement
    else:
        retVal = 'Failure:'
        retStatement = retVal + retStatement

    print 'retStatement: ', retStatement

    return retStatement


@app.route('/')
def my_form():
    return render_template('my-form.html')


@app.route('/executeCmd', methods=['POST'])
def my_form_post():

    operation = request.form.get('operation', 0)

    if operation and int(operation) == 1 and request.form.get('userName'
            , 0) and request.form.get('passWord', 0) \
        and request.form.get('operation', 0):

        print 'Create: Operation'
        status = 'Failed'
        operation = 0  # 1 -> Create, 2 -> Delete, 3 -> Modify
        isGrant = 0
        userName = request.form['userName']
        shellType = request.form['shellType']
        homeFolder = request.form['homeFolder']
        passWord = request.form['passWord']

        if request.form.get('isGrant', 0):
            isGrant = 1
        else:
            isGrant = 0

        if request.form.get('operation', 0):
            operation = request.form['operation']

        retStatement = ''

        retStatement = createUser(userName, passWord, homeFolder,
                                  shellType, isGrant)
        return retStatement
    elif int(operation) == 2 and request.form.get('userName', 0):

        print 'Delete Operation:'
        userName = request.form['userName']
        retStatement = delUser(userName)
        return retStatement
    elif int(operation) == 3 and request.form.get('userName', 0):

        print 'Modify Operation:'
        userName = request.form['userName']
        passWord = request.form['passWord']
        homeFolder = request.form['homeFolder']
        shellType = request.form['shellType']

        retStatement = modUser(userName, passWord, homeFolder,
                               shellType)
        return retStatement
    else:

        return 'Failure: Fields Missing.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

			
