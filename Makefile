install-deps:
	uv pip compile requirements.in -o requirements.txt && uv pip sync requirements.txt
