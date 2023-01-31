compile_run: eight_queen.o
	./eight_queen > output.txt
eight_queen.o: 
	g++ eight_queen.cpp -o eight_queen