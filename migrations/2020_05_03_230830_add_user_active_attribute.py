from orator.migrations import Migration


class AddUserActiveAttribute(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('users') as table:
            table.boolean('active').default('false')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('users') as table:
            table.drop_column('active')
