from users import init_db as init_users
from tasks import init_db as init_tasks

if __name__ == '__main__':
	init_users()
	init_tasks()
