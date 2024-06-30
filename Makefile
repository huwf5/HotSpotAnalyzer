backend_base_dir = backend
web_base_dir = web
analyze_dir = analyze

.PHONY: all
all:
	@echo "Please specify a target to start!"

.PHONY: server_build_deps
server_build_deps:
	@echo "Building backend dependencies..."
	@cd $(backend_base_dir) && poetry install

.PHONY: server_init_db
server_init_db: server_build_deps
	@echo "Initializing database..."
	@cd $(backend_base_dir) && poetry run python manage.py makemigrations && poetry run python manage.py migrate
	@echo "Adding initial data..."
	@cd $(backend_base_dir) && poetry run python manage.py init

.PHONY: run
run: 
	@echo "Building frontend..."
	@cd $(web_base_dir) && pnpm run build:pro

	@echo "collecting static files..."
	@mkdir -p $(backend_base_dir)/static
	@cd $(backend_base_dir) && poetry run python manage.py collectstatic --noinput

	@echo "Running server..."
	@cd $(backend_base_dir) && poetry run python manage.py runserver

.PHONY: analyze
analyze: 
	@echo "doing analyze process..."
	@cd crawler && poetry install
	@cd $(analyze_dir) && poetry install
	@$(MAKE) -C analyze

.PHONY: clean
clean:
	@echo "Cleaning up..."