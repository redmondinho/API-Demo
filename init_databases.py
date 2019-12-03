from data.users import init_db as init_users
from data.tasks import init_db as init_tasks

from config import initial_username, initial_password, initial_email

if __name__ == '__main__':
	init_users(initial_password, initial_username, initial_email)
	init_tasks()