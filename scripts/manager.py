# -*- coding:utf-8 -*-
import sys
sys.path.append('.')

from flask.ext.script import Manager, Shell, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand

from promise import app, db
from promise.user import utils as userUtils
from promise.user.models import User, Privilege, Role

migrate = Migrate(app, db)

manager = Manager(app, usage="Perform database operations")

manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    "initialize database tables"
    import os
    if not os.path.exists(app.config['DB_FOLDER']):
        os.mkdir(app.config['DB_FOLDER'])
    db.create_all()
    print 'Database inited, location: ' + app.config['SQLALCHEMY_DATABASE_URI']


@manager.command
def importdata():
    "Import data into database tables"

    user_admin_privilege = Privilege(
        privilege_name='userAdmin',
        description='user/role/privlilege administration.')
    inventory_admin_privilege = Privilege(
        privilege_name='InventoryAdmin',
        description='cmdb/inventory administration')
    shell_exec_privilege = Privilege(
        privilege_name='shellExec',
        description='execution of shell module of walker.')
    script_exec_privilege = Privilege(
        privilege_name='scriptExec',
        description='execution of script module of walker.')
    walker_info_privilege = Privilege(
        privilege_name='walkerInfo',
        description='get the details infomation of walkers.')
    user_admin_privilege.save()
    inventory_admin_privilege.save()
    shell_exec_privilege.save()
    script_exec_privilege.save()
    walker_info_privilege.save()

    # init roles
    role_root = Role(role_name='root', description='超级用户')
    role_operator = Role(role_name='operator', description='运维操作员')
    role_inventory_admin = Role(
        role_name='InventoryAdmin', description='资源管理员')
    role_user_admin = Role(role_name='userAdmin', description='用户管理员')

    role_root.update(
        privileges=[
            inventory_admin_privilege, user_admin_privilege,
            shell_exec_privilege, script_exec_privilege,
            walker_info_privilege])
    role_user_admin.update(privileges=[user_admin_privilege])
    role_inventory_admin.update(privileges=[inventory_admin_privilege])
    role_operator.update(
        privileges=[
            shell_exec_privilege, script_exec_privilege,
            walker_info_privilege])

#    db.session.add(roleRoot)
#    db.session.add(roleOperator)
#    db.session.add(roleInventoryAdmin)
#    db.session.commit()  # commit the roles before user init
    role_root.save()
    role_user_admin.save()
    role_inventory_admin.save()
    role_operator.save()

    # init users
    user1 = User(
        username='tom',
        hashed_password=userUtils.hash_pass("tompass"),
        role_list=[role_operator])
    user2 = User(
        username='jerry',
        hashed_password=userUtils.hash_pass("jerrypass"),
        role_list=[role_inventory_admin])
    user3 = User(
        username='mike',
        hashed_password=userUtils.hash_pass("mikepass"),
        role_list=[role_user_admin])
    # user2.addRole(role=roleInventoryAdmin)
    root_user = User(
        username=app.config['DEFAULT_ROOT_USERNAME'],
        hashed_password=userUtils.hash_pass(
            app.config['DEFAULT_ROOT_PASSWORD']),
        role_list=[role_root])
    visitor = User(
        username='visitor',
        hashed_password=userUtils.hash_pass('visitor'))

    user1.save()
    user2.save()
    user3.save()
    root_user.save()
    visitor.save()
    print 'Data imported'


@manager.command
def dropdb():

    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print 'Database droped.'


@manager.command
def recreatedb():
    "Recreates database tables \
    (same as issuing 'drop', 'create' and then 'import')"
    dropdb()
    initdb()
    importdata()


def _make_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=_make_context))


if __name__ == '__main__':
    manager.run()
