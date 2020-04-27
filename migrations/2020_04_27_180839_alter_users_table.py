from orator.migrations import Migration


class AlterUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('users') as table:
            table.string('first_name').default('')
            table.string('last_name').default('')
            table.string('email').default('')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('users') as table:
            table.drop_column('first_name', 'last_name', 'email')
