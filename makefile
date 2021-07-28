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
	poetry run mypy . --ignore-missing-imports

run:
	poetry run main

view :
	pytest -s .\tests\test_view.py::test_draw_trade_data_view