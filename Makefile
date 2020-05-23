CLEAN_SCRIPT_PATH=./Scripts/clean.py

clean: $(CLEAN_SCRIPT_PATH)
	@-python3 $(CLEAN_SCRIPT_PATH)

