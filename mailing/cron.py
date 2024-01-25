from mailing.management.commands.start_mailing import Command


def scheduled_mailing():
    Command().start_mailing()
