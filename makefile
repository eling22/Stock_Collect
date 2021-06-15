better :
	poetry run black .
	poetry run autoflake \
			--remove-unused-variables \
			--remove-all-unused-imports \
			--ignore-init-module-imports \
			--recursive\
			--in-place\
			.
	poetry run isort .
	poetry run mypy .

