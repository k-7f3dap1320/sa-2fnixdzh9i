""" App database access information """
class sa_db_access:

    def username(self):
        """ Get database username """
        sa_usr = "__db_user_name__"
        return sa_usr

    def password(self):
        """ Get database password """
        sa_pwd = "__mysql_user_password__"
        return sa_pwd

    def db_name(self):
        """ Get database name """
        sa_db_name = "smartalpha"
        return sa_db_name

    def db_server(self):
        """ Get database server address """
        sa_srv = "localhost"
        return sa_srv
