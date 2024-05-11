backend_base_dir = backend
web_base_dir = web

.PHONY: all
all:
	@echo "Please specify a target to start!"

.PHONY: server_build_deps
server_build_deps:
	@echo "Building backend dependencies..."
	@cd $(backend_base_dir) && poetry install

.PHONY: server_init_db
server_init_db:
	@echo "Initializing database..."
	@cd $(backend_base_dir) && python manage.py makemigrations && python manage.py migrate

.PHONY: run_server
run_server:
	@echo "Running server..."
	@cd $(backend_base_dir) && python manage.py runserver

.PHONY: clean
clean:
	@echo "Cleaning up..."