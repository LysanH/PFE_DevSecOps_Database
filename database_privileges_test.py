#!/usr/bin/python

import json
import pymysql
import re

class User:
    databases = {}
    privileges = {}
    crud_right = ('Select_priv', 'Insert_priv', 'Update_priv', 'Delete_priv', 'Show_view',
                  'Index_priv', 'Create_view', 'Create_temporary_tables',)
    list_db_right = ('Show_db_priv',)
    table_modifier_right = ('Drop_priv', 'Create_priv')
    server_administration_right =('Create_tablespace_priv','Create_user_priv','Process_priv', 'Proxy_priv','Reload_priv',
        'Repl_client_priv', 'Repl_slave_priv', 'Show_db_priv', 'Shutdown_priv', 'Super_priv',)
    grant_right = ('Grant_priv',)
    trigger_right=('Trigger_priv',)
    tables = {}
    user = ''
    host = ''

    def __init__(self, user, host):
        self.user = user
        self.host = host

    def parse_show_grant_user(self, privileges):
        self.privileges = {**self.privileges, **privileges}

    def parse_show_grant_db(self, databases):
        self.databases = {**self.databases, **databases}

    def parse_show_grant(self, grant):
        print('Parsing grant ....', grant)
        for g in grant:
            matchObj = re.match( r'grant (.*) on (.*)\.(.*) to (.*)@(.*)', g, re.I)
            if matchObj:
                if self.database.get(matchObj.group(2), 'false') == 'false':
                    if self.database[matchObj.group(2)].has_key(matchObj.group(3), 'false') == 'false':
                        self.database[matchObj.group(2)][matchObj.group(3)].add(matchObj.group(1))
                    else:
                        self.database[matchObj.group(2)][matchObj.group(3)] = Privilege(matchObj.group(1))
                else:
                    self.database[matchObj.group(2)][matchObj.group(3)] = Privilege(matchObj.group(1))

    def set_all_privileges(self, database):
        print("Setting privileges")

    def dump(self):
        print("User: %s, Host: %s \nGobal Right:\n %s\n Databases Right:\n %s" %
              (self.user, self.host, self.privileges, self.databases))

    def analyseRights(self):
        print('User: %s, Host: %s'%(self.user, user.host))
        
        print("\tGlobal privilege")
        self.analyse(self.privileges)
        for key, values in self.databases.items():
            print("\tPrivilege on %s DB"%key)
            self.analyse(values)
        
    def analyse(self, tab):
        all_privileges = 1
        
        for key, values in tab.items():
            if values == 'N':
                all_privileges = 0
                break;
        if all_privileges == 1 :
            print("\t\tTous les privilèges accordés")

        for c in self.crud_right:
            if (tab.get(c, 'N') == 'Y'):
                print("\t\t- Droit de requête")
                break;
            
        for c in self.list_db_right:
            if (tab.get(c, 'N') == 'Y'):
                print("\t\t- Droit de lister les bases de données")
                break;
            
        for c in self.table_modifier_right:
            if (tab.get(c, 'N') == 'Y'):
                print("\t\t- Droit de créer ou modifier une table")
                break;
            
        for c in self.server_administration_right:
            if (tab.get(c, 'N') == 'Y'):
                print("\t\t- Droit d'administration du serveur")
                break;
        for c in self.grant_right:
            if (tab.get(c, 'N') == 'Y'):
                print("\t\t- Droit de transmettre un droit")
                break;
            
        for c in self.trigger_right:
            if (tab.get(c, 'N') == 'Y'):
                print("\t\t- Droit de créer des évènements")
                break;
    

with open('user.json', 'r') as f:
    user_list = json.load(f)

pfe_user = user_list[0]['pfedevsecops']
root_user = user_list[1]['root']
print(pfe_user)
db = pymysql.connect(pfe_user['host'],pfe_user['username'],pfe_user['password'])
#db = pymysql.connect(root_user['host'],root_user['username'],root_user['password'])
cursor = db.cursor();

cursor.execute("SELECT `user`, `host` FROM `mysql`.`user`")
database_users = cursor.fetchall()
users_list = []
for row in database_users:
    user = User(row[0], row[1])
    #print ('------------------------------------------------------------\n')
    cursor.execute("SHOW COLUMNS FROM `mysql`.`user`")
    columns = cursor.fetchall()
    cursor.execute("select * from mysql.user where User=%s and Host=%s;", (row[0], row[1]))
    right = cursor.fetchone()
    mapping = {}
    for i in range(0, len(columns)):
        mapping[columns[i][0]] = right[i]
    print(mapping)
    user.parse_show_grant_user(mapping)
    #print('-------------------------------------------------------------\n')
    cursor.execute("SHOW COLUMNS FROM `mysql`.`db`")
    columns = cursor.fetchall()
    cursor.execute("select * from mysql.db where User=%s and Host=%s;", (row[0], row[1]))
    right = cursor.fetchall()
    mapping = {}
    for r in right:
        mapping[r[2]] = {}
        for i in range(0, len(columns)):
            mapping[r[2]][columns[i][0]] = r[i]
    user.parse_show_grant_db(mapping)
    #print('-------------------------------------------------------------\n')
    users_list.append(user)

for user in users_list:
    print('-------------------------------------------------------------\n')
    user.analyseRights()

db.close()
