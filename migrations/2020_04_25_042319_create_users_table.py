from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
    
        with self.schema.create('users') as table:
            table.increments('id')
            table.string('username', 12).unique()
            table.long_text('public_key')
            table.long_text('private_key')
            table.timestamps()
            table.soft_deletes()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
