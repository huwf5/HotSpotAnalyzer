backend_base_dir = backend
web_base_dir = web

.PHONY: all
all:
	@echo "Please specify a target to start!"

.PHONY: server_build_deps
server_build_deps:
	@echo "Building backend dependencies..."
	@cd $(backend_base_dir) && poetry install

.PHONY: enter_virtualEnv
enter_virtualEnv:
	@echo "Entering virtual environment..."
	@cd $(backend_base_dir) && poetry shell

.PHONY: server_init_db
server_init_db: enter_virtualEnv
	@echo "Initializing database..."
	@cd $(backend_base_dir) && python manage.py makemigrations && python manage.py migrate
	@echo "Adding initial data..."
	@cd $(backend_base_dir) && python manage.py init

.PHONY: server_collect_static
server_collect_static: enter_virtualEnv
	@echo "collecting static files..."
	@mkdir -p $(backend_base_dir)/static
	@cd $(backend_base_dir) && python manage.py collectstatic --noinput

.PHONY: run_server
run_server: enter_virtualEnv
	@echo "Running server..."
	@cd $(backend_base_dir) && python manage.py runserver

.PHONY: clean
clean:
	@echo "Cleaning up..."