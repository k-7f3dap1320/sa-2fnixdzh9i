# Copyright (c) 2018-present, Kahroo LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

class sa_db_access:

    def username(self):
        sa_usr = "__db_user_name__"
        return sa_usr

    def password(self):
        sa_pwd = "__mysql_user_password__"
        return sa_pwd

    def db_name(self):
        sa_db_name = "smartalpha"
        return sa_db_name

    def db_server(self):
        sa_srv = "localhost"
        return sa_srv
